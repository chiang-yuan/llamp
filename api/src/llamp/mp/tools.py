import json
import re
from typing import Optional

from emmet.core.summary import HasProps
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from langchain.tools import BaseTool, Tool

from llamp.mp.schemas import (
    ElasticitySchema,
    MagnetismSchema,
    SummarySchema,
    SynthesisSchema,
    ThermoSchema,
)
from llamp.utilities import MPAPIWrapper

# NOTE: https://python.langchain.com/docs/modules/agents/tools/custom_tools

class MPTool(BaseTool):
    name: str
    api_wrapper: MPAPIWrapper = Field(default_factory=MPAPIWrapper)

    # def _run(
    #     self,
    #     query: str,
    #     run_manager: CallbackManagerForToolRun | None = None,
    # ) -> str:
    #     return self.api_wrapper.run(
    #         function_name=self.name, 
    #         function_args=query
    #     )
    
    def _run(
            self,
            **query_params
    ):
        return self.api_wrapper.run(
            function_name=self.name,
            function_args=json.dumps(query_params),
            debug=False
        )
        
    
    async def _arun(
        self,
        function_name: str,
        function_args: str
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("async is not supported yet")
    
class MaterialsSummary(MPTool):
    name: str = "search_materials_summary__get"
    description: str = re.sub(
        r"\s+",
        " ",
        """useful when you need calulated or derived materials properties, also useful 
        when you need to perform filtering on chemical systems or sorting on materials 
        properties"""
    ).strip().replace("\n", " ")[0]
    args_schema: type[SummarySchema] = SummarySchema

class MaterialsElasticity(MPTool):
    name: str = "search_materials_elasticity__get"
    description: str = re.sub(
        r"\s+",
        " ",
        """useful when you need elasticity properties like bulk modulus, shear modulus, 
        elastic anisotropy, Poisson ratio, elastic/compliance tensors, also useful when 
        you need to perform filtering and sorting elastic properties and retrieve the 
        qualified materials"""
    ).strip().replace("\n", " ")[0]
    args_schema: type[ElasticitySchema] = ElasticitySchema

class MaterialsSynthsis(MPTool):
    name: str = "search_materials_synthesis__get"
    description: str = re.sub(
        r"\s+",
        " ",
        """useful when you need materials synthesis recipes and list out the reactions, 
        precursors, targets, operations, conditions, required devices and references."""
    ).strip().replace("\n", " ")[0]
    args_schema: type[SynthesisSchema] = SynthesisSchema

class MaterialsThermo(MPTool):
    name: str = "search_materials_thermo__get"
    description: str = re.sub(
        r"\s+",
        " ",
        """useful when you need thermodynamic properties like mass density, atomic 
        density, formation energy, decomposition enthalpy, energy above hull, 
        equilibrium reaction energy, and raw DFT calculated energy, also useful when
        you want to compare the thermodynamic properties of materials with 
        material_ids."""
    ).strip().replace("\n", " ")[0]
    args_schema: type[ThermoSchema] = ThermoSchema


class MaterialsMagnetism(MPTool):
    name: str = "search_materials_magnetism__get"
    description: str = re.sub(
        r"\s+",
        " ",
        """useful when you need magnetic properties like magnetic moment (magmoms), 
        magnetic ordering and symmetry, magnetic sites, magnetic type, also useful when 
        you need to perform filtering and sorting magnetic properties and retrieve the 
        qualified materials."""
    ).strip().replace("\n", " ")[0]
    args_schema: type[MagnetismSchema] = MagnetismSchema

# tools = [
#     # Tool.from_function(
#     #     func=search.run,
#     #     name="Search",
#     #     description="useful for when you need to answer questions about current events"
#     #     # coroutine= ... <- you can specify an async method if desired as well
#     # ),
#     MaterialsSummary()
# ]