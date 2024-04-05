import weakref
from typing import TYPE_CHECKING

from ase.io import read, write
from ase.parallel import world
from ase.utils import IOContext
from pymatgen.io.ase import AseAtomsAdaptor

if TYPE_CHECKING:
    from ase import Atoms


class TrajectoryWriter(IOContext):
    def __init__(self, dyn, atoms, extxyzfile, format="extxyz", mode="a"):
        if hasattr(dyn, "get_time"):
            self.dyn = weakref.proxy(dyn)
        else:
            self.dyn = None
        self.atoms: Atoms = atoms
        self.extxyzfile = self.openfile(extxyzfile, comm=world, mode="a")
        self.extxyzfpath = self.extxyzfile.name
        self.format = format

    def __call__(self):
        write(self.extxyzfile, self.atoms, format=self.format, append=True)

        structure = AseAtomsAdaptor().get_structure(self.atoms)
        with open(
            f"{self.extxyzfpath}.{self.dyn.get_number_of_steps()}.json", "w"
        ) as f:
            f.write(structure.to_json())
