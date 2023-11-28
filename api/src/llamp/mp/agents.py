import os
from typing import List

from dotenv import load_dotenv
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
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description_and_args

from llamp.mp.tools import (
    MaterialsBonds,
    MaterialsDielectric,
    MaterialsElasticity,
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

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# OPENAI_GPT_MODEL = "gpt-4-1106-preview"
OPENAI_GPT_MODEL = "gpt-3.5-turbo-1106"

REACT_MULTI_JSON_PROMPT = hub.pull("hwchase17/react-multi-input-json")

class MPAgent:
    """Agent that uses the MP tools."""

    def __init__(self, llm):
        self.llm = llm
        self.chain = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
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
        return REACT_MULTI_JSON_PROMPT.partial(
            tools=render_text_description_and_args(self.tools),
            tool_names=", ".join([t.name for t in self.tools]),
        )
    
    def as_executor(
            self, 
            verbose=True,
            return_intermediate_steps=False,
            max_iterations=10,
            handle_parsing_errors=True,
            **kwargs
            ) -> AgentExecutor:
        return AgentExecutor(
            agent=self.chain, 
            tools=self.tools, 
            verbose=verbose,
            return_intermediate_steps=return_intermediate_steps,
            max_iterations=max_iterations,
            handle_parsing_errors=handle_parsing_errors,
            **kwargs
        )
    
    def as_tool(self, return_direct=True, **kwargs) -> Tool:
        return Tool.from_function(
            func=self.as_executor().run, # if use `invoke`, need to provide `input` key when calling
            name=self.name,
            description=self.description,
            return_direct=return_direct,
            **kwargs
        )

class MPThermoExpert(MPAgent):
    """Theromodynamics expert that has access to Materials Project thermo endpoint"""

    @property
    def tools(self):
        return [
            MaterialsThermo(return_direct=True, handle_tool_error=True),
        ]
    
class MPElasticityExpert(MPAgent):
    """Elasticity expert that has access to Materials Project elasticity endpoint"""

    @property
    def tools(self):
        return [
            MaterialsElasticity(return_direct=True, handle_tool_error=True),
        ]

class MPMagnetismExpert(MPAgent):
    """Magnetism expert that has access to Materials Project magnetism endpoint"""

    @property
    def tools(self):
        return [
            MaterialsMagnetism(return_direct=True, handle_tool_error=True),
        ]

class MPDielectricExpert(MPAgent):
    """Dielectric expert that has access to Materials Project dielectric endpoint"""

    @property
    def tools(self):
        return [
            MaterialsDielectric(return_direct=True, handle_tool_error=True),
        ]
    
class MPPiezoelectricExpert(MPAgent):
    """Piezoelectric expert that has access to Materials Project piezoelectric endpoint"""

    @property
    def tools(self):
        return [
            MaterialsPiezoelectric(return_direct=True, handle_tool_error=True),
        ]


    
    
    
        


# class MPAgent(BaseSingleActionAgent):
#     """Agent that uses the MP tools."""

#     @property
#     def input_keys(self):
#         return ["input"]

llm = ChatOpenAI(
    # temperature=0, 
    # model='gpt-3.5-turbo-16k-0613',
    model='gpt-4-1106-preview',
    openai_api_key=OPENAI_API_KEY
)

tools = load_tools(["llm-math"], llm=llm)
tools += [
    MaterialsSummary(handle_tool_error=True),
    MaterialsSynthesis(handle_tool_error=True),
    MaterialsThermo(handle_tool_error=True),
    MaterialsElasticity(handle_tool_error=True),
    MaterialsMagnetism(handle_tool_error=True),
    MaterialsDielectric(handle_tool_error=True),
    MaterialsPiezoelectric(handle_tool_error=True),
    MaterialsRobocrystallographer(handle_tool_error=True),
    MaterialsOxidation(handle_tool_error=True),
    MaterialsBonds(handle_tool_error=True),
    MaterialsSimilarity(handle_tool_error=True),
]

prompt = hub.pull("hwchase17/react-multi-input-json")
prompt = prompt.partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)

llm_with_stop = llm.bind(stop=["Observation"])

summarizer = load_summarize_chain(
    llm, 
    chain_type="map_reduce", 
    # max_tokens=4096
    )

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    # | summarizer
    | JSONAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {
        "input": "What is the most stiff materials with lowest formation energy in Si-O system? You may use different tools to get the most holistic answer."
    }
)