from fastapi import APIRouter

from llamp.mp.agent import MPLLM

# from langchain.memory import RedisChatMessageHistory
# from langchain.schema import SystemMessage, messages_to_dict, AIMessage, HumanMessage
from langchain.schema import ChatMessage

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

agent = MPLLM()


@chat_router.post("/{chat_id}/question")
async def question(chat_id: str, message: ChatMessage):
    mpllm.run_material_conversation(message.content)

    return answer
