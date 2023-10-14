import json
import os.path as osp
import re
import time
from pathlib import Path
from typing import Any

import openai
from langchain.agents import BaseMultiActionAgent
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.schema import (
    AgentAction,
    AgentFinish,
    ChatMessage,
)

# SystemMessage,
# messages_to_dict,
# AIMessage,
# HumanMessage,
# FunctionMessage,
# from langchain.agents.agent_toolkits import OpenAPIToolkit
from langchain.tools.json.tool import JsonSpec

# from langchain.llms import OpenAI
from mp_api.client import MPRester

# from langchain.agents.agent_toolkits.openapi import OpenAPISpec
from llamp.utils import MP_API_KEY, OPENAI_API_KEY

# from pydantic_settings import BaseSettings


class MultiLLaMP(BaseMultiActionAgent):
    @property
    def input_keys(self):
        return ["input"]

    def plan(
        self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
    ) -> list[AgentAction] | AgentFinish:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        if len(intermediate_steps) == 0:
            return [
                AgentAction(tool="Search", tool_input=kwargs["input"], log=""),
                AgentAction(tool="RandomWord",
                            tool_input=kwargs["input"], log=""),
            ]
        else:
            return AgentFinish(return_values={"output": "bar"}, log="")

    async def aplan(
        self, intermediate_steps: list[tuple[AgentAction, str]], **kwargs: Any
    ) -> list[AgentAction] | AgentFinish:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        if len(intermediate_steps) == 0:
            return [
                AgentAction(tool="Search", tool_input=kwargs["input"], log=""),
                AgentAction(tool="RandomWord",
                            tool_input=kwargs["input"], log=""),
            ]
        else:
            return AgentFinish(return_values={"output": "bar"}, log="")


