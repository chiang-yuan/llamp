import json
from collections.abc import Sequence
from enum import Enum
from pathlib import Path
from typing import Literal

from atomate2.forcefields import MLFF
from atomate2.forcefields.md import _valid_dynamics

# from pydantic import BaseModel, Field
from langchain.pydantic_v1 import BaseModel, Field
from pymatgen.core import Structure


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
    info: dict | None = Field(None, description="Dictionary with additional information")
    velocities: list[list[float]] | None = Field(None, description="List of atomic velocities. Can not be set at the same time as momenta.")


class Dynamics(Enum):
    Langevin = "langevin"
    NoseHoover = "nose-hoover"
    VelocityVerlet = "velocityverlet"
    Andersen = "andersen"
    Berendsen = "berendsen"

class MLFFMDInput(BaseModel):
    """
    Input model for MLFFMDTask
    """
    atom_dict: AtomDict = Field(
        ..., 
        description="ASE Atoms definition." + json.dumps(AtomDict.schema())
    )
    force_field_name: MLFF = MLFF.MACE
    time_step: float | None = None
    n_steps: int = 1000
    ensemble: Literal["nve", "nvt", "npt"]
    dynamics: str = Field(
        ...,
        description=f"The dynamical thermostat or barostat to use. The valid combination of ensemble and dynamics are {json.dumps(_valid_dynamics)}."
    )
    temperature: float | list[float] | None = Field(
        300.0, description="Temperature in Kelvin. If a list of float, the temperature schedule will be interpolated linearly between the given values."
    )
    pressure: float | list[float] | list[list[list[float]]] | None = Field(
        None, description="The pressure in kilobar. If a list of float, the pressure schedule will be interpolated linearly between the given values. If a list of 2d lists, the pressure tensor schedule will be interpolated linearly between the given values."
    )
    ase_md_kwargs: dict | None = None
    calculator_kwargs: dict = Field(default_factory=dict)
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