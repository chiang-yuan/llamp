
import datetime
import glob
import json
import os
import re
from pathlib import Path

import numpy as np
import torch
from ase import units
from ase.build import sort
from ase.md import MDLogger
from ase.md.npt import NPT
from langchain.pydantic_v1 import Field
from langchain.tools import BaseTool
from mace.calculators import MACECalculator
from monty.json import MontyDecoder
from monty.tempfile import ScratchDir
from pymatgen.io.ase import AseAtomsAdaptor

from llamp.ase.schemas import NoseHooverSchema
from llamp.ase.utils import TrajectoryWriter
from llamp.utilities import MPAPIWrapper


class NoseHooverMD(BaseTool):
    """Nose-Hoover MD tool."""
    name: str = "nose_hoover_md"
    description: str = (
        re.sub(
            r"\s+",
            " ",
            """useful when you need to run molecular dynamics (MD) simulation using 
            Nosé-Hoover dynamics. In Nosé-Hoover dynamics, an extra term is added to 
            the Hamiltonian representing the coupling to the heat bath. From a p
            ragmatic point of view one can regard Nosé-Hoover dynamics as adding a 
            friction term to Newton’s second law, but dynamically changing the friction 
            coefficient to move the system towards the desired temperature. Typically 
            the “friction coefficient” will fluctuate around zero.""",
        )
        .strip()
        .replace("\n", " ")[0]
    )
    args_schema: type[NoseHooverSchema] = NoseHooverSchema
    api_wrapper: MPAPIWrapper = Field(default_factory=MPAPIWrapper)

    def _process_args(self, **kwargs):
        kwargs["pressure"] = kwargs.get("pressure", 0.0)
        kwargs["pfactor"] = kwargs.get(
            "pfactor", (75 * units.fs)**2 * units.GPa)
        kwargs["ttime"] = kwargs.get("ttime", 25 * units.fs)

    def _run(self, **kwargs):
        """Run Nose-Hoover MD."""

        ctime = datetime.datetime.now()
        tstring = ctime.strftime("%Y-%m-%d-%H-%M-%S")

        # fetch pymatgen structure and convert to ASE atoms
        if "material_id" in kwargs:
            material_id = kwargs["material_id"]
            # _response = self.api_wrapper.mpr.summary.search(
            #     material_ids=[material_id],
            #     fields=["structure"]
            #     )
            _response = self.api_wrapper.run(
                function_name="search_materials_summary__get",
                function_args=json.dumps(
                    {
                        "material_ids": material_id,
                        "fields": "structure"
                    }
                )
            )
            structure = json.loads(json.dumps(
                _response[0]["structure"]), cls=MontyDecoder)
            atoms = AseAtomsAdaptor.get_atoms(structure)
            atoms = sort(atoms)

            print('before triu', atoms)

            scaled_pos = atoms.get_scaled_positions(wrap=True)
            triu_cell = np.triu(atoms.get_cell(complete=True))
            atoms.set_cell(triu_cell)
            atoms.set_scaled_positions(scaled_pos)

            print('after triu', atoms)

        # run md
        # with ScratchDir("."):

        calculator = MACECalculator(
            model_paths=[Path(__file__).parent.absolute() /
                            "2023-09-01-mace-universal.model"],
            # FIXME: torch.device("cuda" if torch.cuda.is_available() else "cpu")
            device="cpu"
        )

        atoms.calc = calculator

        npt = NPT(
            atoms=atoms,
            timestep=kwargs.get("timestep", 5.0) * units.fs,
            temperature_K=kwargs.get("temperature", 300.0),
            externalstress=kwargs.get("pressure", 0.0) * units.GPa,
            ttime=kwargs.get("ttime", 25 * units.fs),
            pfactor=kwargs.get("pfactor", (75 * units.fs)**2 * units.GPa),
        )
        out_dir = Path(__file__).parent.absolute() / ".tmp"
        os.makedirs(out_dir, exist_ok=True)

        logfile = f'{atoms.get_chemical_formula()}_{tstring}.log'
        xyzfile = f'{atoms.get_chemical_formula()}_{tstring}.extxyz'
        interval = kwargs.get("interval", 10)
        npt.attach(
            MDLogger(
                npt, atoms,
                out_dir / logfile,
                header=True, stress=True, peratom=True, mode="a"),
            interval=interval
        )
        npt.attach(
            TrajectoryWriter(
                npt, atoms,
                out_dir / xyzfile,
                format='extxyz', mode='a'),
            interval=interval
        )
        npt.run(kwargs.get("nsteps", 1000))

        fpattern = str(
            out_dir / f'{atoms.get_chemical_formula()}_{tstring}.*.json')
        jsons = sorted(
            glob.glob(fpattern),
            key=lambda x: int(x.split('.')[-2])
        )

        # NOTE: logfile for xyz plot, jsons for simulation animation
        # NOTE: absolute file paths are returned for all the files
        return '[simulation]' + json.dumps({"log": str(out_dir / logfile), "jsons": jsons})

    async def _arun(self, **kwargs):
        """Run Nose-Hoover MD asynchronously."""
        raise NotImplementedError("async is not supported yet")
