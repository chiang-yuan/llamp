
from ase import Atoms
from atomate2.forcefields.md import ForceFieldMDMaker
from jobflow import run_locally
from langchain.tools import BaseTool
from pymatgen.io.ase import AseAtomsAdaptor

from llamp.atomate2.schemas import AtomDict, Dynamics, MLFFMDInput


class MLFFMD(BaseTool):
    name: str = "MLFF MD"
    description: str = "Run MLFF MD simulation"
    args_schema: type[MLFFMDInput]= MLFFMDInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _run(self, **kwargs):

        atom_dict = kwargs.pop("atom_dict")
        assert isinstance(atom_dict, AtomDict)
        atoms = Atoms(**atom_dict.dict())
        structure = AseAtomsAdaptor.get_structure(atoms)

        job = ForceFieldMDMaker(**kwargs).make(structure)
        
        response = run_locally(job, create_folders=True)
        task_doc = response[next(iter(response))][1].output

        return task_doc