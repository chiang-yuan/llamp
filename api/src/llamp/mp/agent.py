import json
import os.path as osp
import re
import time
from pathlib import Path

import openai
from langchain.tools import OpenAPISpec
from mp_api.client import MPRester

from ..utils import MP_API_KEY, OPENAI_API_KEY


class MPLLM:
    spec = OpenAPISpec.from_file(
        osp.join(Path(__file__).parent.resolve(), "mp_openapi.json")
    )
    def __init__(
        self,
        mp_api_key=MP_API_KEY,
        openai_api_key=OPENAI_API_KEY,
        max_tokens: int = 4096,
    ) -> None:
        openai.api_key = openai_api_key

        self.mpr = MPRester(
            api_key=mp_api_key, monty_decode=False, use_document_model=False
        )
        self.max_tokens = max_tokens
        self._messages: list[dict[str, str]] = []

    def search_materials_core(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.materials._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
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
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_eos(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.eos._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_summary(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_robocrys(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")
        return self.mpr.robocrys._search(
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
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_thermo(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.thermo._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_dielectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.dielectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_piezoelectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.piezoelectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_magnetism(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        if "formula" in query_params:
            material_docs = self.mpr.materials.search(
                formula=query_params.pop("formula").split(","), fields=["material_id"]
            )

            material_ids = [doc["material_id"] for doc in material_docs]

            # return self.mpr.magnetism._search(
            #     num_chunks=None, chunk_size=1000, all_fields=True,
            #     material_ids=material_ids,
            #     **query_params
            # )

            return self.mpr.magnetism.search(
                material_ids=material_ids,
                fields=[
                    "material_id",
                    "formula_pretty",
                    "ordering",
                    "is_magnetic",
                    "exchange_symmetry",
                    "num_magnetic_sites",
                    "num_unique_magnetic_sites",
                    "types_of_magnetic_species",
                    "magmoms",
                    "total_magnetization",
                    "total_magnetization_normalized_vol",
                    "total_magnetization_normalized_formula_units",
                ],
            )

        return self.mpr.magnetism._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
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
                formula=query_params["formula"].split(","), fields=["material_id"]
            )

            elastic_docs = []
            for doc in material_docs:
                try:
                    elastic_doc = self.mpr.elasticity.get_data_by_id(
                        document_id=doc["material_id"],
                        fields=["pretty_formula", "elasticity", "task_id"],
                    )
                    elastic_docs.extend(elastic_doc)
                except Exception:
                    continue

            return elastic_docs

        return self.mpr.elasticity._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_electronic_structure(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get("fields", []) + _fields.split(",")

        return self.mpr.electronic_structure._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
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
            # NOTE: Using all functions available on MP consumes too many tokens.
            # Here we only use a subset of functions.
            # functions = self.functions
            functions = json.load(f)
            idx = list(map(lambda x: x["name"], functions)).index(
                "search_materials_core__get"
            )
            functions.pop(idx)
            return functions

    @property
    def material_routes(self):
        return {
            # "search_materials_core_formula_autocomplete__get": self.search_materials_core,
            # "search_materials_core__get": self.search_materials_core,
            "search_materials_absorption__get": None,
            "search_materials_bonds__get": self.search_materials_bonds,
            "search_materials_chemenv__get": None,
            "search_materials_tasks_trajectory__get": None,
            "search_materials_tasks__get": self.search_materials_tasks,
            "get_by_key_materials_thermo_phase_diagram__phase_diagram_id___get": None,
            "search_materials_thermo__get": self.search_materials_thermo,
            "search_materials_dielectric__get": self.search_materials_dielectric,
            "search_materials_piezoelectric__get": self.search_materials_piezoelectric,
            "search_materials_magnetism__get": self.search_materials_magnetism,
            "get_by_key_materials_phonon__material_id___get": None,
            "search_materials_eos__get": None,
            "get_by_key_materials_eos__task_id___get": None,
            "get_by_key_materials_similarity__material_id___get": self.fetch_materials_similarity,
            "search_materials_xas__get": None,
            "search_materials_grain_boundary__get": None,
            "get_by_key_materials_fermi__task_id___get": None,
            "get_by_key_materials_elasticity__task_id___get": None,
            "search_materials_elasticity__get": self.search_materials_elasticity,
            "search_materials_substrates__get": None,
            "search_materials_surface_properties__get": None,
            "search_materials_robocrys_text_search__get": None,
            "search_materials_robocrys__get": self.search_materials_robocrys,
            "search_materials_insertion_electrodes__get": None,
            "search_materials_oxidation_states__get": None,
            "search_materials_alloys__get": None,
            "search_materials_provenance__get": None,
            "search_materials_charge_density__get": None,
            "get_by_key_materials_charge_density__fs_id___get": None,
            "search_materials_summary_stats__get": None,
            "search_materials_summary__get": self.search_materials_summary,
            "search_materials_electronic_structure_bandstructure__get": None,
            "search_materials_electronic_structure_dos__get": None,
            "search_materials_electronic_structure__get": self.search_materials_electronic_structure,
            "search_materials_electronic_structure_bandstructure_object__get": None,
            "search_materials_electronic_structure_dos_object__get": None,
        }

    @property
    def molecule_functions(self):
        raise NotImplementedError("Molecule functions not supported yet.")

    @property
    def messages(self) -> list[dict[str, str]]:
        return self._messages

    def trim_messages(self):
        total_tokens = sum(len(message["content"].split()) for message in self.messages)
        while total_tokens > self.max_tokens:
            oldest_message = self.messages.pop(0)
            total_tokens -= len(oldest_message["content"].split())

    def general_reponse(self, message: dict[str, str], model="gpt-3.5-turbo-0613"):

        if message["role"] != "function":
            self.messages.append(message)
            self.trim_messages()

        messages = [
            {
                "role": "system",
                "content": re.sub(
                    r"\s+",
                    " ",
                    """You are a data-vigilant agent that decide whether to call 
                    Materials Project API for expert-curated data, and answer user 
                    requests based on the data retrieved and information in the 
                    conversation history below.""",
                ).strip().replace('\n', ' ')
            },
            *self.messages,
        ]

        if message["role"] == "function":
            messages.append(message)
        else:
            messages.append({
                "role": "system",
                "content": re.sub(
                    r"\s+",
                    " ",
                    """Now you need to decide, based on the conversation above, whether 
                    to call Materials Project API for data or answer user requests 
                    directly based on the information you have. If you decide to call 
                    Materials Project API, respond 'Calling Materials Project API...'.
                    If the user request is ambiguous, respond 'Please clarify your
                    request.' If user decide to end the conversation, respond 'Goodbye!'
                    """,
                ).strip().replace('\n', ' ')
            })

        try:
            response = openai.ChatCompletion.create(
                model=model, messages=messages, temperature=0, top_p=1
            )
        except Exception as e:
            print("Error:", e, "Trying again with gpt-4-32k.")
            response = openai.ChatCompletion.create(
                model="gpt-4-32k", messages=messages, temperature=0, top_p=1
            )

        return response

    def material_response(
        self, message: dict[str, str], model="gpt-3.5-turbo-16k-0613"
    ):
        self.messages.append(message)
        self.trim_messages()

        messages = [
            {
                "role": "system",
                "content": re.sub(
                    r"\s+",
                    " ",
                    """You are a data-vigilant agent that answer user requests based on 
                    the expert-curated data retrieved from Materials Project and the 
                    conversation history below. Don't make assumptions about the values 
                    to plug into the functions. Ask for clarification if the user 
                    request is ambiguous. Provide `_fields` or `field` to the function 
                    whenever possible. Read the response from function calls carefully
                    and find out relevant information to respond to user requests."""
                ).strip().replace('\n', ' ')
            },
            *self.messages,
        ]

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                functions=self.material_functions,
                function_call="auto",
                temperature=0,
                top_p=1,
            )
        except Exception as e:
            print("Error:", e, "Trying again with gpt-4-32k.")
            response = openai.ChatCompletion.create(
                model="gpt-4-32k",
                messages=messages,
                functions=self.material_functions,
                function_call="auto",
                temperature=0,
                top_p=1,
            )
        return response

    def run_material_conversation(
        self,
        user_input: str | None = None,
        model: str | None = None,
        debug: bool = False,
    ):
        if debug:
            print("Conversation started.")
        
        while True:
            user_input = user_input if user_input else input("User: ")
            print("User:", user_input)
            gen_reponse = self.general_reponse(
                {"role": "user", "content": user_input},
                model=model if model else "gpt-3.5-turbo-0613",
            )
            if debug:
                print(gen_reponse)

            gen_reponse_msg = gen_reponse["choices"][0]["message"]  # type: ignore

            if gen_reponse_msg["content"] == "Calling Materials Project API...":
                mat_reponse = self.material_response(
                    {"role": "user", "content": user_input},
                    model=model if model else "gpt-3.5-turbo-16k-0613",
                )
                if debug:
                    print(mat_reponse)
                mat_reponse_msg = mat_reponse["choices"][0]["message"]  # type: ignore
                function_name = mat_reponse_msg.get("function_call", {}).get(
                    "name", None
                )

                print("OpenAI:", mat_reponse_msg)

                if function_name:
                    
                    print("MP API call:", function_name)
                    print("MP API args:", mat_reponse_msg["function_call"]["arguments"])

                    function_to_call = self.material_routes.get(function_name)
                    if function_to_call is None:
                        print(f"Function {function_name} is not supported yet.")
                        continue

                    function_args = json.loads(
                        mat_reponse_msg["function_call"]["arguments"]
                    )
                    function_response = function_to_call(query_params=function_args)

                    if debug:
                        print("MP API response:", json.dumps(function_response))

                    gen_reponse = self.general_reponse(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": json.dumps(function_response),
                        },
                        model=model if model else "gpt-3.5-turbo-0613",
                    )
                    if debug:
                        print(gen_reponse)

                    gen_reponse_msg = gen_reponse["choices"][0]["message"]  # type: ignore

            if gen_reponse_msg["content"] == "Goodbye!":
                break

            self._messages.append(gen_reponse_msg)
            
            print("OpenAI:", gen_reponse_msg["content"])
            time.sleep(0.5)

            user_input = None

            
