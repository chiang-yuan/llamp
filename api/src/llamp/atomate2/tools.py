import re
from pathlib import Path

from ase import Atoms
from ase.io import read, write
from atomate2.forcefields.md import ForceFieldMDMaker
from atomate2.forcefields.jobs import ForceFieldRelaxMaker
from jobflow import run_locally
from langchain.tools import BaseTool
from pymatgen.core import Structure
from pymatgen.io.ase import AseAtomsAdaptor

from llamp.atomate2.schemas import AtomDict, MLFFElasticInput, MLFFMDInput, VASPInput

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

        try:
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
            else:
                raise ValueError(
                    f"Unsupported type for atom_path_or_dict: {type(atom_path_or_dict)}"
                )
            return structure
        except Exception as e:
            raise RuntimeError(
                f"Failed to load the structure from {atom_path_or_dict}. Error: {e}"
            )

    def _submit_flow(self, flow, run_mode, project):
        if run_mode == "local":
            response = run_locally(flow, create_folders=False)
            task_doc = response[next(iter(response))][1].output

            return task_doc.output
        elif run_mode == "fireworks":
            if not fireworks_imported:
                raise ImportError(
                    "Fireworks is not installed. Please install it to use this feature."
                )

            flow = add_metadata_to_flow(
                flow,
                additional_fields={
                    "project": project,
                },
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
    args_schema: type[MLFFMDInput] = MLFFMDInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _submit_flow(self, flow, run_mode, project):
        if run_mode == "local":
            response = run_locally(flow, create_folders=False)
            task_doc = response[next(iter(response))][1].output

            return {
                "energy": task_doc.output.energy,
                "n_steps": task_doc.output.n_steps,
            }
        elif run_mode == "fireworks":
            if not fireworks_imported:
                raise ImportError(
                    "Fireworks is not installed. Please install it to use this feature."
                )

            flow = add_metadata_to_flow(
                flow,
                additional_fields={
                    "project": project,
                },
            )

            wf = flow_to_workflow(flow)

            lpad = LaunchPad.auto_load()
            lpad.add_wf(wf)

            return wf.to_display_dict()

    def _run(self, **kwargs):

        try:
            atom_path_or_dict = kwargs.pop("atom_path_or_dict", None)
            structure = self._get_structure(atom_path_or_dict)

            kwargs["ensemble"] = kwargs["ensemble"].lower()

            run_mode = kwargs.pop("run_mode", "local")
            project = kwargs.pop("project", "llamp-atomate2")

            flow = ForceFieldMDMaker(**kwargs).make(structure)

            return self._submit_flow(flow, run_mode, project)
        except Exception as e:
            return str(e)


class VASP(Atomate2Tool):
    name: str = "VASP"
    description: str = "Run VASP calculation"
    args_schema: type[VASPInput] = VASPInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _run(self, **kwargs):

        try:
            atom_path_or_dict = kwargs.pop("atom_path_or_dict", None)
            structure = self._get_structure(atom_path_or_dict)

            run_mode = kwargs.pop("run_mode", "local")
            project = kwargs.pop("project", "llamp-atomate2")

            flow = BaseVaspMaker(**kwargs).make(structure)

            return self._submit_flow(flow, run_mode, project)
        except Exception as e:
            return str(e)

class MLFFElastic(Atomate2Tool):
    name: str = "MLFF Elastic"
    description: str = (
        re.sub(
            r"\s+",
            " ",
            """Calculate elastic constants using ML forcefields.""",
        )
        .strip()
        .replace("\n", " ")
    )
    args_schema: type[MLFFElasticInput] = MLFFElasticInput

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _submit_flow(self, flow, run_mode, project):
        if run_mode == "local":
            response = run_locally(flow, create_folders=False)
            task_doc = list(response.values())[-1][1].output
            return {
                'elastic_tensor': task_doc.elastic_tensor,
                'derived_properties': task_doc.derived_properties
            }
        
        elif run_mode == "fireworks":
            if not fireworks_imported:
                raise ImportError(
                    "Fireworks is not installed. Please install it to use this feature."
                )
            flow = add_metadata_to_flow(
                flow,
                additional_fields={
                    "project": project,
                },
            )
            wf = flow_to_workflow(flow)
            lpad = LaunchPad.auto_load()
            lpad.add_wf(wf)
            return wf.to_display_dict()

    def _run(self, **kwargs):

        try:
            atom_path_or_dict = kwargs.pop("atom_path_or_dict", None)
            structure = self._get_structure(atom_path_or_dict)

            run_mode = kwargs.pop("run_mode", "local")
            project = kwargs.pop("project", "llamp-atomate2")

            force_field_name = kwargs.pop("force_field_name")

            from atomate2.forcefields.flows.elastic import ElasticMaker
            kwargs["bulk_relax_maker"] = ForceFieldRelaxMaker(
                force_field_name=force_field_name,
                relax_cell=True, relax_kwargs={"fmax": 0.00001}
            )
            kwargs["elastic_relax_maker"] = ForceFieldRelaxMaker(
                force_field_name=force_field_name,
                relax_cell=False, relax_kwargs={"fmax": 0.00001}
            )
            flow = ElasticMaker(**kwargs).make(structure)

            return self._submit_flow(flow, run_mode, project)
        except Exception as e:
            return str(e)