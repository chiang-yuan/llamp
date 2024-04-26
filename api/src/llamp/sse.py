import asyncio
import json
import os
import uuid
import openai

import redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks.base import BaseCallbackManager
from langchain.memory import ConversationBufferMemory, RedisChatMessageHistory
from langchain.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from redis.client import PubSub
from mp_api.client import MPRester

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

OPENAI_GPT_MODEL = "gpt-4-1106-preview"  # TODO: allow user to choose LLMs
# TODO: allow user to choose both top-level and bottom-level agent LLMs
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)


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
    OpenAiOrg: str = None


@app.get("/api/health")
async def health():
    return {"status": "ok"}


redis_client = None
if REDIS_PASSWORD is None:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
else:
    redis_client = redis.Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)


async def listen_to_pubsub(pubsub: PubSub):
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            yield message["data"].decode()
        await asyncio.sleep(0.01)  # Prevents busy-waiting


def validate_openai_api_key(api_key: str):
    try:
        client = openai.OpenAI(api_key=api_key)
        client.models.list()
    except openai.AuthenticationError:
        return False, "Invalid OpenAI API Key"
    except openai.RateLimitError:
        return False, "OpenAI API Rate Limit Exceeded"
    except Exception as e:
        print(e)
        return False, "Unknown error"
    else:
        return True, None


def validate_mp_api_key(api_key: str):
    try:
        with MPRester(api_key) as mpr:
            mpr.get_material_id_references("mp-568")
    except Exception as e:
        print(e)
        return False, "Invalid MP API Key"
    else:
        return True, None


async def agent_stream(
    input_data: str, chat_id: str, user_openai_api_key: str, user_mp_api_key: str, user_openai_org: str
):
    top_level_cb = StreamingRedisCallbackHandler(
        redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_channel=chat_id, redis_password=REDIS_PASSWORD
    )
    bottom_level_cb = StreamingRedisCallbackHandler(
        redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_channel=chat_id, redis_password=REDIS_PASSWORD, level=1,
    )

    mp_llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_GPT_MODEL,
        openai_api_key=user_openai_api_key,
        organization=user_openai_org,
        max_retries=5,
        streaming=True,
        callbacks=[bottom_level_cb],
    )

    tools = load_tools(["llm-math"], llm=mp_llm)
    tools += [PythonREPLTool()]
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
    REDIS_URL = ""
    if REDIS_PASSWORD is not None:
        REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    else:
        REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    conversation_redis_memory = ConversationBufferMemory(
        memory_key=chat_id,
        chat_memory=RedisChatMessageHistory(
            url=REDIS_URL,
            session_id=chat_id,
        ),
        return_messages=True
    )

    llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_GPT_MODEL,
        organization=user_openai_org,
        openai_api_key=user_openai_api_key,
        streaming=True,
        callbacks=[top_level_cb],
    )

    SUFFIX = f"""
    Chat History {{{chat_id}}}
    Begin!
    Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
    Thought:"""

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
        },
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


@app.post("/api/chat")
async def chat(query: Query):
    chat_id = query.chat_id
    if query.chat_id is None or query.chat_id == "":
        while redis_client.exists(chat_id := str(uuid.uuid4())):
            pass

    valid, error = validate_openai_api_key(query.OpenAiAPIKey)
    if not valid:
        raise HTTPException(status_code=400, detail=error)

    valid, error = validate_mp_api_key(query.mpAPIKey)
    if not valid:
        raise HTTPException(status_code=400, detail=error)

    return StreamingResponse(
        prepend_chat_id_to_stream(chat_id, agent_stream(
            query.text, chat_id, query.OpenAiAPIKey, query.mpAPIKey, query.OpenAiOrg)),
        media_type="text/plain",
    )


@app.get("/api/structures/{material_id}")
async def get_structure(material_id: str):
    material = redis_client.get(material_id)
    trial = 0
    while material is None and trial < 5:
        await asyncio.sleep(1)
        material = redis_client.get(material_id)
        trial += 1

    if material is not None:
        return json.loads(material)

    raise HTTPException(status_code=404, detail="Structure not found")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
