import sys
import redis

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentFinish
from typing import Any


class StreamingRedisCallbackHandler(BaseCallbackHandler):
    def __init__(self, redis_host='localhost', redis_port=6379, redis_channel='llm_stream'):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.redis_channel = redis_channel

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.redis_client.publish(self.redis_channel, token)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent finish. Only available when streaming is enabled."""
        self.redis_client.publish(self.redis_channel, "Agent finished!")
