from fastapi import FastAPI
from llamp.mp.agent import MPLLM, MultiLLaMP

from langchain.schema import ChatMessage

from langchain.agents import Tool, AgentExecutor
from langchain.utilities import SerpAPIWrapper, WikipediaAPIWrapper, ArxivAPIWrapper

from langchain.chains.question_answering import load_qa_chain
from langchain.chains import ConversationalRetrievalChain

from langchain.chat_models import ChatOpenAI
from langchain.retrievers import WikipediaRetriever, ArxivRetriever

llm = ChatOpenAI(
    temperature=0.0,
)  # Grabs the API Key from os.environ
qa_chain = load_qa_chain(llm, chain_type="stuff")

app = FastAPI()
multiagent = MultiLLaMP()

mp = MPLLM()
search = SerpAPIWrapper()  # get SERPAPI_API_KEY from .env
wiki = WikipediaAPIWrapper()
arxiv = ArxivAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful when you need general but unreliable information about a topic on the web",
    ),
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="useful when you need foundational knowldge about a topic on Wikipedia",
    ),
    Tool(
        name="ArXiv",
        func=arxiv.run,
        description="useful when you need to search literature or compare Materials Project database with literature data.",
    ),
    Tool(
        name="MP",
        func=mp.run,
        description="useful when you need rich, reliable, and expert-curated materials science data.",
    ),
]


agent_executor = AgentExecutor.from_agent_and_tools(
    agent=multiagent, tools=tools, verbose=True
)


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


@app.post("/ask")
async def ask(message: ChatMessage):
    response = await mp.run(message=message)
    return {
        "response": response,
    }


@app.post("/multi")
async def multi(message: ChatMessage):
    pass
