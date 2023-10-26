



# Import things that are needed generically
import re

from emmet.core.summary import HasProps
from langchain.tools import BaseTool, Tool
from langchain.utilities import SerpAPIWrapper
from pydantic import BaseModel, Field

from llamp.utilities import MPAPIWrapper


class SummarySchema(BaseModel):
    """Schema for the search_materials_summary__get endpoint"""
    material_ids: str = Field(description="Comma-separated list of material_ids to query on")
    formula: str = Field(description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.")
    chemsys: str = Field(description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries")
    elements: str = Field(description="Query by elements in the material composition as a comma-separated list")
    exclude_elements: str = Field(description="Query by excluded elements in the material composition as a comma-separated list")
    possible_species: str = Field(
        description="Comma delimited list of element symbols appended with oxidation states.",
        examples=["Cr2+,O2-"]
        )
    spacegroup_number: str = Field(description="Query by spacegroup number")
    is_stable: bool = Field(description="Whether the material is stable")
    theoretical: bool = Field(description="Whether the material is theoretical")
    is_gap_direct: bool = Field(description="Whether a band gap is direct or not")
    is_metal: bool = Field(description="Whether the material is a metal")
    nsites_max: int = Field(description="Maximum number of sites")
    nsites_min: int = Field(description="Minimum number of sites")
    nsites: int = Field(description="Query for nsites being equal to an exact value")
    nsites_not_eq: int = Field(description="Query for nsites not being equal to an exact value")
    nsites_eq_any: int = Field(description="Query for nsites being equal to any value in a comma separated list")
    nsites_neq_any: int = Field(description="Query for nsites not being equal to any value in a comma separated list")
    nelements_max: int = Field(description="Maximum number of elements")
    nelements_min: int = Field(description="Minimum number of elements")
    nelements: int = Field(description="Query for nelements being equal to an exact value")
    nelements_not_eq: int = Field(description="Query for nelements not being equal to an exact value")
    nelements_eq_any: int = Field(description="Query for nelements being equal to any value in a comma separated list")
    nelements_neq_any: int = Field(description="Query for nelements not being equal to any value in a comma separated list")
    volume_max: float = Field(description="Maximum volume in Å^3")
    volume_min: float = Field(description="Minimum volume in Å^3")
    density_max: float = Field(description="Maximum density in g/cm^3")
    density_min: float = Field(description="Minimum density in g/cm^3")
    density_atomic_max: float = Field(description="Maximum atomic density in atoms/Å^3")
    density_atomic_min: float = Field(description="Minimum atomic density in atoms/Å^3")
    uncorrected_energy_per_atom_max: float = Field(description="Maximum uncorrected energy per atom in eV/atom")
    uncorrected_energy_per_atom_min: float = Field(description="Minimum uncorrected energy per atom in eV/atom")
    energy_per_atom_max: float = Field(description="Maximum energy per atom in eV/atom")
    energy_per_atom_min: float = Field(description="Minimum energy per atom in eV/atom")
    formation_energy_per_atom_max: float = Field(description="Maximum formation energy per atom in eV/atom")
    formation_energy_per_atom_min: float = Field(description="Minimum formation energy per atom in eV/atom")
    energy_above_hull_max: float = Field(description="Maximum energy above hull in eV/atom")
    energy_above_hull_min: float = Field(description="Minimum energy above hull in eV/atom")
    equilibrium_reaction_energy_per_atom_max: float = Field(description="Maximum equilibrium reaction energy per atom in eV/atom")
    equilibrium_reaction_energy_per_atom_min: float = Field(description="Minimum equilibrium reaction energy per atom in eV/atom")
    band_gap_max: float = Field(description="Maximum band gap in eV")
    band_gap_min: float = Field(description="Minimum band gap in eV")
    efermi_max: float = Field(description="Maximum Fermi energy in eV")
    efermi_min: float = Field(description="Minimum Fermi energy in eV")
    dos_energy_up_max: float = Field(description="Maximum spin-up DOS energy in eV")
    dos_energy_up_min: float = Field(description="Minimum spin-up DOS energy in eV")
    dos_energy_down_max: float = Field(description="Maximum spin-down DOS energy in eV")
    dos_energy_down_min: float = Field(description="Minimum spin-down DOS energy in eV")
    total_magnetization_max: float = Field(description="Maximum total magnetization in Bohr magnetons")
    total_magnetization_min: float = Field(description="Minimum total magnetization in Bohr magnetons")
    total_magnetization_normalized_vol_max: float = Field(description="Maximum normalized total magnetization in Bohr magnetons/Å^3")
    total_magnetization_normalized_vol_min: float = Field(description="Minimum normalized total magnetization in Bohr magnetons/Å^3")
    total_magnetization_normalized_formula_units_max: float = Field(description="Maximum normalized total magnetization in Bohr magnetons/formula unit")
    total_magnetization_normalized_formula_units_min: float = Field(description="Minimum normalized total magnetization in Bohr magnetons/formula unit")
    num_magnetic_sites_max: int = Field(description="Maximum number of magnetic sites")
    num_magnetic_sites_min: int = Field(description="Minimum number of magnetic sites")
    num_magnetic_sites: int = Field(description="Query for num_magnetic_sites being equal to an exact value")
    num_magnetic_sites_not_eq: int = Field(description="Query for num_magnetic_sites not being equal to an exact value")
    num_magnetic_sites_eq_any: int = Field(description="Query for num_magnetic_sites being equal to any value in a comma separated list")
    num_magnetic_sites_neq_any: int = Field(description="Query for num_magnetic_sites not being equal to any value in a comma separated list")
    num_unique_magnetic_sites_max: int = Field(description="Maximum number of unique magnetic sites")
    num_unique_magnetic_sites_min: int = Field(description="Minimum number of unique magnetic sites")
    num_unique_magnetic_sites_not_eq: int = Field(description="Query for num_unique_magnetic_sites not being equal to an exact value")
    num_unique_magnetic_sites_eq_any: int = Field(description="Query for num_unique_magnetic_sites being equal to any value in a comma separated list")
    k_voigt_max: float = Field(description="Maximum Voigt bulk modulus in GPa")
    k_voigt_min: float = Field(description="Minimum Voigt bulk modulus in GPa")
    k_reuss_max: float = Field(description="Maximum Reuss bulk modulus in GPa")
    k_reuss_min: float = Field(description="Minimum Reuss bulk modulus in GPa")
    k_vrh_max: float = Field(description="Maximum Voigt-Reuss-Hill bulk modulus in GPa")
    k_vrh_min: float = Field(description="Minimum Voigt-Reuss-Hill bulk modulus in GPa")
    g_voigt_max: float = Field(description="Maximum Voigt shear modulus in GPa")
    g_voigt_min: float = Field(description="Minimum Voigt shear modulus in GPa")
    g_reuss_max: float = Field(description="Maximum Reuss shear modulus in GPa")
    g_reuss_min: float = Field(description="Minimum Reuss shear modulus in GPa")
    g_vrh_max: float = Field(description="Maximum Voigt-Reuss-Hill shear modulus in GPa")
    g_vrh_min: float = Field(description="Minimum Voigt-Reuss-Hill shear modulus in GPa")
    universal_anisotropy_max: float = Field(description="Maximum universal anisotropy")
    universal_anisotropy_min: float = Field(description="Minimum universal anisotropy")
    homogeneous_poisson_max: float = Field(description="Maximum homogeneous Poisson ratio")
    homogeneous_poisson_min: float = Field(description="Minimum homogeneous Poisson ratio")
    e_total_max: float = Field(description="Maximum total energy in eV")
    e_total_min: float = Field(description="Minimum total energy in eV")
    e_ionic_max: float = Field(description="Maximum ionic energy in eV")
    e_ionic_min: float = Field(description="Minimum ionic energy in eV")
    e_electronic_max: float = Field(description="Maximum electronic energy in eV")
    e_electronic_min: float = Field(description="Minimum electronic energy in eV")
    n_max: int = Field(description="Maximum number of atoms") # TODO: check if this is correct
    n_min: int = Field(description="Minimum number of atoms") # TODO: check if this is correct
    e_ij_max_max: float = Field(description="Maximum maximum pairwise energy in eV")
    e_ij_max_min: float = Field(description="Minimum maximum pairwise energy in eV")
    weighted_surface_energy_EV_PER_ANG2_max: float = Field(description="Maximum weighted surface energy in eV/Å^2")
    weighted_surface_energy_EV_PER_ANG2_min: float = Field(description="Minimum weighted surface energy in eV/Å^2")
    weighted_surface_energy_max: float = Field(description="Maximum weighted surface energy in J/m^2")
    weighted_surface_energy_min: float = Field(description="Minimum weighted surface energy in J/m^2")
    weighted_work_function_max: float = Field(description="Maximum weighted work function in eV")
    weighted_work_function_min: float = Field(description="Minimum weighted work function in eV")
    surface_anisotropy_max: float = Field(description="Maximum surface anisotropy")
    surface_anisotropy_min: float = Field(description="Minimum surface anisotropy")
    shape_factor_max: float = Field(description="Maximum shape factor")
    shape_factor_min: float = Field(description="Minimum shape factor")
    has_reconstructed: bool = Field(description="Whether the material has a reconstructed surface")
    has_props: list[HasProps] = Field(description="Comma-delimited list of possible properties given by HasPropsEnum to search for.")
    deprecated: bool = Field(description="Whether the material is deprecated")
    _sort_fields: str = Field(description="Comma-delimited list of fields to sort on. Prefix with - for descending order.")
    # _page
    # _per_page
    # _skip
    _limit: int = Field(description="Maximum number of results to return")
    _fields: str = Field(description="Comma-delimited list of fields to return in results")
    _all_fields: bool = Field(description="Whether to return all fields in results")

class ElasticitySchema(BaseModel):
    chemsys: str = Field(description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries")
    


class MaterialSummary(BaseTool):
    name = "search_materials_summary__get"
    description = re.sub(
        r"\s+",
        " ",
        """useful when you need calulated or derived materials properties. also useful 
        when you need to perform filtering on chemical systems or sorting on materials 
        properties"""
    ).strip().replace("\n", " "),
    args_schema: type[SummarySchema] = SummarySchema

    def _run(
        self,
        function_name: str,
        function_args: str
    ) -> str:
        mpapi_wrapper = MPAPIWrapper()

        return mpapi_wrapper.run(function_name=function_name, function_args=function_args)

    async def _arun(
        self,
        function_name: str,
        function_args: str
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
    


tools = [
    # Tool.from_function(
    #     func=search.run,
    #     name="Search",
    #     description="useful for when you need to answer questions about current events"
    #     # coroutine= ... <- you can specify an async method if desired as well
    # ),
    MaterialSummary()
]
