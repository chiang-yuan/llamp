"""Util that calls Arxiv."""
import json
import logging
import os
import os.path as osp
import re
from pathlib import Path
from typing import Any

from langchain.pydantic_v1 import BaseModel, root_validator
from langchain.schema import (
    Document,
)

logger = logging.getLogger(__name__)


class MPAPIWrapper(BaseModel):
    """Wrapper around mp-api.

    To use, you should have the ``mp-api`` python package installed.

    Attributes:

    Example:
        .. code-block:: python

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

    arxiv_search: Any  #: :meta private:
    arxiv_exceptions: Any  # :meta private:
    top_k_results: int = 3
    ARXIV_MAX_QUERY_LENGTH: int = 300
    load_max_docs: int = 100
    load_all_available_meta: bool = False
    doc_content_chars_max: int | None = 4000

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

        return self.mpr.materials.bonds._search(
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

        return self.mpr.materials.chemenv._search(
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

        return self.mpr.materials.eos._search(
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

        response = self.mpr.materials.summary._search(
            num_chunks=None, chunk_size=1000, all_fields=True, **query_params
        )
        return response

    def search_materials_robocrys(self, query_params: dict):
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")
        return self.mpr.materials.robocrys._search(
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

        doc = self.mpr.materials.synthesis._search(**query_params)

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

        return self.mpr.materials.oxidation_states._search(
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
        return self.mpr.materials.provenance._search(
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

        return self.mpr.materials.tasks._search(
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
        
        return self.mpr.materials.thermo._search(
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

        return self.mpr.materials.dielectric._search(
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

        return self.mpr.materials.piezoelectric._search(
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
        fields = query_params.pop("fields", None)
        if fields:
            query_params["fields"] = fields.split(",")
        _fields = query_params.pop("_fields", None)
        if _fields:
            query_params["fields"] = query_params.get(
                "fields", []) + _fields.split(",")

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
            "search_materials_electronic_structure_bandstructure__get": None,
            "search_materials_electronic_structure_dos__get": None,
            "search_materials_electronic_structure__get": self.search_materials_electronic_structure,
            "search_materials_electronic_structure_bandstructure_object__get": None,
            "search_materials_electronic_structure_dos_object__get": None,
        }

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        """Validate that the python package exists in environment."""
        try:
            import mp_api
            from mp_api.client import MPRester

            # import arxiv

            # values["arxiv_search"] = arxiv.Search
            # values["arxiv_exceptions"] = (
            #     arxiv.ArxivError,
            #     arxiv.UnexpectedEmptyPageError,
            #     arxiv.HTTPError,
            # )
            # values["arxiv_result"] = arxiv.Result
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
            raise ValueError(f"Error on {function_name}: {e}. Please provide more information or try smaller request.")
        
        if debug:
            print("MP API response:", json.dumps(function_response))

        return function_response

    def load(self, query: str) -> list[Document]:
        """
        Run Arxiv search and get the article texts plus the article meta information.
        See https://lukasschwab.me/arxiv.py/index.html#Search

        Returns: a list of documents with the document.page_content in text format

        Performs an arxiv search, downloads the top k results as PDFs, loads
        them as Documents, and returns them in a List.

        Args:
            query: a plaintext search query
        """  # noqa: E501
        try:
            import fitz
        except ImportError:
            raise ImportError(
                "PyMuPDF package not found, please install it with "
                "`pip install pymupdf`"
            )

        try:
            # Remove the ":" and "-" from the query, as they can cause search problems
            query = query.replace(":", "").replace("-", "")
            if self.is_arxiv_identifier(query):
                results = self.arxiv_search(
                    id_list=query[: self.ARXIV_MAX_QUERY_LENGTH].split(),
                    max_results=self.load_max_docs,
                ).results()
            else:
                results = self.arxiv_search(  # type: ignore
                    query[: self.ARXIV_MAX_QUERY_LENGTH], max_results=self.load_max_docs
                ).results()
        except self.arxiv_exceptions as ex:
            logger.debug("Error on arxiv: %s", ex)
            return []

        docs: list[Document] = []
        for result in results:
            try:
                doc_file_name: str = result.download_pdf()
                with fitz.open(doc_file_name) as doc_file:
                    text: str = "".join(page.get_text() for page in doc_file)
            except (FileNotFoundError, fitz.fitz.FileDataError) as f_ex:
                logger.debug(f_ex)
                continue
            if self.load_all_available_meta:
                extra_metadata = {
                    "entry_id": result.entry_id,
                    "published_first_time": str(result.published.date()),
                    "comment": result.comment,
                    "journal_ref": result.journal_ref,
                    "doi": result.doi,
                    "primary_category": result.primary_category,
                    "categories": result.categories,
                    "links": [link.href for link in result.links],
                }
            else:
                extra_metadata = {}
            metadata = {
                "Published": str(result.updated.date()),
                "Title": result.title,
                "Authors": ", ".join(a.name for a in result.authors),
                "Summary": result.summary,
                **extra_metadata,
            }
            doc = Document(
                page_content=text[: self.doc_content_chars_max], metadata=metadata
            )
            docs.append(doc)
            os.remove(doc_file_name)
        return docs