# TODO: change this a child of Pydantic BaseModel
class MPLLM:
    # spec = JsonSpec.from_file(Path(__file__).parent.resolve() / "mp_openapi.json")
    spec_path = Path(__file__).parent.resolve() / "mp_openapi.json"

    call_mp_hint = "Call MP"
    call_arxiv_hint = "Call arXiv"

    # NOTE: json explorer
    # spec = OpenAPIToolkit.parse_file(
    #     osp.join(Path(__file__).parent.resolve(), "mp_openapi.json")
    # )

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

    def clear_messages(self):
        self._messages.clear()

    def set_messages(self, messages: list[dict[str, str]]):
        self._messages = messages

    @property
    def spec(self):
        return self.json_spec

    @property
    def reduced_spec(self):
        with open(self.spec_path) as f:
            import json

            raw_spec = json.load(f)

        raw_spec["servers"] = raw_spec.get(
            "servers", ["https://api.materialsproject.org"]
        )

        return reduce_openapi_spec(raw_spec)

    @property
    def json_spec(self) -> JsonSpec:
        return JsonSpec.from_file(self.spec_path)

    def search_materials_core(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.materials._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def fetch_materials_similarity(self, material_id: str, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.materials.get_data_by_id(
            document_id=material_id, **query_params
        )

    def search_materials_bonds(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.bonds._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_chemenv(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.chemenv._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_eos(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.eos._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_summary(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        # if query_params.get("material_ids"):
        #     material_ids = query_params.get("material_ids").split(",")
        #     if len(material_ids) < 5:  # TODO: move 5 to settings
        #         return self.mpr.summary._search(
        #             num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        #         )

        response = self.mpr.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
        # TODO: move 5 to settings
        if len(response) < 5:
            return response
        else:
            response = self.mpr.summary._search(
                num_chunks=None,
                chunk_size=1000,
                all_fields=[
                    "nsites",
                    "elements",
                    # "nelements",
                    "composition",
                    "formula_pretty",
                    # "formula_anonymous",
                    # "chemsys",
                    "volume",
                    "density",
                    "density_atomic",
                    "symmetry",
                    "property_name",
                    "material_id",
                    "deprecated",
                    # "deprecation_reasons",
                    "last_updated",
                    "warnings",
                    # "structure",
                    "task_ids",
                    "uncorrected_energy_per_atom",
                    "energy_per_atom",
                    "formation_energy_per_atom",
                    "energy_above_hull",
                    "is_stable",
                    "equilibrium_reaction_energy_per_atom",
                    "decomposes_to",
                    "band_gap",
                    "cbm",
                    "vbm",
                    "efermi",
                    "is_gap_direct",
                    "is_metal",
                    "bandstructure",
                    "dos",
                    "dos_energy_up",
                    "dos_energy_down",
                    "is_magnetic",
                    "ordering",
                    "total_magnetization",
                    "total_magnetization_normalized_vol",
                    "total_magnetization_normalized_formula_units",
                    "num_magnetic_sites",
                    "num_unique_magnetic_sites",
                    "types_of_magnetic_species",
                    "k_voigt",
                    "k_reuss",
                    "k_vrh",
                    "g_voigt",
                    "g_reuss",
                    "g_vrh",
                    "universal_anisotropy",
                    "homogeneous_poisson",
                    "e_total",
                    "e_ionic",
                    "e_electronic",
                    "n",
                    "e_ij_max",
                    "weighted_surface_energy_EV_PER_ANG2",
                    "weighted_surface_energy",
                    "weighted_work_function",
                    "surface_anisotropy",
                    "shape_factor",
                    "has_reconstructed",
                    "possible_species",
                    "has_props",
                    "theoretical",
                    "database_IDs",
                ],
                **query_params,
            )
            return

    def search_materials_robocrys(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")
        return self.mpr.robocrys._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_synthesis(self, query_params: dict):
        keywords = query_params.pop("keywords", None)
        if keywords:
            query_params["keywords"] = keywords.split(",")

        operations = query_params.pop("operations", None)
        if operations:
            query_params["operations"] = operations.split(",")

        condition_heating_atmosphere = query_params.pop(
            "condition_heating_atmosphere", None
        )
        if condition_heating_atmosphere:
            query_params[
                "condition_heating_atmosphere"
            ] = condition_heating_atmosphere.split(",")

        condition_mixing_device = query_params.pop(
            "condition_mixing_device", None)
        if condition_mixing_device:
            query_params["condition_mixing_device"] = condition_mixing_device.split(
                ",")

        condition_mixing_media = query_params.pop(
            "condition_mixing_media", None)
        if condition_mixing_media:
            query_params["condition_mixing_media"] = condition_mixing_media.split(
                ",")

        doc = self.mpr.synthesis._search(**query_params)

        if len(doc) < 5:
            return doc
        else:
            return doc[:5]

    def search_materials_oxidation_states(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        # FIXME
        if "possible_species" not in query_params["fields"]:
            query_params["fields"].append("possible_species")

        return self.mpr.oxidation_states._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_provenance(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")
        return self.mpr.provenance._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_tasks(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.tasks._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_thermo(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        # FIXME: _limit is not a valid query parameter for thermo search
        query_params["_limit"] = query_params.pop("limit", None)

        return self.mpr.thermo._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_dielectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.dielectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_piezoelectric(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.piezoelectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_magnetism(self, query_params):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

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
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

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

                    # print(elastic_doc)
                    elastic_docs.append(elastic_doc)

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
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        return self.mpr.electronic_structure._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    @property
    def endpoints(self):
        endpoints = [
            (route, method, operation)
            for route, paths in self.spec.dict_["paths"].items()
            for method, operation in paths.items()
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
                operation.get("operationId", None)
                if len(operation.get("operationId", None)) <= 64
                else operation.get("operationId", None)[:64]
            )

            description = operation.get("description", None) or operation.get(
                "summary", None
            )

            properties = {
                property["name"]: {
                    "type": property.get("schema", {}).get("type", None),
                    "description": property.get("description", None)
                    if property.get("description", None) is not None
                    else "",
                    **(
                        {"enum": property.get("schema", {}).get("enum", None)}
                        if property.get("schema", {}).get("enum", None) is not None
                        else {}
                    ),
                }
                for property in operation["parameters"]
                if property.get("schema", {}).get("type", None) is not None
            }

            required = [
                property["name"]
                for property in operation["parameters"]
                if property["required"]
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
            osp.join(Path(__file__).parent.resolve(),
                     "material_functions.json")
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
            "search_materials_chemenv__get": self.search_materials_chemenv,
            "search_materials_tasks_trajectory__get": None,
            "search_materials_tasks__get": self.search_materials_tasks,
            "get_by_key_materials_thermo_phase_diagram__phase_diagram_id___get": None,
            "search_materials_thermo__get": self.search_materials_thermo,
            "search_materials_dielectric__get": self.search_materials_dielectric,
            "search_materials_piezoelectric__get": self.search_materials_piezoelectric,
            "search_materials_magnetism__get": self.search_materials_magnetism,
            "get_by_key_materials_phonon__material_id___get": None,
            "search_materials_eos__get": self.search_materials_eos,
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
            "search_materials_synthesis__get": self.search_materials_synthesis,
            "search_materials_oxidation_states__get": self.search_materials_oxidation_states,
            "search_materials_alloys__get": None,
            "search_materials_provenance__get": self.search_materials_provenance,
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

    def trim_messages(self, debug: bool = False):
        total_tokens = sum(len(message["content"].split())
                           for message in self.messages)
        while total_tokens > self.max_tokens:
            oldest_message = self.messages.pop(0)
            if debug:
                print(f"remove message: {oldest_message}")
            total_tokens -= len(oldest_message["content"].split())

    def general_reponse(
        self, message: dict[str, str], model="gpt-3.5-turbo-0613", debug: bool = False
    ):
        if message["role"] != "function":
            self._messages.append(message)
            self.trim_messages(debug=debug)

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
                )
                .strip()
                .replace("\n", " "),
            },
            *self.messages,
        ]

        if message["role"] == "function":
            messages.append(message)
        else:
            messages.append(
                {
                    "role": "system",
                    "content": re.sub(
                        r"\s+",
                        " ",
                        f"""Now you need to decide, based on the last request above, whether 
                    to call Materials Project API for data or answer user request 
                    directly based on the information you have. If you decide to call 
                    Materials Project, respond {self.call_mp_hint}.
                    If the user request is ambiguous, respond 'Please clarify your
                    request.' If user decide to end the conversation, respond 'Goodbye!'
                    """,
                    )
                    .strip()
                    .replace("\n", " "),
                }
            )

        try:
            response = openai.ChatCompletion.create(
                model=model, messages=messages, temperature=0, top_p=1
            )
        except Exception as e:
            print("Error:", e)
            response = {}
            # response = openai.ChatCompletion.create(
            #     model="gpt-4-32k", messages=messages, temperature=0, top_p=1
            # )

        return response

    def material_response(
        self,
        message: dict[str, str],
        model="gpt-3.5-turbo-16k-0613",
        debug: bool = False,
    ):
        self.messages.append(message)
        self.trim_messages(debug=debug)

        messages = [
            {
                "role": "system",
                "content": re.sub(
                    r"\s+",
                    " ",
                    """You are a data-vigilant agent that answer user requests based on 
                    the expert-curated data retrieved from Materials Project and the 
                    conversation history below. Always read carefully the function 
                    specifications. Ask for clarification if the user request is 
                    ambiguous. You must provide `_fields` or `field` to the function 
                    arguments if required. Read the response from function calls 
                    carefully and find out relevant information to respond to user 
                    requests.""",
                )
                .strip()
                .replace("\n", " "),
            },
            {
                "role": "user",
                "content": re.sub(
                    r"\s+",
                    " ",
                    """You must provide `_fields` or `field` to the function 
                    arguments if required.""",
                )
                .strip()
                .replace("\n", " "),
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
            print("Error:", e)
            response = {}
            # response = openai.ChatCompletion.create(
            #     model="gpt-4-32k",
            #     messages=messages,
            #     functions=self.material_functions,
            #     function_call="auto",
            #     temperature=0,
            #     top_p=1,
            # )
        return response

    def __call__(self, message: ChatMessage, model: str = "gpt-3.5-turbo-0613"):
        pass

    def run(
        self,
        messages: list[ChatMessage],
        model: str = "gpt-3.5-turbo-0613",
        debug: bool = False,
    ) -> ChatMessage:
        message = messages[-1]
        self.set_messages([{
            'role': msg.role,
            'content': msg.content
        } for msg in messages[:-1]])
        self.trim_messages(debug=debug)

        gen_reponse = self.general_reponse(
            message.dict(include={"role", "content"}),
            model=model if model else "gpt-3.5-turbo-0613",
            debug=debug,
        )
        if debug:
            print("OpenAI General:", gen_reponse)

        gen_reponse_msg = gen_reponse["choices"][0]["message"]  # type: ignore

        if gen_reponse_msg["content"] == self.call_mp_hint:
            mat_reponse = self.material_response(
                message=message.dict(include={"role", "content"}),
                model=model if model else "gpt-3.5-turbo-16k-0613",
                debug=debug,
            )
            if debug:
                print("LLaMP Function Calling:", mat_reponse)
            # type: ignore
            mat_reponse_msg = mat_reponse["choices"][0]["message"]
            function_name = mat_reponse_msg.get(
                "function_call", {}).get("name", None)

            print("LLaMP:", mat_reponse_msg)

            if function_name:
                if debug:
                    print("MP API call:", function_name)
                    print(
                        "MP API args:",
                        mat_reponse_msg["function_call"]["arguments"],
                    )

                function_to_call = self.material_routes.get(function_name)
                if function_to_call is None:
                    print(f"Function {function_name} is not supported yet.")
                    return

                function_args = json.loads(
                    mat_reponse_msg["function_call"]["arguments"]
                )
                try:
                    function_response = function_to_call(
                        query_params=function_args)
                except Exception as e:
                    print("Error:", e)
                    print("Please provide more information or try smaller request.")
                    return

                if debug:
                    print("MP API response:", json.dumps(function_response))

                gen_reponse = self.general_reponse(
                    # FunctionMessage(json.dumps(function_response))
                    {
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    },
                    model=model if model else "gpt-3.5-turbo-0613",
                    debug=debug,
                )
                if debug:
                    print("OpenAI Text Completion:", gen_reponse)

                # type: ignore
                gen_reponse_msg = gen_reponse["choices"][0]["message"]

        self._messages.append(gen_reponse_msg)
        return gen_reponse_msg

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
                debug=debug,
            )
            if debug:
                print("OpenAI General:", gen_reponse)

            # type: ignore
            gen_reponse_msg = gen_reponse["choices"][0]["message"]

            if gen_reponse_msg["content"] == self.call_mp_hint:
                mat_reponse = self.material_response(
                    {"role": "user", "content": user_input},
                    model=model if model else "gpt-3.5-turbo-16k-0613",
                    debug=debug,
                )
                if debug:
                    print("LLaMP Function Calling:", mat_reponse)
                # type: ignore
                mat_reponse_msg = mat_reponse["choices"][0]["message"]
                function_name = mat_reponse_msg.get("function_call", {}).get(
                    "name", None
                )

                print("LLaMP:", mat_reponse_msg)

                if function_name:
                    if debug:
                        print("MP API call:", function_name)
                        print(
                            "MP API args:",
                            mat_reponse_msg["function_call"]["arguments"],
                        )

                    function_to_call = self.material_routes.get(function_name)
                    if function_to_call is None:
                        print(
                            f"Function {function_name} is not supported yet.")
                        user_input = None
                        continue

                    function_args = json.loads(
                        mat_reponse_msg["function_call"]["arguments"]
                    )
                    try:
                        function_response = function_to_call(
                            query_params=function_args)
                    except Exception as e:
                        print("Error:", e)
                        print(
                            "Please provide more information or try smaller request.")
                        user_input = None
                        continue

                    if debug:
                        print("MP API response:", json.dumps(function_response))

                    gen_reponse = self.general_reponse(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": json.dumps(function_response),
                        },
                        model=model if model else "gpt-3.5-turbo-0613",
                        debug=debug,
                    )
                    if debug:
                        print("OpenAI Text Completion:", gen_reponse)

                    # type: ignore
                    gen_reponse_msg = gen_reponse["choices"][0]["message"]

            self._messages.append(gen_reponse_msg)

            print("OpenAI:", gen_reponse_msg["content"])
            time.sleep(0.5)
            if gen_reponse_msg["content"] == "Goodbye!":
                break

            user_input = None
