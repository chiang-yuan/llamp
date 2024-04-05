import ast
import json
import re
from typing import Any, Optional
from uuid import UUID

from langchain import hub
from langchain.agents import (
    AgentExecutor,
)
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool, Tool
from langchain.tools.render import render_text_description_and_args
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import LLM
from langchain_core.prompts import ChatPromptTemplate

from llamp.mp.schemas import SynthesisRecipe

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
    MaterialsStructureText,
    MaterialsStructureVis,
    MaterialsSummary,
    MaterialsSynthesis,
    MaterialsTasks,
    MaterialsThermo,
)

REACT_MULTI_JSON_PROMPT = hub.pull("hwchase17/react-multi-input-json")


class ChainInputSchema(BaseModel):
    input: str = Field(
        ...,
        description="Complete question to ask the assistatn agent. Should include all the context and details needed to answer the question holistically.",
    )
    # agent_scratchpad: str = ""


class MPAgent:
    """Agent that uses the MP tools."""

    def __init__(self, llm, mp_api_key=None):
        self.llm = llm
        self.mp_api_key = mp_api_key
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
                f"""You are a helpful assitent called {self.name} having access to 
                materials data on Materials Project (MP). DO NOT be overconfident and 
                request related MP API endpoint whenever possible. When you create 
                function input arguments, ALWAYS follow MP API schema strictcly and 
                DO NOT hallucinate invalid arguments. Convert ALL acronyms and 
                abbreviations to valid arguments, especially chemical formula and 
                isotopes (e.g. D2O should be H2O), composition, and systems.""",
            ).replace("\n", " ")
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
                }
            )

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

    @property
    def tools(self):
        return [
            MaterialsSummary(return_direct=False, handle_tool_error=True),
        ]


class MPStructureRetriever(MPAgent):
    """Structure expert who will retrieve the structure from Materials Project as a JSON text or save it to a local file for frontend visualization"""

    @property
    def tools(self):
        return [
            MaterialsStructureText(return_direct=True, handle_tool_error=True),
            # MaterialsStructureVis(return_direct=True, handle_tool_error=True),
        ]


class MPStructureVisualizer(MPAgent):
    """Structure expert who will retrieve the structure from Materials Project, save it to local storage for frontend visualization"""
    chat_id: str = ""

    def __init__(self, llm, chat_id, mp_api_key=None):
        super().__init__(llm, mp_api_key=mp_api_key)
        self.chat_id = chat_id

    @property
    def tools(self):
        return [
            # MaterialsStructureVis(return_direct=True, handle_tool_error=True),
            MaterialsStructureVis(return_direct=False,
                                  handle_tool_error=True,
                                  chat_id=self.chat_id),
        ]


class MPThermoExpert(MPAgent):
    """Theromodynamics expert that has access to Materials Project thermo endpoint"""

    @property
    def tools(self):
        return [
            MaterialsThermo(return_direct=False, handle_tool_error=True),
        ]


class MPElasticityExpert(MPAgent):
    """Elasticity expert that has access to Materials Project elasticity endpoint, including bulk, shear, and young's modulus, poisson ratio, and universal anisotropy index"""

    @property
    def tools(self):
        return [
            MaterialsElasticity(return_direct=False, handle_tool_error=True),
        ]


class MPMagnetismExpert(MPAgent):
    """Magnetism expert that has access to Materials Project magnetism endpoint"""

    @property
    def tools(self):
        return [
            MaterialsMagnetism(return_direct=False, handle_tool_error=True),
        ]


class MPDielectricExpert(MPAgent):
    """Dielectric expert that has access to Materials Project dielectric endpoint"""

    @property
    def tools(self):
        return [
            MaterialsDielectric(return_direct=False, handle_tool_error=True),
        ]


class MPPiezoelectricExpert(MPAgent):
    """Piezoelectric expert that has access to Materials Project piezoelectric endpoint"""

    @property
    def tools(self):
        return [
            MaterialsPiezoelectric(return_direct=False,
                                   handle_tool_error=True),
        ]


class MPElectronicExpert(MPAgent):
    """Electronic expert that has access to Materials Project electronic endpoint"""

    @property
    def tools(self):
        return [
            MaterialsElectronic(return_direct=False, handle_tool_error=True),
        ]


class SyntheisCallbackHandler(BaseCallbackHandler):

    def __init__(self, llm):
        super().__init__()
        self.llm: LLM = llm

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", re.sub(
                        r"\s+", " ", """You are a summarizer agent that proceses a 
                        batch of synthesis recipes. You should summarize the synthesis 
                        recipes in a concise and informativeformat that conforms the 
                        output schema."""
                    ).strip().replace("\n", " ")
                ),
                (
                    "assistant", "here are the synthesis recipes from MP: {input}"
                )
            ]
        )

        self.extractor = self.prompt | self.llm.with_structured_output(
            schema=SynthesisRecipe,
            include_raw=False
        )

    def on_tool_end(self,
                    output: Any,
                    *,
                    run_id: UUID,
                    parent_run_id: UUID | None = None,
                    **kwargs: Any) -> Any:

        # output = json.loads(output)
        output = ast.literal_eval(output)
        print("on_tool_end:", type(output), len(output), output)
        return self.extractor.batch(
            [{"input": recipe} for recipe in output],
            {"max_concurrency": 100},
        )


class MPSynthesisExpert(MPAgent):
    """Materials synthesis expert that has access to Materials Project synthesis
    endpoint, where synthesis recipes are extracted  from scientific literature through
    text mining and natural language processing approaches"""

    @property
    def tools(self):
        return [
            MaterialsSynthesis(
                return_direct=False, handle_tool_error=True,
                # callbacks=[SyntheisCallbackHandler(llm=self.llm)]
            ),
        ]
