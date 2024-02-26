import asyncio
import os
import re
import uuid
from collections.abc import AsyncGenerator, Generator

import redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain import hub
from langchain.agents import AgentType, initialize_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
)
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import MessagesPlaceholder
from langchain.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.tools.render import render_text_description_and_args
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from llamp.callbacks.streaming_redis_handler import StreamingRedisCallbackHandler
from llamp.mp.agents import (
    MPDielectricExpert,
    MPElasticityExpert,
    MPElectronicExpert,
    MPMagnetismExpert,
    MPPiezoelectricExpert,
    MPStructureRetriever,
    MPSummaryExpert,
    MPSynthesisExpert,
    MPThermoExpert,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_GPT_MODEL = "gpt-4-1106-preview"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

top_level_callback_handler = StreamingRedisCallbackHandler(
    redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_channel='llm_stream')  # TODO: different redis channel for each chat_id

mp_llm = ChatOpenAI(
    temperature=0,
    model=OPENAI_GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    openai_organization=None,
    max_retries=5,
    streaming=True,
    callbacks=[top_level_callback_handler],
)

llm = ChatOpenAI(
    temperature=0,
    model=OPENAI_GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    openai_organization=None,
    streaming=True,
    callbacks=[top_level_callback_handler],
)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

tools = [
    MPThermoExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPElasticityExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPDielectricExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPMagnetismExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPElectronicExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPPiezoelectricExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPSummaryExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPSynthesisExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    MPStructureRetriever(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=True)),
    arxiv,
    wikipedia,
]

prompt = hub.pull("hwchase17/react-multi-input-json")
# prompt = hub.pull("hwchase17/structured-chat-agent")
# prompt = hub.pull("hwchase17/react")
prompt.messages[0].prompt.template = re.sub(
    r"\s+", " ",
    """You are a data-aware agent that can consult materials-related
    data through Materials Project (MP) database, arXiv, and Wikipedia. Ask 
    user to clarify their queries if needed. Please note that you don't have 
    direct control over MP but through multiple assistant agents to help you. 
    You need to provide complete context in the input for them to do their job.
    """).replace("\n", " ") + prompt.messages[0].prompt.template

prompt = prompt.partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)


model = ChatOpenAI(temperature=0, streaming=True, max_retries=5,
                   model=OPENAI_GPT_MODEL, api_key=OPENAI_API_KEY)
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm.bind(stop=["Observation"])
    # | map_reduce_chain  # TODO: Add map-reduce after LLM
    | JSONAgentOutputParser()
)

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

agent_kwargs = {
    "handle_parsing_errors": True,
    "extra_prompt_messages": [
        MessagesPlaceholder(variable_name="chat_history"),
    ],
}

agent_kwargs = {
    "handle_parsing_errors": True,
    "extra_prompt_messages": [
        MessagesPlaceholder(variable_name="chat_history"),
        # SystemMessage(content=re.sub(
        #     r"\s+", " ",
        #     """You are a helpful data-aware agent that can consult materials-related
        #     data through Materials Project (MP) database, arXiv, and Wikipedia. Ask
        #     user to clarify their queries if needed. Please note that you don't have
        #     direct control to MP but through multiple assistant agents to help you.
        #     You need to provide complete context for them to do their job.
        #     """).replace("\n", " ")
        # )
    ],
    "early_stopping_method": 'generate',
}

agent_executor = initialize_agent(
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=5,
    # memory=conversational_memory,
    # agent_kwargs=agent_kwargs,
    handle_parsing_errors=True,
    callback_manager=BaseCallbackManager(
        handlers=[top_level_callback_handler]),
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


@app.get('/health')
async def health():
    return {"status": "ok"}


redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0)


async def listen_to_pubsub(pubsub):
    while True:
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            yield message['data'].decode()
        await asyncio.sleep(0.1)  # Prevents busy-waiting


async def agent_stream(input_data: str, chat_id: str):
    pubsub = redis_client.pubsub()
    # pubsub.subscribe(chat_id)
    pubsub.subscribe('llm_stream')
    print("Subscribed to 'llm_stream' channel. Listening for new messages...")

    ainvoke_task = asyncio.create_task(
        agent_executor.ainvoke({"input": input_data}))

    async for message in listen_to_pubsub(pubsub):
        if message == "AGENT_FINISH":
            ainvoke_task.cancel()
            break
        yield message.encode('utf-8')

    # Ensure ainvoke_task is also completed before exiting
    await ainvoke_task


@app.post('/chat')
async def chat(query: Query):
    chat_id = str(uuid.uuid4())
    return StreamingResponse(agent_stream(query.text, chat_id), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
