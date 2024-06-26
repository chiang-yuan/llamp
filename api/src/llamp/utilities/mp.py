import json
import logging
import os.path as osp
import re
from pathlib import Path
from typing import Any

import mp_api
import mp_api.client
import requests
from ase.io import read, write
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.tools.json.tool import JsonSpec
from langchain.utils import get_from_dict_or_env
from pydantic import BaseModel, Field, model_validator
from pymatgen.core import Structure

logger = logging.getLogger(__name__)


DEFAULT_LIMIT = 10


class MPAPIWrapper(BaseModel):
    """Wrapper around mp-api.

    To use, you should have the ``mp-api`` python package installed.
    """

    mpr: Any = {}
    mp_api_key: str = Field("", alias="mpApiKey")

    max_tokens: int | None = 4096
    spec_path: Path | str = Path(
        __file__).parent.resolve() / "mp_openapi_selected.json"

    def set_api_key(self, api_key: str):
        self.mp_api_key = api_key
        self.mpr = mp_api.client.MPRester(
            api_key=api_key,
            monty_decode=False,
            use_document_model=False,
            headers={"X-API-KEY": api_key, "accept": "application/json"},
        )

    @model_validator(mode="after")
    def validate_environment(cls, values: dict) -> dict:
        """Validate that the python package exists in environment."""

        try:
            import mp_api

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
            return (
                re.sub(
                    r"\s+",
                    " ",
                    f"""
                I want to call {function_name} but it is not supported yet. 
                Please rephrase or confine your request.
                """,
                )
                .strip()
                .replace("\n", " ")
            )

        try:
            if debug:
                print(function_args)
            function_response = function_to_call(
                query_params=json.loads(function_args))
        except Exception as e:
            error_response = (
                f"Error on {function_name}: {e}. "
                "Please revise arguments "
                "or try smaller request by specifying 'limit' in request."
            )
            return error_response

        if debug:
            print("MP API response:", json.dumps(function_response))

        return function_response

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
        query_params["_limit"] = query_params.pop("limit", DEFAULT_LIMIT)
        all_fields = query_params.pop("all_fields", None)
        if all_fields:
            query_params["_all_fields"] = all_fields
        sort_fields = query_params.pop("sort_fields", None)
        if sort_fields:
            query_params["_sort_fields"] = sort_fields
            query_params["fields"] = list(
                set(query_params.get("fields", []) + [
                    f.lstrip('-') for f in sort_fields.split(",")])
            )
        return query_params

    def search_materials_core(self, query_params: dict):
        query_params = self._process_query_params(query_params)
        return self.mpr.materials._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def fetch_materials_similarity(self, query_params: dict):
        query_params = self._process_query_params(query_params)
        return self.mpr.materials.get_data_by_id(
            document_id=query_params.pop("material_id"), **query_params
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

        assert "fields" in query_params, "`fields` must be specified in the query"

        if "material_id" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["material_id"]

        if "formula_pretty" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["formula_pretty"]
            
        sort_fields = query_params.get("_sort_fields", "material_id")
        sort_fields = sort_fields.split(",")

        docs = self.mpr.materials.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )
        for sort_field in sort_fields:
            if sort_field[0] == '-':
                sort_field = sort_field[1:]
                docs = sorted(
                    docs, key=lambda x: x[sort_field], reverse=True
                )
            else:
                docs = sorted(
                    docs, key=lambda x: x[sort_field], reverse=False
                )
        return docs[:query_params.get("_limit", DEFAULT_LIMIT)]
            
        # limit = query_params.get("_limit", DEFAULT_LIMIT)

        # return self.mpr.materials.summary._search(
        #     num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        # )[:limit]

    def search_materials_structure(self, query_params: dict):
        # NOTE: this is a convenient function to retrieve pymatgen structure
        # but not a real mp-api endpoint

        query_params = self._process_query_params(query_params)

        if "material_id" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["material_id"]

        if "structure" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["structure"]
            
        if "formula_pretty" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["formula_pretty"]
            
        if "symmetry" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["symmetry"]

        # query_params["fields"] = query_params.get(
        #     "fields", []) + ["structure", "material_id"]

        return_mode = query_params.pop("return_mode", "file")

        limit = query_params.get("_limit", DEFAULT_LIMIT)

        # return self.mpr.materials.summary._search(
        #     num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        # )[:limit]
    
        docs = self.mpr.materials.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )[:limit]

        if return_mode == "text":
            return docs
        elif return_mode == "file":
            paths = []
            for doc in docs:
                structure = Structure.from_dict(doc["structure"])
                path = f"{doc['material_id']}-{doc['formula_pretty']}-sg{doc['symmetry']['number']}.json"
                structure.to_file(filename=path, fmt="json")
                # write(path, atoms, format="extxyz")
                paths.append(path)
            return "All retrieved structures are saved as Pymatgen Structure json files to the following paths: " + ", ".join(paths)

        # return [Structure.from_dict(doc["structure"]).to_ase_atoms() for doc in docs]


    def search_materials_robocrys(self, query_params: dict):
        query_params = self._process_query_params(query_params)

        if "material_id" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["material_id"]

        if "description" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["description"]

        if "material_ids" in query_params:
            return self.mpr.materials.robocrys._search(
                num_chunks=None, all_fields=False, **query_params
            )

        return self.mpr.materials.robocrys.text_query_resource(
            criteria={
                "keywords": query_params.pop("keywords"),
                "_limit": query_params.get("_limit", 10),
            },
            suburl="text_search",
            use_document_model=False,
            chunk_size=1000,
            num_chunks=None,
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

        response = self.mpr.materials.synthesis._search(**query_params)

        return response[:5]

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
        # query_params["_limit"] = query_params.pop("limit", None)

        thermo_types = query_params.pop("thermo_types", ["GGA_GGA+U_R2SCAN"])
        if thermo_types:
            query_params.update({"thermo_types": ",".join(thermo_types)})

        assert "fields" in query_params, "fields must be specified"

        if "energy_above_hull" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["energy_above_hull"]

        sort_fields = query_params.get("_sort_fields", "energy_above_hull")
        sort_fields = sort_fields.split(",")
        
        thermo_docs =  self.mpr.materials.thermo._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

        for sort_field in sort_fields:
            if sort_field[0] == '-':
                sort_field = sort_field[1:]
                thermo_docs = sorted(
                    thermo_docs, key=lambda x: x[sort_field], reverse=True
                )
            else:
                thermo_docs = sorted(
                    thermo_docs, key=lambda x: x[sort_field], reverse=False
                )
        return thermo_docs[:query_params.get("_limit", DEFAULT_LIMIT)]

    def search_materials_dielectric(self, query_params):
        query_params = self._process_query_params(query_params)

        query_params["fields"] = query_params.get(
            "fields", ["material_id", "formula_pretty",
                       "total", "n", "symmetry"]
        )

        if "material_id" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["material_id"]

        if "formula_pretty" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["formula_pretty"]

        if "formula" in query_params:
            material_docs = self.mpr.materials.summary.search(
                formula=query_params.pop("formula").split(","), fields=["material_id"]
            )

            material_ids = [doc["material_id"] for doc in material_docs]

            # query_params["material_ids"] = ",".join(material_ids)

            return self.mpr.materials.dielectric.search(
                material_ids=material_ids,
                fields=query_params.get(
                    "fields", "material_id,formula_pretty,total,n,symmetry"
                ).split(","),
            )

        return self.mpr.materials.dielectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_piezoelectric(self, query_params):
        query_params = self._process_query_params(query_params)

        if "formula" in query_params:
            material_docs = self.mpr.materials.summary.search(
                formula=query_params.pop("formula").split(","), fields=["material_id"]
            )

            material_ids = [doc["material_id"] for doc in material_docs]

            return self.mpr.materials.piezoelectric.search(
                material_ids=material_ids,
                fields=query_params.get(
                    "fields",
                    "material_id,formula_pretty,total,ionic,electronic,e_ij_max,max_direction,strain_for_max",
                ).split(","),
            )

        return self.mpr.materials.piezoelectric._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_magnetism(self, query_params):
        query_params = self._process_query_params(query_params)
        if "formula" in query_params:
            material_docs = self.mpr.materials.summary.search(
                formula=query_params.pop("formula").split(","), fields=["material_id"]
            )

            material_ids = [doc["material_id"] for doc in material_docs]

            query_params["material_ids"] = material_ids

        query_params["fields"] = query_params.get("fields", []) + [
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
        ]

        return self.mpr.magnetism._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_elasticity(self, query_params):
        query_params = self._process_query_params(query_params)

        query_params["fields"] = query_params.get("fields", []) + [
            "material_id",
            "formula_pretty",
            "elastic_tensor",
            "bulk_modulus"
            "shear_modulus",
            "thermal_conductivity",
            "young_modulus",
            "universal_anisotropy",
            "homogeneous_poisson"
        ]

        if "formula" in query_params:
            material_docs = self.mpr.materials.summary.search(
                formula=query_params.pop("formula"), fields=["material_id"]
            )

            matereial_ids = [doc["material_id"] for doc in material_docs]
            query_params["material_ids"] = ",".join(matereial_ids)

        # # BUG: mp-api does not support get elastic properties by material_ids
        # if "material_ids" in query_params:
        #     material_ids = query_params["material_ids"].split(",")
        #     elastic_docs = []
        #     for material_id in material_ids:
        #         try:
        #             elastic_doc = self.mpr.materials.elasticity.get_data_by_id(
        #                 document_id=material_id,
        #                 fields=["pretty_formula", "elasticity", "task_id"],
        #             )
        #             elastic_docs.append(elastic_doc)

        #         except Exception:
        #             continue

        #     return elastic_docs[:query_params.get("_limit", 10)]

        return self.mpr.materials.elasticity._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )

    def search_materials_electronic_structure(self, query_params):
        query_params = self._process_query_params(query_params)

        if "material_id" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["material_id"]

        if "formula_pretty" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["formula_pretty"]

        if "band_gap" not in query_params.get("fields", []):
            query_params["fields"] = query_params.get(
                "fields", []) + ["band_gap"]
            
        sort_fields = query_params.get("_sort_fields", "material_id,band_gap")
        sort_fields = sort_fields.split(",")

        # BUG: this endpoint does not support sorting yet
        query_params.pop("_sort_fields", None)

        docs = self.mpr.materials.electronic_structure._search(
            num_chunks=None, chunk_size=1000, all_fields=False, **query_params
        )
            
        for sort_field in sort_fields:
            if sort_field[0] == '-':
                sort_field = sort_field[1:]
                docs = sorted(
                    docs, key=lambda x: x[sort_field], reverse=True
                )
            else:
                docs = sorted(
                    docs, key=lambda x: x[sort_field], reverse=False
                )
        return docs[:query_params.get("_limit", DEFAULT_LIMIT)]

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
