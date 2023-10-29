

from ase import units
from pydantic import BaseModel, Field


class OptimizationSchema(BaseModel):
    """Schema for ASE optimization."""
    pass

class NoseHooverSchema(BaseModel):
    """Schema for running ASE Nose-Hoover MD"""
    # input structure
    material_id: str | None = Field(
        default='mp-766262', 
        description='Material ID to run molecular dynamics (MD) simulation'
        )
    xyz: str | None = Field(
        default=None,
        description='XYZ file to run molecular dynamics (MD) simulation'
        )
    # MD settings
    temperature: float | None = Field(
        default=300.0, 
        description='Temperature for MD simulation'
        )
    timestep: float | None = Field(
        default=5.0, 
        description='Timestep for MD simulation in femtoseconds'
        )
    ttime: float | None = Field(
        default=25 * units.fs, 
        description='Characteristic timescale of the thermostat. Set to None to disable the thermostat.'
        )
    pressure: float | None = Field(
        default=0.0, 
        description='Pressure for MD simulation in GPa'
        )
    pfactor: float | None = Field(
        default=(75 * units.fs)**2 * units.GPa, 
        description='A constant in the barostat differential equation. If a characteristic barostat timescale of ptime is desired, set pfactor to ptime^2 * B (where ptime is in units matching eV, Å, u; and B is the Bulk Modulus, given in eV/Å^3). Set to None to disable the barostat. Typical metallic bulk moduli are of the order of 100 GPa or 0.6 eV/A^3.'
        )
    nsteps: int | None = Field(
        default=1000, 
        description='Number of MD steps'
        )
    # output settings
    interval: int | None = Field(
        default=10, 
        description='Interval for logging MD steps'
        )