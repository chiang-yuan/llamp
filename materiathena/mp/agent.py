import json
import os.path as osp
from pathlib import Path

import openai
from langchain.tools import OpenAPISpec
from mp_api.client import MPRester
from mp_api.client.core import BaseRester
from mp_api.client.routes import (
    MaterialsRester,
    SummaryRester,
    TaskRester,
    ThermoRester,
)

from ..utils import MP_API_KEY, OPENAI_API_KEY


class MPLLM:
    spec = OpenAPISpec.from_file(
        osp.join(Path(__file__).parent.resolve(), "mp_openapi.json")
    )

    def __init__(self, mp_api_key=MP_API_KEY, openai_api_key=OPENAI_API_KEY) -> None:
        openai.api_key = openai_api_key

        self.mpr = MPRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

        self.base = BaseRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

        self.materials = MaterialsRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

        self.thermo = ThermoRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

        self.tasks = TaskRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

        self.summary = SummaryRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )

    def search_base(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.base._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_core(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.materials._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_summary(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_thermo(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.thermo._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    @property
    def endpoints(self):
        endpoints = [
            (route, method, operation)
            for route, paths in self.spec.paths.items()
            for method, operation in paths
            if method in ["get", "post"]
        ]
        return endpoints

    @property
    def functions(self):
        functions = []
        for route, method, operation in self.endpoints:
            if operation is None:
                continue

            name = (
                operation.operationId
                if len(operation.operationId) <= 64
                else operation.operationId[:64]
            )

            description = operation.description or operation.summary

            properties = {
                property.name: {
                    "type": property.param_schema.type,
                    "description": property.description
                    if property.description is not None
                    else "",
                    **(
                        {"enum": property.param_schema.enum}
                        if property.param_schema.enum is not None
                        else {}
                    ),
                }
                for property in operation.parameters
                if property.param_schema.type is not None
            }

            required = [
                property.name for property in operation.parameters if property.required
            ]
            functions.append(
                {
                    "name": name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                    },
                    **({"required": required} if required else {}),
                }
            )

        return functions

    @property
    def material_functions(self):
        with open(
            osp.join(Path(__file__).parent.resolve(), "material_functions.json"), "r"
        ) as f:
            functions = json.load(f)
            idx = list(map(lambda x: x["name"], functions)).index(
                "search_materials_core__get"
            )
            functions.pop(idx)
            return functions

    @property
    def material_routes(self):
        return {
            # "search_base": self.search_base,
            "search_materials_thermo__get": self.search_materials_thermo,
            # "search_materials_core__get": self.search_materials_core,
            "search_materials_summary__get": self.search_materials_summary,
        }

    @property
    def molecule_functions(self):
        raise NotImplementedError("Molecule functions not supported yet.")

    def run_material_conversation(
        self, user_input: str, model: str = "gpt-3.5-turbo-16k-0613"
    ):
        # TODO: polish system content
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a data-vigilent agent that responds user requrests based on data hosted on Materials Project."
                    "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous. Only use the functions you have been provided with."
                    "You must provide `fields` or `_fields` to specify which fields to return."
                    "Pass as many arguments as possible for function calling to restrict the response to avoid timeout."
                ),
            },
            {"role": "user", "content": user_input},
        ]

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=self.material_functions,
                function_call="auto",
            )
        except Exception as e:
            print("Error:", e, "Trying again with gpt-4-32k-0613.")
            response = openai.ChatCompletion.create(
                model="gpt-4-32k-0613",
                messages=messages,
                functions=self.material_functions,
                function_call="auto",
            )
        response_message = response["choices"][0]["message"]  # type: ignore

        print(response_message)

        function_name = response_message["function_call"]["name"]
        function_to_call = self.material_routes[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(query_params=function_args)

        content = json.dumps(function_response)

        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": content,
            }
        )

        try:
            second_response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
        except Exception as e:
            print("Error:", e, "Trying again with gpt-3.5-turbo-16k-0613.")
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=messages,
            )

        return second_response
