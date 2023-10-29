"""Util that calls Arxiv."""
import json
import logging
import os
import os.path as osp
import re
from pathlib import Path
from typing import Any

import requests
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.pydantic_v1 import BaseModel, root_validator
from langchain.schema import (
    Document,
)
from langchain.tools.json.tool import JsonSpec
from langchain.utils import get_from_dict_or_env

# from pydantic import BaseModel
from llamp.utils import MP_API_KEY, OPENAI_API_KEY

logger = logging.getLogger(__name__)


# NOTE: https://python.langchain.com/docs/modules/agents/tools/custom_tools


class MPAPIWrapper(BaseModel):
    """Wrapper around mp-api.

    To use, you should have the ``mp-api`` python package installed.

    Attributes:

    Example:
        .. code-block:: python
            # TODO: modify this example
            from langchain.utilities.arxiv import ArxivAPIWrapper
            arxiv = ArxivAPIWrapper(
                top_k_results = 3,
                ARXIV_MAX_QUERY_LENGTH = 300,
                load_max_docs = 3,
                load_all_available_meta = False,
                doc_content_chars_max = 40000
            )
            arxiv.run("tree of thought llm)
    """

    max_tokens: int = 2048
    mp_api_key: str = MP_API_KEY
    openai_api_key: str = OPENAI_API_KEY

    spec_path = Path(__file__).parent.resolve() / "mp_openapi_selected.json"

    mpr: Any

    @property
    def spec(self):
        return self.json_spec

    @property
    def reduced_spec(self):
        if self.spec_path.exists():
            with open(self.spec_path) as f:
                import json

                raw_spec = json.load(f)
        else:
            raw_spec = requests.get(
                "https://api.materialsproject.org/openapi.json"
            ).json()

        # raw_spec["servers"] = ["https://api.materialsproject.org"]
        raw_spec["servers"] = raw_spec.get(
            "servers", [{"url": "https://api.materialsproject.org"}]
        )

        return reduce_openapi_spec(raw_spec)

    @property
    def json_spec(self) -> JsonSpec:
        return JsonSpec.from_file(self.spec_path)

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
            idx = list(map(lambda x: x["name"], functions)).index(
                "search_materials_core_formula_autocomplete__get"
            )
            functions.pop(idx)
            idx = list(map(lambda x: x["name"], functions)).index(
                "search_materials_provenance__get"
            )
            functions.pop(idx)
            return functions

    def _process_query_params(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

        limit = query_params.pop("limit", None)
        if limit:
            query_params["_limit"] = limit
        sort_fields = query_params.pop("sort_fields", None)
        if sort_fields:
            query_params["_sort_fields"] = sort_fields.split(",")

        return query_params

    def search_materials_core(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def fetch_materials_similarity(self, material_id: str, query_params: dict):
        query_params = self._process_query_params(query_params)

        # TODO: add support for query by formula

        return self.mpr.materials.similarity.get_data_by_id(
            document_id=material_id, **query_params
        )

    def search_materials_bonds(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.bonds._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_chemenv(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.chemenv._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_eos(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.eos._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_summary(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_structure(self, query_params: dict):
        # NOTE: this is a convenient function to retrieve pymatgen structure in JSON
        # but not a real mp-api endpoint

        query_params = self._process_query_params(query_params)
        query_params["fields"] = query_params.get(
            "fields", []) + ["structure", "material_id"]

        return self.mpr.materials.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_robocrys(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.robocrys._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )

    def search_materials_synthesis(self, query_params: dict):
        query_params = self._process_query_params(query_params)

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

        doc = self.mpr.materials.synthesis._search(**query_params)

        if len(doc) < 5:
            return doc
        else:
            return doc[:5]

    def search_materials_oxidation_states(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        # FIXME
        if "possible_species" not in query_params["fields"]:
            query_params["fields"].append("possible_species")

        return self.mpr.materials.oxidation_states._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_provenance(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.provenance._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_tasks(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.tasks._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_thermo(self, query_params):
        query_params = self._process_query_params(query_params)

        # FIXME: _limit is not a valid query parameter for thermo search
        query_params["_limit"] = query_params.pop("limit", None)

        return self.mpr.materials.thermo._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_dielectric(self, query_params):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.dielectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_piezoelectric(self, query_params):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.piezoelectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_magnetism(self, query_params):
        query_params = self._process_query_params(query_params)

        if "formula" in query_params:
            material_docs = self.mpr.materials.search(
                formula=query_params.pop("formula").split(","), fields=["material_id"]
            )

            material_ids = [doc["material_id"] for doc in material_docs]

            return self.mpr.materials.magnetism.search(
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
        query_params = self._process_query_params(query_params)

        if "formula" in query_params:
            material_docs = self.mpr.materials.search(
                formula=query_params["formula"].split(","), fields=["material_id"]
            )

            elastic_docs = []
            for doc in material_docs:
                try:
                    elastic_doc = self.mpr.materials.elasticity.get_data_by_id(
                        document_id=doc["material_id"],
                        fields=["pretty_formula", "elasticity", "task_id"],
                    )

                    # print(elastic_doc)
                    elastic_docs.append(elastic_doc)

                except Exception:
                    continue

            return elastic_docs

        return self.mpr.materials.elasticity._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_electronic_structure(self, query_params):
        query_params = self._process_query_params(query_params)

        return self.mpr.materials.electronic_structure._search(
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
            # "search_materials_provenance__get": self.search_materials_provenance,
            "search_materials_charge_density__get": None,
            "get_by_key_materials_charge_density__fs_id___get": None,
            "search_materials_summary_stats__get": None,
            "search_materials_summary__get": self.search_materials_summary,
            "search_materials_structure__get": self.search_materials_structure,
            "search_materials_electronic_structure_bandstructure__get": None,
            "search_materials_electronic_structure_dos__get": None,
            "search_materials_electronic_structure__get": self.search_materials_electronic_structure,
            "search_materials_electronic_structure_bandstructure_object__get": None,
            "search_materials_electronic_structure_dos_object__get": None,
        }

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        """Validate that the python package exists in environment."""

        mp_api_key = get_from_dict_or_env(
            values, "mp_api_key", "MP_API_KEY"
        )

        openai_api_key = get_from_dict_or_env(
            values, "openai_api_key", "OPENAI_API_KEY"
        )

        try:
            import openai
            openai.api_key = openai_api_key
        except ImportError:
            raise ImportError(
                "Could not import `openai` python package. "
                "Please install it with `pip install openai`."
            )
        try:
            import mp_api
            import mp_api.client
            os.environ["MP_API_KEY"] = mp_api_key

            values["client"] = mp_api.client
            values["mpr"] = mp_api.client.MPRester(
                api_key=mp_api_key, monty_decode=False, use_document_model=False,
                headers={"X-API-KEY": mp_api_key, 'accept': 'application/json'}
            )
        except ImportError:
            raise ImportError(
                "Could not import `mp_api` python package. "
                "Please install it with `pip install mp_api`."
            )
        return values

    def run(self, function_name: str, function_args: str, debug: bool = False) -> str:
        """
        Performs an mp-api call and returns the result.

        Args:
            function_name: a function name to call
            function_args: arguments for the function
            debug: whether to print debug information
        Returns:
            function response in text format
        """

        function_to_call = self.material_routes.get(function_name, None)
        if function_to_call is None:
            print(f"Function {function_name} is not supported yet.")
            return re.sub(
                r"\s+",
                " ",
                f"""
                I want to call {function_name} but it is not supported yet. 
                Please rephrase or confine your request.
                """
            ).strip().replace("\n", " ")

        try:
            function_response = function_to_call(
                query_params=json.loads(function_args))
        except Exception as e:
            raise ValueError(
                f"Error on {function_name}: {e}. Please provide more information or try smaller request.")

        if debug:
            # print("MP API response:", json.dumps(function_response))
            pass

        return function_response
