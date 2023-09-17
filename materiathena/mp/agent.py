import json
import os.path as osp
from pathlib import Path

import openai
from langchain.tools import OpenAPISpec
from mp_api.client import MPRester

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
    
    def fetch_materials_similarity(self, material_id: str, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.materials.get_data_by_id(
            document_id=material_id, **query_params
        )
    
    def search_materials_bonds(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.bonds._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
    
    def search_materials_eos(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")
        
        return self.mpr.eos._search(
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

    def search_materials_tasks(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.tasks._search(
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
    
    def search_materials_dielectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.dielectric._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
    
    def search_materials_piezoelectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.piezoelectric._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
    
    def search_materials_magnetism(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.magnetism._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
    
    def search_materials_elasticity(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        if "formula" in query_params:
            material_docs = self.mpr.materials.search(
                formula=query_params["formula"].split(","), 
                fields=["material_id"]
            )

            elastic_docs = []
            for doc in material_docs:
                try:
                    elastic_doc = self.mpr.elasticity.get_data_by_id(
                        document_id=doc['material_id'], fields=["pretty_formula", "elasticity", "task_id"]
                    )
                    elastic_docs.extend(elastic_doc)
                except Exception:
                    continue
            
            return elastic_docs

        return self.mpr.elasticity._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
    
    def search_materials_electronic_structure(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.electronic_structure._search(
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
            "search_materials_core__get": self.search_materials_core,
            "search_materials_summary__get": self.search_materials_summary,
            "search_materials_tasks__get": self.search_materials_tasks,
            "get_by_key_materials_similarity__material_id___get": self.fetch_materials_similarity,
            "search_materials_bonds__get": self.search_materials_bonds,
            "search_materials_eos__get" : None,
            "search_materials_thermo__get": self.search_materials_thermo,
            "search_materials_dielectric__get": self.search_materials_dielectric,
            "search_materials_piezoelectric__get": self.search_materials_piezoelectric,
            "search_materials_magnetism__get": self.search_materials_magnetism,
            "search_materials_elasticity__get": self.search_materials_elasticity,
            "search_materials_electronic_structure__get": self.search_materials_electronic_structure,
        }

    @property
    def molecule_functions(self):
        raise NotImplementedError("Molecule functions not supported yet.")

    def run_material_conversation(
        self, user_input: str, model: str = "gpt-3.5-turbo-16k-0613", debug: bool = False
    ):
        # TODO: polish system content
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a data-vigilent agent that responds user requrests based on data hosted on Materials Project."
                    "Read the response from function calls carefully and find out relevant information to respond to user requests."
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

        if debug:
            print(response)

        response_message = response["choices"][0]["message"]  # type: ignore

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
        # else:
        #     raise Exception("Failed to get response from OpenAI API.")
        
        if debug:
            print(second_response)

        return second_response
