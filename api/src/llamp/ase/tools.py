
import datetime
import json
import os
import re
from pathlib import Path

import torch
from ase import units
from ase.build import sort
from ase.md import MDLogger
from ase.md.npt import NPT
from langchain.tools import BaseTool
from mace.calculators import MACECalculator
from monty.json import MontyDecoder
from monty.tempfile import ScratchDir
from pydantic import Field
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
                        "material_ids": [material_id],
                        "fields": ["structure"]
                    }
                )
            )
            structure = json.loads(_response[0]["structure"], cls=MontyDecoder)
            atoms = AseAtomsAdaptor.get_atoms(structure)
            atoms = sort(atoms)
            print(atoms)
        
        # run md
        with ScratchDir("."):

            calculator = MACECalculator(
                model_paths=[Path(__file__).parent.absolute() / "2023-09-01-mace-universal.model"],
                device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
            )

            atoms.calc = calculator

            npt = NPT(
                atoms=atoms,
                timestep=kwargs["timestep"],
                temperature_K=kwargs["temperature"],
                externalstress=kwargs["pressure"]*units.GPa,
            )
            out_dir = Path(__file__).parent.absolute() / ".tmp"
            os.makedirs(out_dir, exist_ok=True)

            logfile = f'{atoms.get_chemical_formula()}_{tstring}.log'
            xyzfile = f'{atoms.get_chemical_formula()}_{tstring}.extxyz'
            npt.attach(
                MDLogger(
                    npt, atoms, 
                    out_dir / logfile, 
                    header=False, stress=False, peratom=True, mode="a"), 
                interval=kwargs["interval"]
                )
            npt.attach(
                TrajectoryWriter(
                    npt, atoms, 
                    out_dir / xyzfile, 
                    format='extxyz', mode='a'),
                interval=kwargs["interval"]
                )
            npt.run(kwargs["steps"])

        return '[simulation]' + json.dumps({"log": logfile, "extxyz": xyzfile})
        

    async def _arun(self, **kwargs):
        """Run Nose-Hoover MD asynchronously."""
        raise NotImplementedError("async is not supported yet")