import os
import re
import warnings
import pandas as pd
import sys
from query_llm import construct_openai_message, call_openai
import time

# Suppress specific deprecation warning
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentType, load_tools
from langchain_experimental.tools import PythonREPLTool
from langchain.agents.initialize import initialize_agent
from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.tools.render import render_text_description_and_args
from langchain.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain.prompts import MessagesPlaceholder

# from langchain.schema import ChatMessage, SystemMessage
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

load_dotenv()
from config import PromptingConfig


def agent_setup():
    top_llm = ChatOpenAI(
    temperature=0.1,
    model=OPENAI_GPT_MODEL,
    openai_api_key=OPENAI_API_KEY,
    openai_organization=OPENAI_ORGANIZATION,
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
        streaming=True,
        callbacks=[bottom_callback_handler],
    )


    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())

    tools = load_tools(["llm-math"], llm=bottom_llm)
    tools += [PythonREPLTool()]
    tools += [
        MPSummaryExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPThermoExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPElasticityExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPDielectricExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPMagnetismExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPElectronicExpert(llm=bottom_llm).as_tool(
            agent_kwargs=dict(return_intermediate_steps=False)
        ),
        MPPiezoelectricExpert(llm=bottom_llm).as_tool(
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
    # TODO: do prompt engineering
    instructions = re.sub(
            r"\s+",
            " ",
            """You are a data-aware agent that can consult materials-related
        data through Materials Project (MP) database, arXiv, Wikipedia, and a python 
        REPL, which you can use to execute python code. If you get an error, debug 
        your code and try again. Only use the output of your code to answer the 
        question. Ask user to clarify their queries if needed. Please note that you 
        don't have direct control over MP but through multiple assistant agents to 
        help you. You need to provide complete context in the input for assistants to 
        do their job.
        """,
        ).replace("\n", " ") 
    
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    conversational_memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=5, return_messages=True
    )

    agent = create_react_agent(top_llm, tools, prompt)

    return tools, top_llm, conversational_memory, agent

    
def agent_prompting(prompt):
    tools, top_llm, conversational_memory, agent = agent_setup()
    
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True,
        handle_parsing_errors=True,
        memory=conversational_memory,
    )


    llamp_response = agent_executor.invoke({"input": prompt,})["output"]
    print("llamp_response", llamp_response)


    # Define the ChatGPT agent
    llm_gpt = ChatOpenAI(
        temperature=0.7,
        # model="gpt-3.5-turbo-1106",
        model=PromptingConfig().gpt_model,
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
        " Ferromag": "FM",
        " Ferrimag": "FiM",
        "Antiferromag": "AFM",
        "Anti-ferromag": "AFM",
        "non-mag": "NM",
    }
    # {'FiM', 'Unknown', 'NM', 'FM', None, 'AFM'}
    for key, value in categories.items():
        if key.lower() in ordering.lower():
            return value
    return None

def llm_eval(response, config):
    """LLM Evalluator"""
    try: 
        message_content = config.eval_prompt[config.task] + response
    except: 
        print("Config task number and eval_prompt mismatch")

    request_body = construct_openai_message(
            message_content,
            temperature=0.5,
            max_tokens=1000,
            model=EVALUATOR_MODEL,
        )
    
    value = call_openai(request_body, EVALUATOR_MODEL)

    return value

def save_in_csv(csv_path, prompt, llamp_response, gpt_response, config):
    df = pd.read_csv(csv_path)
    llamp_output = llamp_response
    llamp_output = llamp_output["action_input"] if isinstance(llamp_output, dict) and "action_input" in llamp_output else llamp_output
    gpt_output = gpt_response if isinstance(gpt_response, str) else gpt_response.content

    llamp_value = llm_eval(llamp_output, config)
    gpt_value = llm_eval(gpt_output, config)
    llamp_value = eval(llamp_value)
    gpt_value = eval(gpt_value) 

    # Find the index of the row with the matching prompt
    row_index = df.index[df['prompt'] == prompt].tolist()
    if row_index:
        row_index = row_index[0]
        df.at[row_index, 'llamp_output'] = llamp_output
        df.at[row_index, 'gpt_output'] = gpt_output
        # Update the existing row with new information
        if config.task == 6:
            df.at[row_index, 'llamp_magnetic_ordering'] = llamp_value["magnetic_ordering"]
            df.at[row_index, 'llamp_mp_id'] = llamp_value["material_id"]
            df.at[row_index, 'llamp_magnetization_unit'] = llamp_value["total_magnetization_normalized_formula_units"]
            df.at[row_index, 'gpt_magnetic_ordering'] = gpt_value["magnetic_ordering"]
            df.at[row_index, 'gpt_mp_id'] = gpt_value["material_id"]
            df.at[row_index, 'gpt_magnetization_unit'] = gpt_value["total_magnetization_normalized_formula_units"]
        elif config.task == 7:
            df.at[row_index, 'llamp_volume'] = llamp_value["volume"]
            df.at[row_index, 'llamp_density'] = llamp_value["mass_density"]
            df.at[row_index, 'gpt_volume'] = gpt_value["volume"]
            df.at[row_index, 'gpt_density'] = gpt_value["mass_density"]
        else:
            raise NotImplementedError("This task hasn't been implemented yet.")
    else:
        print("Prompt not found in the DataFrame. No row updated.")
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # load the config
    config = PromptingConfig()
    assert config.task in config.eval_prompt.keys() 

    # TODO: Setting up the API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
    OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION", None)
    MP_API_KEY = os.getenv("MP_API_KEY", None)



    OPENAI_GPT_MODEL = config.gpt_model
    EVALUATOR_MODEL = config.evaluator_model
    
    # New prompting pipeline
    csv_path = config.csv_path

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        print("File not found. Creating a new one with basic structure.")

    starting_index = 997 #TODO: find a way to print out the stopping index from the pipeline
    # Iterate over the DataFrame rows
    for index, row in df.iterrows():
        if index < starting_index:
            continue
        start_time = time.time()
        prompt = row['prompt']

        # Try 3 times to
        attempt = 0
        # for attempt in range(1):  # Allows up to 3 attempts
        try:
            llamp_response, gpt_response = agent_prompting(prompt)

            # Testing script below: 
            # llamp_response, gpt_response = {"output":"The compound PmPd2Pb has a non-magnetic (NM) ordering. It crystallizes in the cubic Fm-3m space group (number 225) with a final magnetic moment of 0.001 μB per formula unit. This information is based on data from the Materials Project with the material ID mp-862950"},\
            #       "The compound PmPd2Pb has a non-magnetic (NM) ordering. It crystallizes in the cubic Fm-3m space group (number 225) with a final magnetic moment of 0.001 μB per formula unit. This information is based on data from the Materials Project with the material ID mp-862950" #Testing script

            save_in_csv(csv_path, prompt, llamp_response, gpt_response, config)
            print(f"prompt {index} finish")
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Total execution time: {total_time} seconds, prompt: {prompt}")
            # break  # Exit loop on success

        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e} with index {index}", flush=True)
            error_message = str(e)
            if "Error code:" in error_message:
                print(f"Attempt {attempt + 1}: Error received. Waiting for 1 minute before retrying with index {index}", flush=True)
                # time.sleep(200)  # Wait for 10 minutes for the openai request issue
                break
                print("Finish sleep")
            if attempt == 2:  # Last attempt
                print("Final attempt failed. Moving to next prompt.")
            continue
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total execution time: {total_time} seconds, prompt: {prompt} with index {index}")
        if total_time > 600:
            print("Operation Time Out")
            break

print(f"#################################################### Finish Prompting #######################################################")

