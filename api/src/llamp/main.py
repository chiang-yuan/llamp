
from llamp.mp.tools import (
    MaterialsSummary,
    MaterialsSynthesis,
    MaterialsThermo,
    MaterialsElasticity,
    MaterialsMagnetism,
    MaterialsDielectric,
    MaterialsPiezoelectric,
    MaterialsRobocrystallographer,
    MaterialsOxidation,
    MaterialsBonds,
    MaterialsSimilarity,
    MaterialsStructure,
)
import json
from typing import Any
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from pydantic import BaseModel


def load_json(file_path: Path) -> Any:
    with file_path.open('r') as file:
        data = json.load(file)
    return data


# from llamp.elementari.tools import StructureVis

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
    MaterialsStructure(return_direct=True),
    # StructureVis(),
]

# MEMORY_KEY = "chat_history"

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-16k-0613')
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


def load_structures(str: str) -> list[Any]:
    str = str.replace('[structures]', '')
    mp_list = str.split(',')
    res = []
    for mp in mp_list:
        res.append(load_json(BASE_DIR / f'mp/.tmp/{mp}.json'))
    return res


@app.post("/ask/")
async def ask(messages: list[ChatMessage]):
    print(messages)
    '''
    chat_history = [lambda x:
                    HumanMessage(content=x.content) if x.role == "user" else AIMessage(
                        content=x.content)
                    for x in messages[:-1]]
    '''
    chat_history = [
        {
            "role": x.role,
            "content": x.content
        } for x in messages[:-1]
    ]

    '''
    output = agent_executor.invoke({
        "input": messages[-1].content,
        'chat_history': chat_history,
    })
    '''
    output = agent_executor.run(input=messages[-1].content)
    structures = []
    if (output.startswith('[structures]')):
        structures = [*load_structures(output)]
        output = ""

    return {
        "responses": [{
            'role': 'assistant',
            'content': output,
        }],
        "structures": structures,
    }

if __name__ == "__main__":
    uvicorn.run(app="app", host="127.0.0.1", port=8000, reload=True)
