import os
import re
import warnings
import pandas as pd
import sys
from query_llm import construct_openai_message, call_openai

# Suppress specific deprecation warning
warnings.filterwarnings("ignore")

# from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, AgentType, load_tools
from langchain.agents.initialize import initialize_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.tools import ArxivQueryRun, WikipediaQueryRun, tool
from langchain.tools.render import render_text_description_and_args
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain.prompts import MessagesPlaceholder
from langchain.schema import ChatMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager


from llamp.mp.agents import (
    MPSummaryExpert,
    MPThermoExpert,
    MPElasticityExpert,
    MPDielectricExpert,
    MPPiezoelectricExpert,
    MPMagnetismExpert,
    MPElectronicExpert,
    MPSynthesisExpert,
    MPStructureRetriever,
)
from llamp.arxiv.agents import ArxivAgent

# load_dotenv()

def agent_setup():
    top_llm = ChatOpenAI(
        temperature=0.1,
        model=OPENAI_GPT_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_organization=OPENAI_ORGANIZATION,
        # streaming=True,
        streaming=False,
        callbacks=[StreamingStdOutCallbackHandler()],
    )

    bottom_callback_handler = StreamingStdOutCallbackHandler()

    bottom_llm = ChatOpenAI(
        temperature=0,
        model=OPENAI_GPT_MODEL,
        openai_api_key=OPENAI_API_KEY,
        openai_organization=OPENAI_ORGANIZATION,
        max_retries=5,
        # streaming=True,
        streaming=False,
        callbacks=[bottom_callback_handler],
    )


    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())


    tools = [
        # TODO: fix the error out here
        MPThermoExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        # TODO: failing agent: ValidationError: 1 validation error for ChainInputSchema input field required (type=value_error.missing)
        # MPElasticityExpert(llm=bottom_llm).as_tool(
        #     agent_kwargs=dict(return_intermediate_steps=False)
        # ),
        MPDielectricExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPMagnetismExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPElectronicExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),

        # # TODO: possible failing agent
        MPPiezoelectricExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        #pydantic_core._pydantic_core.ValidationError: 1 validation error for PiezoSchema fields
        # haven't test
        MPSummaryExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPSynthesisExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPStructureRetriever(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        # ArxivAgent(llm=bottom_llm).as_tool(agent_kwargs=dict(return_intermediate_steps=False)),
        arxiv,
        wikipedia,
    ]
    tools += load_tools(["llm-math"], llm=bottom_llm)

    # Define the prompt for the agent
    prompt = hub.pull("hwchase17/react-multi-input-json")
    prompt.messages[0].prompt.template = (
        re.sub(
            r"\s+",
            " ",
            """You are a data-aware agent that can consult materials-related
        data through Materials Project (MP) database, arXiv, and Wikipedia. Ask 
        user to clarify their queries if needed. Please note that you don't have 
        direct control over MP but through multiple assistant agents to help you. 
        You need to provide complete context in the input for them to do their job.
        """,
        ).replace("\n", " ")
        + prompt.messages[0].prompt.template
    )

    prompt = prompt.partial(
        tools=render_text_description_and_args(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        }
        | prompt
        | top_llm.bind(stop=["Observation"])
        # | map_reduce_chain  # TODO: Add map-reduce after LLM
        | JSONAgentOutputParser()
    )

    conversational_memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=5, return_messages=True
    )

    agent_kwargs = {
        "handle_parsing_errors": True,
        "extra_prompt_messages": [
            MessagesPlaceholder(variable_name="chat_history"),
        ],
        "early_stopping_method": "generate",
    }

    return tools, top_llm, conversational_memory, agent_kwargs, bottom_callback_handler

    
def agent_prompting(prompt):
    tools, top_llm, conversational_memory, agent_kwargs, bottom_callback_handler = agent_setup()

    agent_executor = initialize_agent(
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=top_llm,
        verbose=True,
        max_iterations=20,
        memory=conversational_memory,
        agent_kwargs=agent_kwargs,
        handle_parsing_errors=True,
        callback_manager=BaseCallbackManager(handlers=[bottom_callback_handler]),
    )

    llamp_response = agent_executor.invoke({"input": prompt,})
    print("llamp_response", llamp_response)

    # Define the ChatGPT agent
    llm_gpt = ChatOpenAI(
        temperature=0.7,
        model="gpt-3.5-turbo-1106",
        openai_api_key=OPENAI_API_KEY,
        openai_organization=OPENAI_ORGANIZATION,
        # streaming=Truen
    )

    # lenght 2 stores the human input and AIM message for agent_executor.memory.chat_memory.messages
    gpt_response = llm_gpt.invoke(agent_executor.memory.chat_memory.messages[0].content)
    print("gpt_response", gpt_response)

    return llamp_response, gpt_response


# create the pipeline to do evaluation
def categorize_magnetic_ordering(ordering):
    """String Matching Evalluator"""
    categories = {
        # "Diamag": "Diamagnetism",
        # "Paramag": "Paramagnetism",
        " Ferromag": "FM",
        " Ferrimag": "FiM",
        "Antiferromag": "AFM",
        "Anti-ferromag": "AFM",
        "non-mag": "NM",
        # "Superparamag":"Superparamagnetism",
        # "Nagaoka mag": "Nagaoka magnetism"
    }
    # {'FiM', 'Unknown', 'NM', 'FM', None, 'AFM'}
    for key, value in categories.items():
        if key.lower() in ordering.lower():
            return value
    return None

