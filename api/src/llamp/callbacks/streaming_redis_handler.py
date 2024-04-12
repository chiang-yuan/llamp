import redis

from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.agents import AgentFinish, AgentAction
from typing import Any


class StreamingRedisCallbackHandler(AsyncCallbackHandler):
    def publish(self, message: str) -> None:
        self.redis_client.publish(self.redis_channel, message)

    def __init__(
        self, redis_host="localhost", redis_port=6379, redis_channel="llm_stream", redis_password=None, level=0
    ):
        self.level = level
        try:
            if redis_password is not None:
                self.redis_client = redis.Redis(
                    host=redis_host, port=redis_port, db=0, password=redis_password)
            else:
                self.redis_client = redis.Redis(
                    host=redis_host, port=redis_port, db=0)
            self.redis_channel = redis_channel
        except redis.ConnectionError:
            print("Error: Could not establish a connection to Redis.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.publish(token)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent finish. Only available when streaming is enabled."""
        self.publish("AGENT_FINISH")
