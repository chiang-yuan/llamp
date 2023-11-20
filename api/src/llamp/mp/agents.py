import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
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

llm = ChatOpenAI(
    temperature=0, 
    # model='gpt-3.5-turbo-16k-0613',
    model='gpt-3.5-turbo-16k-0613',
    openai_api_key=OPENAI_API_KEY
)

tools = load_tools(["llm-math"], llm=llm)
tools += [
    MaterialsSummary(),
    MaterialsSynthesis(),
    MaterialsThermo(),
    MaterialsElasticity(),
    MaterialsMagnetism(),
    MaterialsDielectric(),
    MaterialsPiezoelectric(),
    MaterialsRobocrystallographer(),
    MaterialsOxidation(),
    MaterialsBonds(),
    MaterialsSimilarity(),
]

prompt = hub.pull("hwchase17/react-multi-input-json")
prompt = prompt.partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)

print(prompt)

llm_with_stop = llm.bind(stop=["\nObservation"])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | llm_with_stop
    | JSONAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {
        "input": "What is the most stiff materials with lowest formation energy in Si-O system? You may use different tools to get the most holistic answer."
    }
)