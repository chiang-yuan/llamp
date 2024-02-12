import re
import os
import asyncio

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import ArxivQueryRun, WikipediaQueryRun, tool
from langchain.tools.render import render_text_description_and_args, format_tool_to_openai_function
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain.prompts import MessagesPlaceholder
from langchain.schema import ChatMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from queue import Queue
from pydantic import BaseModel
from typing import Any, AsyncIterator, List, Literal


from llamp.mp.agents import (
    MPSummaryExpert,
    MPThermoExpert,
    MPElasticityExpert,
    MPDielectricExpert,
    MPPiezoelectricExpert,
    MPMagnetismExpert,
    MPElectronicExpert,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

OPENAI_GPT_MODEL = "gpt-4-1106-preview"


mp_llm = ChatOpenAI(
    temperature=0,
    model=OPENAI_GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    openai_organization=None,
    max_retries=5,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

llm = ChatOpenAI(
    temperature=0,
    model=OPENAI_GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    openai_organization=None,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
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
    MPSummaryExpert(llm=mp_llm).as_tool(
        agent_kwargs=dict(return_intermediate_steps=False)),
    # arxiv,
    # wikipedia,
]

prompt = hub.pull("hwchase17/react-multi-input-json")
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

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm.bind(stop=["Observation"])
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

agent_executor = initialize_agent(
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=10,
    memory=conversational_memory,
    agent_kwargs=agent_kwargs,
    handle_parsing_errors=True,
)

app = FastAPI()


class Query(BaseModel):
    text: str


@app.get('/health')
async def health():
    return {"status": "ok"}


class CustomHandler(AsyncIteratorCallbackHandler):
    async def on_chat_model_start(self, *args, **kwargs):
        # Implement your logic here
        # This method will be called when the chat model starts processing
        pass


async def run_call(input: str, stream_it: CustomHandler):
    agent_executor.agent.llm_chain.llm.callbacks = [stream_it]
    response = await agent_executor.ainvoke({
        "input": input
    })
    return response


async def create_gen(input: str, stream_it: CustomHandler):
    task = asyncio.create_task(run_call(input, stream_it))
    async for token in stream_it.aiter():
        yield token
    await task


@app.get('/chat')
async def chat(query: Query):
    stream_it = CustomHandler()
    gen = create_gen(query.text, stream_it)
    return StreamingResponse(gen, media_type="text/plain")


# agent_executor.invoke({
#    "input": "What's the bandgap of CsPbI3?"
# })


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
