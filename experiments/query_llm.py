import functools
import logging
import os
from enum import Enum
import traceback
from typing import Callable, Optional

import openai
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential
# import anthropic

load_dotenv()


class Model(Enum):
    "not support other LLM besides OpenAI"
    # LLAMA_2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
    # LLAMA_2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
    # LLAMA_2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"

    GPT4 = "gpt-4"  # points to gpt-4-0613
    GPT4_0314 = "gpt-4-0314"

    GPT4_TURBO = "gpt-4-1106-preview"

    GPT3_5_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT3_5_TURBO = "gpt-3.5-turbo"  #  points to gpt-3.5-turbo-0613

    # PPLX_70B_CHAT = "pplx-70b-chat"
    # MIXTRAL_8X7B_INSTRUCT = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    # DOLPHIN = "cognitivecomputations/dolphin-2.6-mixtral-8x7b"
    # CLAUDE_21 = "claude-2.1"


OPENAI_DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
# DEEPINFRA_OPENAI_ENDPOINT = "https://api.deepinfra.com/v1/openai"
# PPLX_ENDPOINT = "https://api.perplexity.ai"


# class MessageConstructor:
#     """A class that constructs messages for a given model"""

#     @classmethod
#     def construct_message(
#         cls,
#         model: Model,
#         message_content: str,
#         temperature=0,
#         max_tokens=1000,
#         **kwargs,
#     ) -> dict[str, str]:
#         """Construct a message for the given model"""
#         constructor = get_constructor(model)
#         return constructor(
#             message_content, temperature=temperature, max_tokens=max_tokens, **kwargs
#         )


# def get_constructor(model: Model) -> Callable:
#     """Get the message constructor for the given model"""
#     return functools.partial(construct_openai_message, model=model)


def construct_openai_message(
    message_content: str,
    temperature: float = 0,
    max_tokens=1000,
    system_prompt=OPENAI_DEFAULT_SYSTEM_PROMPT,
    model: Optional[Model] = None,
) -> dict[str, str]:
    """Construct a message for OpenAI's API"""
    # system prompt is only used for gpt models
    if not model:
        raise ValueError("model must be specified")
    if "gpt" in model:
        request_body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": message_content,
                },
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    else:
        request_body = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message_content,
                },
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    return request_body


# class APICaller:
#     """A class that calls the API for a given model"""

#     @classmethod
#     def call_api(cls, model: Model, request_body) -> str:
#         """Construct a message for the given model"""
#         client = get_client(model)
#         return client(request_body)


# def get_client(model: Model) -> Callable:
#     """Get the message constructor for the given model"""
#     return functools.partial(call_openai, model=model)


@retry(wait=wait_random_exponential(min=2, max=240), stop=stop_after_attempt(6))
def call_openai(request_body, model) -> dict[str, str]:
    """Call the LLM with the given message content and return the response"""
    try:
        # if model == "moderation_api":
        #     kwargs = {"api_key": os.environ["OPENAI_API_KEY"]}
        #     client = openai.OpenAI(**kwargs)
        #     response = client.moderations.create(input=request_body)
        #     content = response.results[0]
        # elif "claude" in model.value:
        #     kwargs = {"api_key": os.environ["ANTHROPIC_API_KEY"]}
        #     client = anthropic.Anthropic(**kwargs)
        #     response = client.beta.messages.create(
        #         **request_body)
        #     content = response.content[0].text
        # else: # use openai client
        if "gpt" in model:
            kwargs = {"api_key": os.environ["OPENAI_API_KEY"]}
            # elif "pplx" in model.value:
            #     kwargs = {
            #         "api_key": os.environ["PPLX_API_KEY"],
            #         "base_url": PPLX_ENDPOINT,
            #     }
            # else:
            #     kwargs = {
            #         "api_key": os.environ["DEEPINFRA_API_KEY"],
            #         "base_url": DEEPINFRA_OPENAI_ENDPOINT,
            #     }
            client = openai.OpenAI(**kwargs)
            response = client.chat.completions.create(**request_body)
            content = response.choices[0].message.content
    except Exception as e:
        # Get the string representation of the exception
        e_string = repr(e)
        logging.info(f'Exception in call_openai: {e_string}')
        # Log the stack trace
        stack_trace = traceback.format_exc()
        # Log the stack trace as a str
        logging.info(stack_trace)
        # Raise the exception again
        raise Exception(f'{e_string!r} \n\n {stack_trace}')
    return content


if __name__ == "__main__":
    # TODO: the testing script below doesn't fit the edited structure above
    with open("src/jbeval/query_messages.txt", "r") as f:
        messages = f.readlines()
    model = Model.GPT4
    responses = []
    for message in messages:
        request_body = MessageConstructor.construct_message(model, message)
        response = APICaller.call_api(model, request_body)
        responses.append(response)
    for m, r in zip(messages, responses):
        print("PROMPT:\n" + m + "\nRESPONSE:\n" + r + "\n\n")
