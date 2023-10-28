import json

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from langchain.tools import BaseTool, Tool

from llamp.elementari.schemas import StructureSchema
from llamp.mp.mpapi import MPAPIWrapper


class StructureVis(BaseTool):
    name: str = "search_materials_structure__get"
    api_wrapper: MPAPIWrapper = Field(default_factory=MPAPIWrapper)

    def _count_token(self, response) -> int:
        '''TODO'''
        pass

    def _too_large(self, response) -> bool:
        '''TODO'''
        return self._count_token(response) > 200

    def _summarize(self, response) -> str:
        '''summarize w/ anthropic'''
        pass

    def _run(self, **query_params):
        _res = self.api_wrapper.run(
            function_name=self.name, function_args=json.dumps(query_params), debug=False
        )

        for entry in _res:
            yield entry['structure']
        
        '''
        while self._too_large(_res):
            _res = self._summarize(_res)
        return _res
        '''
        # return _res

    async def _arun(self, function_name: str, function_args: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("async is not supported yet")
    

    

