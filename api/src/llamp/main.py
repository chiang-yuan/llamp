
import json
import os
import re
from pathlib import Path
from typing import Any

import openai
import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    AgentType,
    BaseSingleActionAgent,
    Tool,
    initialize_agent,
    load_tools,
)
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import ChatMessage, SystemMessage
from langchain.tools import ArxivQueryRun, WikipediaQueryRun, tool
from langchain.tools.render import render_text_description_and_args
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from pydantic import BaseModel

from llamp.ase.tools import NoseHooverMD
from llamp.mp.tools import (
    MaterialsBonds,
    MaterialsDielectric,
    MaterialsElasticity,
    MaterialsMagnetism,
    MaterialsOxidation,
    MaterialsPiezoelectric,
    MaterialsRobocrystallographer,
    MaterialsSimilarity,
    MaterialsStructure,
    MaterialsSummary,
    MaterialsSynthesis,
    MaterialsTasks,
    MaterialsThermo,
    MPTool,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# MP React Agent

mp_tools = [
    MaterialsSummary(return_direct=False, handle_tool_error=True),
    MaterialsThermo(return_direct=False, handle_tool_error=True),
    MaterialsElasticity(return_direct=False, handle_tool_error=True),
    MaterialsMagnetism(return_direct=False, handle_tool_error=True),
    MaterialsDielectric(return_direct=False, handle_tool_error=True),
    MaterialsPiezoelectric(return_direct=False, handle_tool_error=True),
    MaterialsRobocrystallographer(return_direct=False, handle_tool_error=True),
    MaterialsOxidation(return_direct=False, handle_tool_error=True),
    MaterialsBonds(return_direct=False, handle_tool_error=True),
    MaterialsSimilarity(return_direct=False, handle_tool_error=True),
    # TODO: consider moving to another agent
    MaterialsSynthesis(return_direct=False, handle_tool_error=True),
    MaterialsTasks(return_direct=False, handle_tool_error=True),
]

mp_prompt = hub.pull("hwchase17/react-multi-input-json")
mp_prompt.messages[0].prompt.template = "You are a helpful agent having access to materials data on Materials Project." + mp_prompt.messages[0].prompt.template
mp_prompt = mp_prompt.partial(
    tools=render_text_description_and_args(mp_tools),
    tool_names=", ".join([t.name for t in mp_tools]),
)

# from langchain.chains import MapReduceDocumentsChain
# def map_fn(doc):
#     """Summarize each chunk"""
#     return mp_llm(f"Summarize this in 100 words: {doc}")  

# def reduce_fn(docs):
#     """Consolidate summaries"""
#     return mp_llm(f"Consolidate these summaries: {docs}")

# map_reduce_chain = MapReduceDocumentsChain(
#     map_fn=map_fn, 
#     reduce_fn=reduce_fn,
#     token_max=4000 # chunk size
# )

mp_llm = ChatOpenAI(
    temperature=0, 
    # model='gpt-3.5-turbo-16k-0613',
    model='gpt-3.5-turbo-16k-0613',
    openai_api_key=OPENAI_API_KEY
)

mp_llm_with_stop = mp_llm.bind(stop=["Observation"])

mp_agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | mp_prompt
    | mp_llm_with_stop
    # | map_reduce_chain # TODO: Add map-reduce after LLM
    | JSONAgentOutputParser()
)

mp_agent_executor = AgentExecutor(
    agent=mp_agent, 
    agent_kwargs={
        "system_message": SystemMessage(
        content=re.sub(
            r"\s+", " ", 
            """When you create function input arguments, follow MP API schema 
            strictcly and DO NOT hallucinate invalid arguments. Convert all acronyms 
            and abbreviations to valid arguments, especially chemical formula and 
            isotopes (e.g. D2O should be H2O), composition, and systems."""
            ).strip().replace("\n", " ")[0]
        )
    },
    tools=mp_tools, 
    return_intermediate_steps=True,
    verbose=True,
    handle_parsing_errors=True,
)  

@tool("MaterialsProject_React_Agent", return_direct=False)
def mp_react_agent(input: str):
    """Materials Project ReAct Agent that has access to MP database."""
    return mp_agent_executor.invoke(
        {
            "input": input
        }
    )#["output"]

