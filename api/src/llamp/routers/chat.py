from fastapi import APIRouter

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

