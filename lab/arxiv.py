import os

import openai
from dotenv import load_dotenv

# from langchain.document_loaders import ArxivLoader
# from langchain.chains import APIChain
# from langchain.llms import OpenAI

# docs = ArxivLoader(query="topological semimetals", load_max_docs=2).load()
# print(len(docs))
# print(docs[0].metadata)
# print(docs[0].page_content[:400])

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY", None)

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0.0)
tools = load_tools(
    ["arxiv"],
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent_chain.run(
    "What's the paper 1605.08386 about?",
)
