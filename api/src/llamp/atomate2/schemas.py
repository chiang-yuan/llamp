import json
from collections.abc import Sequence
from enum import Enum
from pathlib import Path
from typing import Literal

from atomate2.forcefields import MLFF
from atomate2.forcefields.md import _valid_dynamics
from atomate2.vasp.sets.base import VaspInputGenerator
from langchain.pydantic_v1 import BaseModel, Field


class AtomDict(BaseModel):
    # symbols: list[str] | None = Field(None, description="List of atomic symbols")
    positions: list[list[float]] = Field(..., description="List of atomic positions") 
    numbers: list[int] = Field(..., description="List of atomic numbers")
    tags: list[int] | None = Field(None, description="List of special purpose tags")
    momenta: list[list[float]] | None = Field(None, description="List of atomic momenta")
    masses: list[float] | None = Field(None, description="List of atomic masses")
    magmoms: list[float] | None = Field(None, description="List of atomic magnetic moments")
    charges: list[float] | None = Field(None, description="List of atomic charges")
    scaled_positions: list[list[float]] | None = Field(
        None, 
        description="Like positions, but given in units of the unit cell. Can not be set at the same time as positions."
    )
    cell: list[list[float]] = Field(..., description="Unit cell vectors")
    pbc: list[bool] = Field([True, True, True], description="Periodic boundary conditions")
    celldisp: list[list[float]] | None = Field(None, description="Cell displacements")
    constraint: list[dict] | None = Field(None, description="List of constraints")
    info: dict | None = Field(None, description="dictionary with additional information")
    velocities: list[list[float]] | None = Field(None, description="List of atomic velocities. Can not be set at the same time as momenta.")


class Dynamics(Enum):
    Langevin = "langevin"
    NoseHoover = "nose-hoover"
    VelocityVerlet = "velocityverlet"
    Andersen = "andersen"
    Berendsen = "berendsen"

class Atomate2Input(BaseModel):
    run_mode: Literal["local", "fireworks"] = Field(
        default="local",
        description="If 'local', run the simulation locally instantaneously. If 'fireworks', submit a FireWorks workflow to the LaunchPad for job submission."
    )
    project: str = Field(
        default="llamp-atomate2",
        description="The project name to register for data store."
    )
class MLFFMDInput(Atomate2Input):
    """
    Input model for MLFFMDTask
    """
    atom_path_or_dict: Path | AtomDict = Field(
        ..., 
        description="Path to a local file or ASE Atoms definition." + json.dumps(AtomDict.schema())
    )
    force_field_name: str = Field(
        f"{MLFF.MACE}",
        description="The name of the force Field to use. Options are: " + json.dumps([str(ff) for ff in MLFF])
    )
    time_step: float | None = Field(
        None, description="Time step in fs. If `None`, defaults to 0.5 fs if a structure contains an isotope of hydrogen and 2 fs otherwise."
    )
    n_steps: int = 1000
    ensemble: Literal["nve", "nvt", "npt", "NVE", "NVT", "NPT"] = "nvt"
    dynamics: str = Field(
        Dynamics.Langevin,
        description=f"The dynamical thermostat or barostat to use. The valid combination of ensemble and dynamics are {json.dumps(_valid_dynamics)}."
    )
    temperature: float | list[float] | None = Field(
        300.0, description="Temperature in Kelvin. If a list of float, the temperature schedule will be interpolated linearly between the given values."
    )
    pressure: float | list[float] | list[list[list[float]]] | None = Field(
        None, description="The pressure in kilobar. If a list of float, the pressure schedule will be interpolated linearly between the given values. If a list of 2d lists, the pressure tensor schedule will be interpolated linearly between the given values."
    )
    ase_md_kwargs: dict | None = Field(
        None, description="Additional keyword arguments to pass to ASE's Dyanmics class."
    )
    calculator_kwargs: dict = Field(
        default_factory=dict,
        description="Additional keyword arguments to pass to the calculator, such as `dispersion=True`."
    )
    traj_file: str | Path | None = None
    traj_file_fmt: Literal["pmg", "ase"] = "ase"
    traj_interval: int = 1
    mb_velocity_seed: int | None = None
    zero_linear_momentum: bool = False
    zero_angular_momentum: bool = False
    task_document_kwargs: dict = Field(
        default_factory=lambda: {
            "store_trajectory": "partial",
            "ionic_step_data": ("energy",),
        }
    )

class VASPInput(Atomate2Input):
    """
    Input model for VASPTask
    """
    atom_path_or_dict: Path | AtomDict = Field(
        ..., 
        description="Path to a local file or ASE Atoms definition." + json.dumps(AtomDict.schema())
    )
    name: str = Field("base vasp job", description="The job name.")
    input_set_generator: VaspInputGenerator = Field(
        VaspInputGenerator(),
        description="A generator used to make the input set."
    )
    write_input_set_kwargs: dict = Field(
        {},
        description="Keyword arguments passed to write_vasp_input_set."
    )
    copy_vasp_kwargs: dict = Field(
        {},
        description="Keyword arguments passed to copy_vasp_outputs."
    )
    run_vasp_kwargs: dict = Field(
        {},
        description="Keyword arguments passed to run_vasp."
    )
    task_document_kwargs: dict = Field(
        {},
        description="Keyword arguments passed to TaskDoc.from_directory."
    )
    stop_children_kwargs: dict = Field(
        {},
        description="Keyword arguments passed to should_stop_children."
    )
    write_additional_data: dict = Field(
        {},
        description="Additional data to write to the current directory. "
                    "Given as a dict of {filename: data}."
                    "If using FireWorks, keys cannot contain the '.' character; use ':' instead."
                    "E.g., {'my_file:txt': 'contents of the file'}."
    )