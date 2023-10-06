
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from pydantic import BaseModel

from llamp.mp.agent import MPLLM, MultiLLaMP

llm = ChatOpenAI(
    temperature=0.0,
)  # Grabs the API Key from os.environ
qa_chain = load_qa_chain(llm, chain_type="stuff")

app = FastAPI()
multiagent = MultiLLaMP()

mp = MPLLM()
# # search = SerpAPIWrapper()  # get SERPAPI_API_KEY from .env
# search = GoogleSearchAPIWrapper()
# wiki = WikipediaAPIWrapper()
# arxiv = ArxivAPIWrapper()

# tools = [
#     Tool(
#         name="Search",
#         func=search.run,
#         description="useful when you need general but unreliable information about a topic on the web",
#     ),
#     Tool(
#         name="Wikipedia",
#         func=wiki.run,
#         description="useful when you need foundational knowldge about a topic on Wikipedia",
#     ),
#     Tool(
#         name="ArXiv",
#         func=arxiv.run,
#         description="useful when you need to search literature or compare Materials Project database with literature data.",
#     ),
#     Tool(
#         name="MP",
#         func=mp.run,
#         description="useful when you need rich, reliable, and expert-curated materials science data.",
#     ),
# ]


# agent_executor = AgentExecutor.from_agent_and_tools(
#     agent=multiagent, tools=tools, verbose=True
# )


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def main():
#     return {"message": "Hello World"}


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

class MessageContent(BaseModel):
    content: str


# class ChatMessage(BaseModel):
#     role: str
#     content: str


@app.post("/ask/")
async def ask(messages: list[ChatMessage]):
    # responses = []
    # for message in messages:
    #     response = mp.run(
    #         message=message,
    #         model="gpt-3.5-turbo-16k",
    #         debug=True
    #     )
    #     responses.append(response)

    response = mp.run(
        messages=messages,
        model="gpt-3.5-turbo-16k",
        debug=True
    )

    return {
        "responses": response,
    }

# @app.post("/multi")
# async def multi(message: ChatMessage):
#     pass


if __name__ == "__main__":
    uvicorn.run(app="app", host="127.0.0.1", port=8000, reload=True)
