
import json
from pathlib import Path
from typing import Any, List

import openai
import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import ChatMessage
from langchain.tools import ArxivQueryRun, WikipediaQueryRun
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
)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

tools = [
    MaterialsSummary(),
    MaterialsSynthesis(),
    MaterialsThermo(),
    MaterialsElasticity(),
    MaterialsMagnetism(),
    MaterialsDielectric(),
    MaterialsPiezoelectric(),
    MaterialsRobocrystallographer(),
    MaterialsOxidation(),
    MaterialsBonds(),
    MaterialsSimilarity(),
    MaterialsTasks(),
    MaterialsStructure(return_direct=True),
    NoseHooverMD(return_direct=True),
    # StructureVis(),
    arxiv,
    wikipedia
]

# MEMORY_KEY = "chat_history"

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k-0613',
                 # llm = ChatOpenAI(temperature=0, model='gpt-4',
                 openai_api_key="sk-xxxxxx")
# llm = ChatOpenAI(temperature=0, model='gpt-4')

memory = ConversationBufferMemory(memory_key="chat_history")

conversational_memory = ConversationBufferWindowMemory(
    memory_key='memory',
    k=5,
    return_messages=True
)
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}

agent_executor = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    agent_kwargs=agent_kwargs,
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
        res.append(load_json(BASE_DIR / f'mp/.tmp/{mp}.json'))
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
    key: str


@app.post("/ask/")
async def ask(data: MessageInput):
    messages = data.messages
    key = data.key
    print(key)
    agent_executor.agent.llm.openai_api_key = key

    output = None
    structures = []
    simulation_data = None
    try:
        # output = agent_executor.run(input=messages[-1].content)
        output = """[simulation]{"log": "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.log", "jsons": ["/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.1.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.2.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.3.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.4.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.5.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.6.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.7.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.8.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.9.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.10.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.11.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.12.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.13.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.14.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.15.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.16.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.17.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.18.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.19.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.20.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.21.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.22.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.23.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.24.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.25.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.26.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.27.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.28.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.29.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.30.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.31.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.32.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.33.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.34.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.35.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.36.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.37.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.38.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.39.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.40.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.41.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.42.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.43.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.44.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.45.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.46.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.47.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.48.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.49.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.50.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.51.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.52.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.53.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.54.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.55.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.56.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.57.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.58.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.59.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.60.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.61.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.62.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.63.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.64.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.65.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.66.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.67.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.68.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.69.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.70.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.71.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.72.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.73.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.74.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.75.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.76.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.77.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.78.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.79.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.80.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.81.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.82.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.83.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.84.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.85.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.86.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.87.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.88.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.89.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.90.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.91.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.92.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.93.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.94.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.95.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.96.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.97.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.98.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.99.json", "/usr/src/app/src/llamp/ase/.tmp/Mg4O8_2023-10-29-15-23-59.extxyz.100.json"]}
        """
        if (output.startswith('[structures]')):
            structures = [*load_structures(output)]
            output = ""
        if output.startswith('[simulation]'):
            structures, simulation_data = load_simulations(output)
            output = None
    except openai.error.AuthenticationError:
        output = "[Error] Invalid API key"

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
