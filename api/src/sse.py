import re
import os
import asyncio

from dotenv import load_dotenv
from typing import AsyncGenerator
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
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


model = ChatOpenAI(temperature=0, streaming=True, max_retries=5,
                   model=OPENAI_GPT_MODEL, api_key=OPENAI_API_KEY)
agent = create_openai_tools_agent(model.with_config(
    {'tags': ['react-multi-input-json']}), tools, prompt)

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

agent_executor = AgentExecutor(agent=agent, tools=tools).with_config({
    'run_name': 'react-multi-input-json',
})

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


async def agent_stream(input_data: str) -> AsyncGenerator[str, None]:
    async for chunk in agent_executor.astream({"input": input_data}):
        if "actions" in chunk:
            for action in chunk["actions"]:
                yield f"Calling Tool: `{action.tool}` with input `{action.tool_input}`\n"
        elif "steps" in chunk:
            for step in chunk["steps"]:
                yield f"Tool Result: `{step.observation}`\n"
        elif "output" in chunk:
            yield f'Final Output: {chunk["output"]}\n'
        else:
            raise ValueError()
        yield "---\n"


@app.get('/chat')
async def chat(query: Query):
    return StreamingResponse(agent_stream(query.text), media_type="text/plain")


# agent_executor.invoke({
#    "input": "What's the bandgap of CsPbI3?"
# })


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
