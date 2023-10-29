import weakref

from ase.io import read, write
from ase.parallel import world
from ase.utils import IOContext


class TrajectoryWriter(IOContext):
    def __init__(self, dyn, atoms, extxyzfile, format='extxyz', mode="a"):
        if hasattr(dyn, "get_time"):
            self.dyn = weakref.proxy(dyn)
        else:
            self.dyn = None
        self.atoms = atoms
        self.extxyzfile = self.openfile(extxyzfile, comm=world, mode='a')
        self.format = format
        
    def __call__(self):
        write(self.extxyzfile, self.atoms, format=self.format, append=True)