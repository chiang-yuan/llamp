
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


from llamp.mp.tools import (
    MaterialsSummary,
    MaterialsSynthsis,
    MaterialsThermo,
    MaterialsElasticity
)

tools = [
    MaterialsSummary(),
    MaterialsSynthsis(),
    MaterialsThermo(),
    MaterialsElasticity()
]

# MEMORY_KEY = "chat_history"

llm = ChatOpenAI(temperature=0, model='gpt-4')

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
    agent=AgentType.OPENAI_MULTI_FUNCTIONS,
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

    print(output)
    return {
        "responses": [{
            'role': 'assistant',
            'content': output,
        }],
    }

if __name__ == "__main__":
    uvicorn.run(app="app", host="127.0.0.1", port=8000, reload=True)
