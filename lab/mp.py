import json
import os

import openai
from dotenv import load_dotenv
from mp_api.client import MPRester

from langchain.tools import APIOperation, OpenAPISpec

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
MP_API_KEY = os.getenv("MP_API_KEY", None)
openai.api_key = OPENAI_API_KEY

# from langchain.chains import OpenAPIEndpointChain
# from langchain.requests import Requests
# from langchain.llms import OpenAI
# from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec


spec = OpenAPISpec.from_url("https://api.materialsproject.org/openapi.json")

operation = APIOperation.from_openapi_spec(
    spec, "/materials/summary/{material_id}/", "get"
)

print(operation)

# from langchain.chat_models import ChatOpenAI, ChatAnthropic
# from langchain.schema import HumanMessage, AIMessage, ChatMessage
# from langchain.tools import format_tool_to_openai_function

# llm = ChatAnthropic(anthropic_api_key=)

# llm = ChatOpenAI(model='gpt-4-0613', temperature=0.5, openai_api_key=OPENAI_API_KEY, client=)


class LLMaterialsAgent:
    def __init__(self, mp_api_key=MP_API_KEY, openai_api_key=OPENAI_API_KEY):
        # Initialize the Materials Project API
        self.mpr = MPRester(mp_api_key)
        # Initialize the OpenAI API
        openai.api_key = openai_api_key

    def get_materials_data(self, query_params):
        # Retrieve data from the Materials Project using the MPRester class
        data = self.mpr.summary.search(**query_params)
        return data

    def run_conversation(self, user_input):
        # Step 1: send the conversation and available functions to GPT
        messages = [{"role": "user", "content": user_input}]
        functions = [
            {
                "name": "get_materials_data",
                "description": "Get materials data from the Materials Project",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "elements": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Elements to query, e.g., ['Si', 'O']",
                        },
                        "band_gap": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Range of band gap values, e.g., [0.5, 1.0]",
                        },
                        # "limit": {
                        #     "type": "integer",
                        #     "description": "Number of materials to retrieve, e.g., 5",
                        # },
                    },
                    "required": ["elements", "band_gap"],
                },
            }
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]

        # Step 2: check if GPT wanted to call a function
        if response_message.get("function_call"):
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_materials_data": self.get_materials_data,
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(query_params=function_args)

            breakpoint()

            # Step 4: send the info on the function call and function response to GPT
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            breakpoint()
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    # "content": json.dumps(function_response[0]),
                    "content": function_response,
                }
            )  # extend conversation with function response
            breakpoint()
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )  # get a new response from GPT where it can see the function response
            breakpoint()
            return second_response


# Set up the Materials Project API key and OpenAI API key
mp_api_key = MP_API_KEY
openai_api_key = OPENAI_API_KEY

if __name__ == "__main__":
    # Instantiate the LLMaterialsAgent class
    ll_agent = LLMaterialsAgent()

    # Get user input
    user_input = input("Please enter your natural language query: ")

    # Run the conversation with GPT-3.5-turbo model using the user input
    print(ll_agent.run_conversation(user_input))