def llm_categorize_magnetic_ordering(response):
    """LLM Evalluator"""
    message_content = """You are a data-aware agent that can extract the material-related information.

    You don't need to add your interpretation and don't correct the wrong information even if you know that's wrong.

    In the following task, you are required to extract the magnetic ordering, total magnetization normalized formula units, and material_id, which starts with mp-XXX.

    After you reasong through the response and extract the magnetic ordering, total magnetization normalized formula units, and material_id,
    please output it in the format of python dictionary below

    {
    "magnetic_ordering": [extracted information],
    "total_magnetization_normalized_formula_units": [extracted information],
    "material_id": [extracted information]
    }

    Tip: 
    1. for magnetic_ordering, make sure the [extracted information] be acronym in the set: {'FiM', 'Unknown', 'NM', 'FM', 'AFM'}
    2. convert total_magnetization_normalized_formula_units's unit as μB and only include the number in the dictionary.
    3. if the response doesn't include the information you need to extract, put "N/A" string as [extracted information] for that

    Below is the response you need to extract the information specified above:

    Response: """ + response

    request_body = construct_openai_message(
            message_content,
            temperature=0.5,
            max_tokens=1000,
            model=EVALUATOR_MODEL,
        )
    
    value = call_openai(request_body, EVALUATOR_MODEL)

    return value

def save_in_csv(csv_path, prompt, llamp_response, gpt_response):
    df = pd.read_csv(csv_path)
    new_row = {
        'llamp_output': llamp_response["output"],
        'gpt_output': gpt_response if isinstance(gpt_response, str) else gpt_response.content
    }

    llamp_value = llm_categorize_magnetic_ordering(new_row['llamp_output'])
    gpt_value = llm_categorize_magnetic_ordering(new_row['gpt_output'])
    
    try:
        llamp_value = eval(llamp_value)
        gpt_value = eval(gpt_value)
    except Exception as e:
        print(f"Error {e}, the format is not in python dictionary output.")

    # Find the index of the row with the matching prompt
    row_index = df.index[df['prompt'] == prompt].tolist()
    if row_index:
        row_index = row_index[0]
        # Update the existing row with new information
        df.at[row_index, 'llamp_output'] = llamp_response["output"]
        df.at[row_index, 'gpt_output'] = gpt_response if isinstance(gpt_response, str) else gpt_response.content
        df.at[row_index, 'llamp_magnetic_ordering'] = llamp_value["magnetic_ordering"]
        df.at[row_index, 'llamp_mp_id'] = llamp_value["material_id"]
        df.at[row_index, 'llamp_magnetization_unit'] = llamp_value["total_magnetization_normalized_formula_units"]
        df.at[row_index, 'gpt_magnetic_ordering'] = gpt_value["magnetic_ordering"]
        df.at[row_index, 'gpt_mp_id'] = gpt_value["material_id"]
        df.at[row_index, 'gpt_magnetization_unit'] = gpt_value["total_magnetization_normalized_formula_units"]
    else:
        print("Prompt not found in the DataFrame. No row updated.")
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # TODO: Setting up the API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION", None)
    MP_API_KEY = os.getenv("MP_API_KEY", None)

    # Setting the os vision so that other files can execute correctly
    os.environ['MP_API_KEY'] = MP_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.environ['OPENAI_ORGANIZATION'] = OPENAI_ORGANIZATION

    # OPENAI_GPT_MODEL = "gpt-4-1106-preview"
     # OPENAI_GPT_MODEL = "gpt-4"
    OPENAI_GPT_MODEL = "gpt-3.5-turbo-1106"
    EVALUATOR_MODEL = OPENAI_GPT_MODEL
    
    # New prompting pipeline
    csv_path = "cache/small_test_dataset.csv"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        print("File not found. Creating a new one with basic structure.")

    # Iterate over the DataFrame rows
    count = 0
    for index, row in df.iterrows():
        prompt = row['prompt']
    
        # Try 3 times to
        for attempt in range(3):  # Allows up to 3 attempts
            try:
                llamp_response, gpt_response = agent_prompting(prompt)
                # llamp_response, gpt_response = {"output":"The compound PmPd2Pb has a non-magnetic (NM) ordering. It crystallizes in the cubic Fm-3m space group (number 225) with a final magnetic moment of 0.001 μB per formula unit. This information is based on data from the Materials Project with the material ID mp-862950"},\
                #       "The compound PmPd2Pb has a non-magnetic (NM) ordering. It crystallizes in the cubic Fm-3m space group (number 225) with a final magnetic moment of 0.001 μB per formula unit. This information is based on data from the Materials Project with the material ID mp-862950" #Testing script

                save_in_csv(csv_path, prompt, llamp_response, gpt_response)
                count+= 1
                print(f"prompt {index} finish")
                break  # Exit loop on success

            except Exception as e:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt == 2:  # Last attempt
                    print("Final attempt failed. Moving to next prompt.")
                continue
        count = 0

print(f"#################################################### Finish Prompting #######################################################")