# Top-level agent

llm = ChatOpenAI(
    # temperature=0,
    # model='gpt-4-32k',
    # model='gpt-3.5-turbo-1106',
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

tools = [
    mp_react_agent,
    # MaterialsStructure(return_direct=False),
    # NoseHooverMD(return_direct=False),
    arxiv,
    wikipedia,
] + load_tools(["llm-math"], llm=llm)


# MEMORY_KEY = "chat_history"

memory = ConversationBufferMemory(memory_key="chat_history") # FIXME: unsued?

conversational_memory = ConversationBufferWindowMemory(
    memory_key='memory',
    k=5,
    return_messages=True
)
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": SystemMessage(
        content=re.sub(
            r"\s+", " ", 
            """You are a data-aware agent that can consult Materials Project (MP) 
            agent who has access to MP database. Ask user for more details if needed
            """).strip().replace("\n", " ")[0]
        )
}

agent_executor = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    agent_kwargs=agent_kwargs,
    handle_parsing_errors=True,
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


class MessageContent(BaseModel):
    content: str


class ChatMessage(BaseModel):
    role: str
    content: str


BASE_DIR = Path(__file__).resolve().parent


def load_json(file_path: Path) -> Any:
    with file_path.open('r') as file:
        data = json.load(file)
    return data


def load_structures(str: str) -> list[Any]:
    str = str.replace('[structures]', '')
    mp_list = str.split(',')
    res = []
    for mp in mp_list:
        fpath = BASE_DIR / f'mp/.tmp/{mp}.json'
        res.append(load_json(fpath))
        os.remove(fpath)
    return res


def load_simulations(str: str) -> list[Any]:
    str = str.replace('[simulation]', '').strip()
    data = json.loads(str)
    print(data)

    df = pd.read_csv(  # noqa: PD901
        data['log'],
        delim_whitespace=True, skiprows=1, header=None,
        names=['Time[ps]', 'Etot/N[eV]', 'Epot/N[eV]', 'Ekin/N[eV]', 'T[K]',
            'stress_xx', 'stress_yy', 'stress_zz', 'stress_yz', 'stress_xz', 'stress_xy']
        )

    log_json = df.to_json(orient='records', date_format='iso')

    res = [load_json(Path(j)) for j in data['jsons'][0:10] if Path(j).exists()]

    return res, log_json


class MessageInput(BaseModel):
    messages: list[ChatMessage]
    openAIKey: str
    mpAPIKey: str


@app.post("/api/ask/")
async def ask(data: MessageInput): # FIXME: bad argument name
    messages = data.messages

    # if isinstance(agent_executor.agent.llm, ChatOpenAI | OpenAI):
    #     agent_executor.agent.llm.openai_api_key = data.openAIKey

    if isinstance(llm, ChatOpenAI | OpenAI):
        llm.openai_api_key = data.openAIKey
    
    if isinstance(mp_llm, ChatOpenAI | OpenAI):
        mp_llm.openai_api_key = data.openAIKey

    for tool in agent_executor.tools:
        if isinstance(tool, MPTool):
            tool.api_wrapper.set_api_key(data.mpAPIKey)

    for tool in mp_agent_executor.tools:
        if isinstance(tool, MPTool):
            tool.api_wrapper.set_api_key(data.mpAPIKey)

    output = None
    structures = []
    simulation_data = None
    try:
        output = agent_executor.run(input=messages[-1].content)
        if (output.startswith('[structures]')):
            structures = [*load_structures(output)]
            output = ""
        if output.startswith('[simulation]'):
            structures, simulation_data = load_simulations(output)
            output = None
    except openai.error.AuthenticationError as e:
        output = f"[error] {e}. Invalid API key. Please check your API key."
    except Exception as e:
        output = f"[error] {e}. Please try again."

    return {
        "responses": [{
            'role': 'assistant',
            'content': output,
        }],
        "structures": structures,
        "simulation_data": simulation_data
    }

if __name__ == "__main__":
    uvicorn.run(app="app", host="127.0.0.1", port=8000, reload=True)
