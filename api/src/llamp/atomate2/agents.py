import re

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.tools import StructuredTool, Tool
from langchain.tools.render import render_text_description_and_args
from langchain.pydantic_v1 import BaseModel, Field

from llamp.atomate2.tools import MLFFMD

REACT_MULTI_JSON_PROMPT = hub.pull("hwchase17/react-multi-input-json")


class ChainInputSchema(BaseModel):
    input: str = Field(
        ...,
        description="Complete question to ask the assistant agent. Should include all the context and details needed to answer the question holistically.",
    )


class Atomate2Agent:
    """Agent that use atomate2 (automated computational materials workflows)."""

    def __init__(self, llm) -> None:
        self.llm = llm
        self.chain = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"],
                ),
            }
            | self.prompt
            | self.llm.bind(stop=["Observation"])
            | JSONAgentOutputParser()
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def description(self) -> str:
        return self.__doc__

    @property
    def tools(self) -> list[Tool]:
        raise NotImplementedError

    @property
    def prompt(self):
        partial_prompt = REACT_MULTI_JSON_PROMPT.partial(
            tools=render_text_description_and_args(self.tools),
            tool_names=", ".join([t.name for t in self.tools]),
        )
        partial_prompt.messages[0].prompt.template = (
            re.sub(
                r"\s+",
                " ",
                f"""You are a helpful assistant called {self.name} able to call and
                orchestrate atomate2 computational simulation workflow.

                IMPORTANT: 
                - When you create function input arguments, ALWAYS follow the schema s
                trictly and DO NOT hallucinate invalid arguments
                - Convert ALL acronyms and abbreviations to valid arguments, especially 
                chemical formula and isotopes (e.g. D2O should be H2O), composition, 
                and chemical systems
                - You can refuse to answer questions that are out of scope or ask your
                human user or supervisor agent for clarification if the question is 
                unclear
                - Summarize the results without losing the necessary details based on
                the context and question asked
                """,
            )
            + partial_prompt.messages[0].prompt.template
        )
        return partial_prompt

    def as_executor(
        self,
        verbose=True,
        return_intermediate_steps=False,
        max_iterations=5,
        handle_parsing_errors=True,
        **kwargs,
    ) -> AgentExecutor:
        return AgentExecutor(
            agent=self.chain,
            tools=self.tools,
            verbose=verbose,
            return_intermediate_steps=return_intermediate_steps,
            max_iterations=max_iterations,
            handle_parsing_errors=handle_parsing_errors,
            **kwargs,
        )

    def as_tool(
        self,
        return_direct=False,
        agent_kwargs={},
        tool_kwargs={},
    ) -> Tool:
        def run(input: str):
            return self.as_executor(**agent_kwargs).invoke(
                {
                    "input": input,
                },
            )

        return StructuredTool.from_function(
            func=run,
            name=self.name,
            description=self.description,
            return_direct=return_direct,
            args_schema=ChainInputSchema,
            **tool_kwargs,
        )
    
class MLFFMDAgent(Atomate2Agent):
    """Agent that runs MLFF MD simulation using atomate2."""
    
    @property
    def tools(self):
        return [
            MLFFMD(
                return_direct=False,
                handle_tool_error=True,
            ),
        ]
