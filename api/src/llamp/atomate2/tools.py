import re
from pathlib import Path

from ase import Atoms
from ase.io import read, write
from atomate2.forcefields.md import ForceFieldMDMaker
from jobflow import run_locally
from langchain.tools import BaseTool
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor

from llamp.atomate2.schemas import AtomDict, MLFFMDInput, VASPInput

try:
    from atomate2.vasp.jobs.base import BaseVaspMaker
    from atomate2.vasp.powerups import add_metadata_to_flow
    from fireworks import LaunchPad
    from jobflow.managers.fireworks import flow_to_workflow

    fireworks_imported = True
except ImportError:
    fireworks_imported = False


class Atomate2Tool(BaseTool):
    name: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_structure(self, atom_path_or_dict) -> Structure:
        if isinstance(atom_path_or_dict, AtomDict):
            atoms = Atoms(**atom_path_or_dict.dict())
            structure = AseAtomsAdaptor.get_structure(atoms)
        elif isinstance(atom_path_or_dict, Path | str):

            atom_path_or_dict = Path(atom_path_or_dict)

            if atom_path_or_dict.suffix == ".json":
                structure = Structure.from_file(atom_path_or_dict)
            else:
                atoms = read(atom_path_or_dict)
                structure = AseAtomsAdaptor.get_structure(atoms)
        
        return structure

    def _submit_flow(self, flow, run_mode, project):
        if run_mode == "local":
            response = run_locally(flow, create_folders=True, raise_immediately=True)
            task_doc = response[next(iter(response))][1].output

            return task_doc
        elif run_mode == "fireworks":
            if not fireworks_imported:
                raise ImportError("Fireworks is not installed. Please install it to use this feature.")
            
            flow = add_metadata_to_flow(
                flow, 
                additional_fields={
                    "project": project,
                }
            )

            wf = flow_to_workflow(flow)

            lpad = LaunchPad.auto_load()
            lpad.add_wf(wf)

            return wf.to_display_dict()
        
    def _run(self, **kwargs):
        raise NotImplementedError


class MLFFMD(Atomate2Tool):
    name: str = "MLFF MD"
    description: str = (
        re.sub(
            r"\s+",
            " ",
            """Run molecular dynamics simulation using the MLFF force field.""",
        )
        .strip()
        .replace("\n", " ")
    )
    args_schema: type[MLFFMDInput]= MLFFMDInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _run(self, **kwargs):

        atom_path_or_dict = kwargs.pop("atom_path_or_dict")
        structure = self._get_structure(atom_path_or_dict)
        
        kwargs["ensemble"] = kwargs["ensemble"].lower()

        run_mode = kwargs.pop("run_mode")
        project = kwargs.pop("project")

        flow = ForceFieldMDMaker(**kwargs).make(structure)

        return self._submit_flow(flow, run_mode, project)
        
class VASP(Atomate2Tool):
    name: str = "VASP"
    description: str = "Run VASP calculation"
    args_schema: type[VASPInput] = VASPInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _run(self, **kwargs):

        atom_path_or_dict = kwargs.pop("atom_path_or_dict")
        structure = self._get_structure(atom_path_or_dict)

        run_mode = kwargs.pop("run_mode")
        project = kwargs.pop("project")

        flow = BaseVaspMaker(**kwargs).make(structure)

        return self._submit_flow(flow, run_mode, project)