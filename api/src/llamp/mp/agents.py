import os
import re

from langchain import hub
from langchain.agents import (
    AgentExecutor,
    AgentType,
    BaseSingleActionAgent,
    Tool,
    initialize_agent,
    load_tools,
)
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.agents.schema import AgentAction
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool, Tool, tool
from langchain.tools.render import render_text_description_and_args

from llamp.mp.tools import (
    MaterialsBonds,
    MaterialsDielectric,
    MaterialsElasticity,
    MaterialsElectronic,
    MaterialsMagnetism,
    MaterialsOxidation,
    MaterialsPiezoelectric,
    MaterialsRobocrystallographer,
    MaterialsSimilarity,
    MaterialsStructure,
    MaterialsSummary,
    MaterialsSynthesis,
    MaterialsTasks,
    MaterialsThermo,
)

REACT_MULTI_JSON_PROMPT = hub.pull("hwchase17/react-multi-input-json")

class ChainInputSchema(BaseModel):
    input: str = Field(..., description="Complete question to ask the assistatn agent. Should include all the context and details needed to answer the question holistically.")
    # agent_scratchpad: str = ""

class MPAgent:
    """Agent that uses the MP tools."""

    def __init__(self, llm):
        self.llm = llm
        # self.summary_chain = load_summarize_chain(self.llm, chain_type="map_reduce", verbose=True)
        self.chain = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"]
                ),
            }
            | self.prompt
            | self.llm.bind(stop=["Observation"])
            # TODO: add a summarizer to take care of large reponses
            # | ReActSingleInputOutputParser()
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
        partial_prompt.messages[0].prompt.template = re.sub(
                r"\s+", " ",
                f"""You are a helpful agent called {self.name} having access to 
                materials data on Materials Project. When you create function input 
                arguments, follow MP API schema strictcly and DO NOT hallucinate 
                invalid arguments. Convert all acronyms and abbreviations to valid 
                arguments, especially chemical formula and isotopes (e.g. D2O should be 
                H2O), composition, and systems. """
            ).replace("\n", " ") + partial_prompt.messages[0].prompt.template
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
            return self.as_executor(**agent_kwargs).invoke({
                "input": input,
            })
        
        return StructuredTool.from_function(
            func=run,
            name=self.name,
            description=self.description,
            return_direct=return_direct,
            args_schema=ChainInputSchema,
            **tool_kwargs,
        )


class MPSummaryExpert(MPAgent):
    """Summary expert that has access to Materials Project summary endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsSummary(return_direct=False, handle_tool_error=True),
        ]

class MPThermoExpert(MPAgent):
    """Theromodynamics expert that has access to Materials Project thermo endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsThermo(return_direct=False, handle_tool_error=True),
        ]


class MPElasticityExpert(MPAgent):
    """Elasticity expert that has access to Materials Project elasticity endpoint, including bulk, shear, and young's modulus, poisson ratio, and universal anisotropy index"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsElasticity(return_direct=False, handle_tool_error=True),
        ]


class MPMagnetismExpert(MPAgent):
    """Magnetism expert that has access to Materials Project magnetism endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsMagnetism(return_direct=False, handle_tool_error=True),
        ]


class MPDielectricExpert(MPAgent):
    """Dielectric expert that has access to Materials Project dielectric endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsDielectric(return_direct=False, handle_tool_error=True),
        ]


class MPPiezoelectricExpert(MPAgent):
    """Piezoelectric expert that has access to Materials Project piezoelectric endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsPiezoelectric(return_direct=False, handle_tool_error=True),
        ]
    
class MPElectronicExpert(MPAgent):
    """Electronic expert that has access to Materials Project electronic endpoint"""

    def __init__(self, llm):
        super().__init__(llm)

    @property
    def tools(self):
        return [
            MaterialsElectronic(return_direct=False, handle_tool_error=True),
        ]