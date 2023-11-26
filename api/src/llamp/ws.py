from langchain.agents.agent import AgentExecutor
from langchain.agents.tools import InvalidTool
from langchain.agents.agent import ExceptionTool
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    Any,
)
from langchain.tools.base import BaseTool
from langchain.schema import (
    AgentAction,
    AgentFinish,
    OutputParserException,
)
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
    Callbacks,
)


class AgentExecutorDecorator():
    def __init__(self, agent_executor: AgentExecutor):
        super().__init__()
        self._agent_executor = agent_executor

    def emit_event(self, event_type, data):
        # Implement your event emission logic here
        print(f"Emitting event: {event_type}, Data: {data}")

    def run(
        self,
        *args: Any,
        callbacks: Callbacks = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        # Emit event before running the AgentExecutor
        self.emit_event("before_run", {"args": args, "kwargs": kwargs})

        # Call the original run method of the AgentExecutor
        result = self._agent_executor.run(
            *args,
            callbacks=callbacks,
            tags=tags,
            metadata=metadata,
            **kwargs
        )

        # Emit event after running the AgentExecutor
        self.emit_event("after_run", {"result": result})

        return result

    def __getattr__(self, name):
        # Delegate attribute access to the wrapped instance
        return getattr(self._agent_executor, name)

    def _take_next_step(self, *args, **kwargs):
        # Emit event before taking the next step
        self.emit_event("before_take_next_step", {
                        "args": args, "kwargs": kwargs})

        # Call the original _take_next_step method of the AgentExecutor
        result = super()._take_next_step(*args, **kwargs)

        # Emit event after taking the next step
        self.emit_event("after_take_next_step", {"result": result})

        return result
