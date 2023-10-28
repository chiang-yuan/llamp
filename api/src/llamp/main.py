
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
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

'''
agent = {
    "input": lambda x: x["input"],
    "chat_history": lambda x: x["chat_history"],
    "agent": AgentType.OPENAI_MULTI_FUNCTIONS,
}
'''

llm = ChatOpenAI(temperature=0, model='gpt-4')
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are very powerful assistant, but bad at calculating lengths of words."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

llm_with_tools = llm.bind(
    functions=[format_tool_to_openai_function(t) for t in tools]
)

memory = ConversationBufferMemory(memory_key="chat_history")

agent = {
    "input": lambda x: x["input"],
    "agent_scratchpad": lambda x: format_to_openai_functions(x['intermediate_steps'])
} | prompt | llm_with_tools | OpenAIFunctionsAgentOutputParser()

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True)

initialize_agent(agent_executor, memory=memory)

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

    output = agent_executor.invoke({
        "input": messages[-1].content,
        'chat_history': chat_history,
    })
    print(output)
    return {
        "responses": [{
            'role': 'assistant',
            'content': output['output']
        }],
    }

if __name__ == "__main__":
    uvicorn.run(app="app", host="127.0.0.1", port=8000, reload=True)
