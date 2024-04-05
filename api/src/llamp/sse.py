import asyncio
import os
import uuid
import json

import redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.agents import AgentType, initialize_agent
from langchain.callbacks.base import BaseCallbackManager
from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from langchain.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from redis.client import PubSub
from pathlib import Path

from llamp.callbacks.streaming_redis_handler import StreamingRedisCallbackHandler
from llamp.mp.agents import (
    MPDielectricExpert,
    MPElasticityExpert,
    MPElectronicExpert,
    MPMagnetismExpert,
    MPPiezoelectricExpert,
    MPStructureRetriever,
    MPStructureVisualizer,
    MPSummaryExpert,
    MPSynthesisExpert,
    MPThermoExpert,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
OPENAI_GPT_MODEL = "gpt-4-1106-preview"  # TODO: allow user to choose LLMs
# TODO: allow user to choose both top-level and bottom-level agent LLMs
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)


wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str
    OpenAiAPIKey: str
    mpAPIKey: str
    chat_id: str = None


@app.get("/health")
async def health():
    return {"status": "ok"}


redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


async def listen_to_pubsub(pubsub: PubSub):
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            yield message["data"].decode()
        await asyncio.sleep(0.01)  # Prevents busy-waiting


async def agent_stream(
    input_data: str, chat_id: str, user_openai_api_key: str, user_mp_api_key: str
):
    top_level_cb = StreamingRedisCallbackHandler(
        redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_channel=chat_id
    )
    bottom_level_cb = StreamingRedisCallbackHandler(
        redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_channel=chat_id, level=1
    )

    mp_llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_GPT_MODEL,
        openai_api_key=user_openai_api_key,
        # TODO: organization
        organization=None,
        max_retries=5,
        streaming=True,
        callbacks=[bottom_level_cb],
    )

    tools = [
        MPThermoExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPElasticityExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPDielectricExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPMagnetismExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPElectronicExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPPiezoelectricExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPSummaryExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPSynthesisExpert(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPStructureVisualizer(llm=mp_llm, chat_id=chat_id, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=True)
        ),
        MPStructureRetriever(llm=mp_llm, mp_api_key=user_mp_api_key).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        arxiv,
        wikipedia,
    ]
    chat_id = chat_id.strip()
    conversation_redis_memory = ConversationBufferMemory(
        memory_key=chat_id,
        chat_memory=RedisChatMessageHistory(
            url=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
            session_id=chat_id,
        ),
        return_messages=True
    )

    llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_GPT_MODEL,
        # TODO: organization
        organization=None,
        openai_api_key=user_openai_api_key,
        streaming=True,
        callbacks=[top_level_cb],
    )

    SUFFIX = f"""
    Chat History {{{chat_id}}}
    Begin!
    Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
    Thought:"""

    # SUFFIX = f"""
    # Chat History {{{{chat_id}}}}
    # Begin!
    # Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate.

    # For each action, format the output as follows:
    # - For tool actions, use the [Tool] tag, followed by the tool name in angle brackets and the tool input in a separate tag.
    # - For API actions, use the [Api] tag, followed by the API endpoint in angle brackets and the JSON parameters enclosed in triple backticks.
    # - For observations, use the [Observation] tag, followed by the observation text.
    # - For final answers, use the [Final Answer] tag, followed by the answer text.

    # Example:
    # [Tool]
    # <tool-name>MPElasticityExpert</tool-name>
    # <tool-input>
    # What is the bulk modulus of iron (Fe)?
    # </tool-input>

    # [Api]
    # <api-endpoint>search_materials_elasticity__get</api-endpoint>
    # ```json
    # {{
    # "formula": "Fe"
    # }}

    # [Observation]
    # Observation Result
    # [Final Answer]
    # Example Final Answer
    # """

    agent_executor = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
        callback_manager=BaseCallbackManager(
            handlers=[top_level_cb]),
        memory=conversation_redis_memory,
        agent_kwargs={
            'suffix': SUFFIX,
        }
    )
    pubsub = redis_client.pubsub()
    pubsub.subscribe(chat_id)

    ainvoke_task = asyncio.create_task(
        agent_executor.ainvoke({"input": input_data}))

    async for message in listen_to_pubsub(pubsub):
        if message == "AGENT_FINISH":
            ainvoke_task.cancel()
            break
        yield message.encode("utf-8")

    # Ensure ainvoke_task is also completed before exiting
    await ainvoke_task


async def prepend_chat_id_to_stream(chat_id, stream_generator):
    yield f"[chat_id]{chat_id}\n".encode()
    async for data in stream_generator:
        yield data


@app.post("/chat")
async def chat(query: Query):
    print(query.OpenAiAPIKey)
    print(query.mpAPIKey)
    print(f"chat_id: {query.chat_id}")
    chat_id = query.chat_id
    if query.chat_id is None or query.chat_id == "":
        # TODO: check if exists in redis
        chat_id = str(uuid.uuid4())

    return StreamingResponse(
        prepend_chat_id_to_stream(chat_id, agent_stream(
            query.text, chat_id, query.OpenAiAPIKey, query.mpAPIKey)),
        media_type="text/plain",
    )


@app.get("/structures/{material_id}")
async def get_structure(material_id: str):
    out_dir = Path(__file__).parent.absolute() / "mp" / ".tmp"
    print(out_dir)
    fpath = out_dir / f"{material_id}.json"

    if fpath.exists():
        with open(fpath, "r") as f:
            structure_data = json.load(f)
        return structure_data
    else:
        raise HTTPException(status_code=404, detail="Structure not found")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
