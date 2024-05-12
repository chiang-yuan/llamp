from emmet.core.summary import HasProps
from emmet.core.thermo import ThermoType

# from pydantic import BaseModel, Field
from langchain.pydantic_v1 import BaseModel, Field
from pymatgen.analysis.magnetism.analyzer import Ordering


class SummarySchema(BaseModel):
    """Schema for the search_materials_summary__get endpoint"""

    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    elements: str | None = Field(
        None,
        description="Query by elements in the material composition as a comma-separated list",
    )
    exclude_elements: str | None = Field(
        None,
        description="Query by excluded elements in the material composition as a comma-separated list",
    )
    possible_species: str | None = Field(
        None,
        description="Comma delimited list of element symbols appended with oxidation states.",
        examples=["Cr2+,O2-"],
    )
    spacegroup_number: str | None = Field(
        None, description="Query by spacegroup number"
    )
    is_stable: bool | None = Field(None, description="Whether the material is stable")
    theoretical: bool | None = Field(
        None, description="Whether the material is theoretical"
    )
    is_gap_direct: bool | None = Field(
        None, description="Whether a band gap is direct or not"
    )
    is_metal: bool | None = Field(None, description="Whether the material is a metal")
    nsites_max: int | None = Field(None, description="Maximum number of sites")
    nsites_min: int | None = Field(None, description="Minimum number of sites")
    nsites: int | None = Field(
        None, description="Query for nsites being equal to an exact value"
    )
    nsites_not_eq: int | None = Field(
        None, description="Query for nsites not being equal to an exact value"
    )
    nsites_eq_any: int | None = Field(
        None,
        description="Query for nsites being equal to any value in a comma separated list",
    )
    nsites_neq_any: int | None = Field(
        None,
        description="Query for nsites not being equal to any value in a comma separated list",
    )
    nelements_max: int | None = Field(None, description="Maximum number of elements")
    nelements_min: int | None = Field(None, description="Minimum number of elements")
    nelements: int | None = Field(
        None, description="Query for nelements being equal to an exact value"
    )
    nelements_not_eq: int | None = Field(
        None, description="Query for nelements not being equal to an exact value"
    )
    nelements_eq_any: int | None = Field(
        None,
        description="Query for nelements being equal to any value in a comma separated list",
    )
    nelements_neq_any: int | None = Field(
        None,
        description="Query for nelements not being equal to any value in a comma separated list",
    )
    volume_max: float | None = Field(None, description="Maximum volume in Å^3")
    volume_min: float | None = Field(None, description="Minimum volume in Å^3")
    density_max: float | None = Field(None, description="Maximum density in g/cm^3")
    density_min: float | None = Field(None, description="Minimum density in g/cm^3")
    density_atomic_max: float | None = Field(
        None, description="Maximum volume per atom in Å^3/atom"
    )
    density_atomic_min: float | None = Field(
        None, description="Minimum volume per atom in Å^3/atom"
    )
    uncorrected_energy_per_atom_max: float | None = Field(
        None, description="Maximum uncorrected energy per atom in eV/atom"
    )
    uncorrected_energy_per_atom_min: float | None = Field(
        None, description="Minimum uncorrected energy per atom in eV/atom"
    )
    energy_per_atom_max: float | None = Field(
        None, description="Maximum energy per atom in eV/atom"
    )
    energy_per_atom_min: float | None = Field(
        None, description="Minimum energy per atom in eV/atom"
    )
    formation_energy_per_atom_max: float | None = Field(
        None, description="Maximum formation energy per atom in eV/atom"
    )
    formation_energy_per_atom_min: float | None = Field(
        None, description="Minimum formation energy per atom in eV/atom"
    )
    energy_above_hull_max: float | None = Field(
        None, description="Maximum energy above hull in eV/atom"
    )
    energy_above_hull_min: float | None = Field(
        None, description="Minimum energy above hull in eV/atom"
    )
    equilibrium_reaction_energy_per_atom_max: float | None = Field(
        None, description="Maximum equilibrium reaction energy per atom in eV/atom"
    )
    equilibrium_reaction_energy_per_atom_min: float | None = Field(
        None, description="Minimum equilibrium reaction energy per atom in eV/atom"
    )
    band_gap_max: float | None = Field(None, description="Maximum band gap in eV")
    band_gap_min: float | None = Field(None, description="Minimum band gap in eV")
    efermi_max: float | None = Field(None, description="Maximum Fermi energy in eV")
    efermi_min: float | None = Field(None, description="Minimum Fermi energy in eV")
    dos_energy_up_max: float | None = Field(
        None, description="Maximum spin-up DOS energy in eV"
    )
    dos_energy_up_min: float | None = Field(
        None, description="Minimum spin-up DOS energy in eV"
    )
    dos_energy_down_max: float | None = Field(
        None, description="Maximum spin-down DOS energy in eV"
    )
    dos_energy_down_min: float | None = Field(
        None, description="Minimum spin-down DOS energy in eV"
    )
    total_magnetization_max: float | None = Field(
        None, description="Maximum total magnetization in Bohr magnetons"
    )
    total_magnetization_min: float | None = Field(
        None, description="Minimum total magnetization in Bohr magnetons"
    )
    total_magnetization_normalized_vol_max: float | None = Field(
        None, description="Maximum normalized total magnetization in Bohr magnetons/Å^3"
    )
    total_magnetization_normalized_vol_min: float | None = Field(
        None, description="Minimum normalized total magnetization in Bohr magnetons/Å^3"
    )
    total_magnetization_normalized_formula_units_max: float | None = Field(
        None,
        description="Maximum normalized total magnetization in Bohr magnetons/formula unit",
    )
    total_magnetization_normalized_formula_units_min: float | None = Field(
        None,
        description="Minimum normalized total magnetization in Bohr magnetons/formula unit",
    )
    num_magnetic_sites_max: int | None = Field(
        None, description="Maximum number of magnetic sites"
    )
    num_magnetic_sites_min: int | None = Field(
        None, description="Minimum number of magnetic sites"
    )
    num_magnetic_sites: int | None = Field(
        None, description="Query for num_magnetic_sites being equal to an exact value"
    )
    num_magnetic_sites_not_eq: int | None = Field(
        None,
        description="Query for num_magnetic_sites not being equal to an exact value",
    )
    num_magnetic_sites_eq_any: int | None = Field(
        None,
        description="Query for num_magnetic_sites being equal to any value in a comma separated list",
    )
    num_magnetic_sites_neq_any: int | None = Field(
        None,
        description="Query for num_magnetic_sites not being equal to any value in a comma separated list",
    )
    num_unique_magnetic_sites_max: int | None = Field(
        None, description="Maximum number of unique magnetic sites"
    )
    num_unique_magnetic_sites_min: int | None = Field(
        None, description="Minimum number of unique magnetic sites"
    )
    num_unique_magnetic_sites_not_eq: int | None = Field(
        None,
        description="Query for num_unique_magnetic_sites not being equal to an exact value",
    )
    num_unique_magnetic_sites_eq_any: int | None = Field(
        None,
        description="Query for num_unique_magnetic_sites being equal to any value in a comma separated list",
    )
    k_voigt_max: float | None = Field(
        None, description="Maximum Voigt bulk modulus in GPa"
    )
    k_voigt_min: float | None = Field(
        None, description="Minimum Voigt bulk modulus in GPa"
    )
    k_reuss_max: float | None = Field(
        None, description="Maximum Reuss bulk modulus in GPa"
    )
    k_reuss_min: float | None = Field(
        None, description="Minimum Reuss bulk modulus in GPa"
    )
    k_vrh_max: float | None = Field(
        None, description="Maximum Voigt-Reuss-Hill bulk modulus in GPa"
    )
    k_vrh_min: float | None = Field(
        None, description="Minimum Voigt-Reuss-Hill bulk modulus in GPa"
    )
    g_voigt_max: float | None = Field(
        None, description="Maximum Voigt shear modulus in GPa"
    )
    g_voigt_min: float | None = Field(
        None, description="Minimum Voigt shear modulus in GPa"
    )
    g_reuss_max: float | None = Field(
        None, description="Maximum Reuss shear modulus in GPa"
    )
    g_reuss_min: float | None = Field(
        None, description="Minimum Reuss shear modulus in GPa"
    )
    g_vrh_max: float | None = Field(
        None, description="Maximum Voigt-Reuss-Hill shear modulus in GPa"
    )
    g_vrh_min: float | None = Field(
        None, description="Minimum Voigt-Reuss-Hill shear modulus in GPa"
    )
    universal_anisotropy_max: float | None = Field(
        None, description="Maximum universal anisotropy"
    )
    universal_anisotropy_min: float | None = Field(
        None, description="Minimum universal anisotropy"
    )
    homogeneous_poisson_max: float | None = Field(
        None, description="Maximum homogeneous Poisson ratio"
    )
    homogeneous_poisson_min: float | None = Field(
        None, description="Minimum homogeneous Poisson ratio"
    )
    e_total_max: float | None = Field(None, description="Maximum total energy in eV")
    e_total_min: float | None = Field(None, description="Minimum total energy in eV")
    e_ionic_max: float | None = Field(None, description="Maximum ionic energy in eV")
    e_ionic_min: float | None = Field(None, description="Minimum ionic energy in eV")
    e_electronic_max: float | None = Field(
        None, description="Maximum electronic energy in eV"
    )
    e_electronic_min: float | None = Field(
        None, description="Minimum electronic energy in eV"
    )
    n_max: int | None = Field(
        None, description="Maximum value for the refractive index"
    )
    n_min: int | None = Field(
        None, description="Minimum value for the refractive index"
    )
    e_ij_max_max: float | None = Field(
        None, description="Maximum maximum pairwise energy in eV"
    )
    e_ij_max_min: float | None = Field(
        None, description="Minimum maximum pairwise energy in eV"
    )
    weighted_surface_energy_EV_PER_ANG2_max: float | None = Field(
        None, description="Maximum weighted surface energy in eV/Å^2"
    )
    weighted_surface_energy_EV_PER_ANG2_min: float | None = Field(
        None, description="Minimum weighted surface energy in eV/Å^2"
    )
    weighted_surface_energy_max: float | None = Field(
        None, description="Maximum weighted surface energy in J/m^2"
    )
    weighted_surface_energy_min: float | None = Field(
        None, description="Minimum weighted surface energy in J/m^2"
    )
    weighted_work_function_max: float | None = Field(
        None, description="Maximum weighted work function in eV"
    )
    weighted_work_function_min: float | None = Field(
        None, description="Minimum weighted work function in eV"
    )
    surface_anisotropy_max: float | None = Field(
        None, description="Maximum surface anisotropy"
    )
    surface_anisotropy_min: float | None = Field(
        None, description="Minimum surface anisotropy"
    )
    shape_factor_max: float | None = Field(None, description="Maximum shape factor")
    shape_factor_min: float | None = Field(None, description="Minimum shape factor")
    has_reconstructed: bool | None = Field(
        None, description="Whether the material has a reconstructed surface"
    )
    has_props: list[HasProps | str] | None = Field(
        None,
        description="List of possible properties given by HasProps enum to search for.",
    )
    deprecated: bool | None = Field(
        None, description="Whether the material is deprecated"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page
    # _per_page
    # _skip
    limit: int | None = Field(
        default=5, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,composition,nsites,symmetry",
        description="Comma-delimited list of fields to return in results. Fields include: 'builder_meta', 'nsites', 'elements', 'nelements', 'composition', 'composition_reduced', 'formula_pretty', 'formula_anonymous', 'chemsys', 'volume', 'density', 'density_atomic', 'symmetry', 'property_name', 'material_id', 'deprecated', 'deprecation_reasons', 'last_updated', 'origins', 'warnings', 'structure', 'task_ids', 'uncorrected_energy_per_atom', 'energy_per_atom', 'formation_energy_per_atom', 'energy_above_hull', 'is_stable', 'equilibrium_reaction_energy_per_atom', 'decomposes_to', 'xas', 'grain_boundaries', 'band_gap', 'cbm', 'vbm', 'efermi', 'is_gap_direct', 'is_metal', 'es_source_calc_id', 'bandstructure', 'dos', 'dos_energy_up', 'dos_energy_down', 'is_magnetic', 'ordering', 'total_magnetization', 'total_magnetization_normalized_vol', 'total_magnetization_normalized_formula_units', 'num_magnetic_sites', 'num_unique_magnetic_sites', 'types_of_magnetic_species', 'bulk_modulus', 'shear_modulus', 'universal_anisotropy', 'homogeneous_poisson', 'e_total', 'e_ionic', 'e_electronic', 'n', 'e_ij_max', 'weighted_surface_energy_EV_PER_ANG2', 'weighted_surface_energy', 'weighted_work_function', 'surface_anisotropy', 'shape_factor', 'has_reconstructed', 'possible_species', 'has_props', 'theoretical', 'database_IDs'",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class StructureSchema(SummarySchema):
    limit: int | None = Field(
        default=5, description="Maximum number of entries to return", requried=True
    )
    fields: str | None = Field(
        default="material_id,structure,",
        description="Comma-delimited list of fields to return in results. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `structure` `task_ids` `uncorrected_energy_per_atom` `energy_per_atom` `formation_energy_per_atom` `energy_above_hull` `is_stable` `equilibrium_reaction_energy_per_atom` `decomposes_to` `xas` `grain_boundaries` `band_gap` `cbm` `vbm` `efermi` `is_gap_direct` `is_metal` `es_source_calc_id` `bandstructure` `dos` `dos_energy_up` `dos_energy_down` `is_magnetic` `ordering` `total_magnetization` `total_magnetization_normalized_vol` `total_magnetization_normalized_formula_units` `num_magnetic_sites` `num_unique_magnetic_sites` `types_of_magnetic_species` `k_voigt` `k_reuss` `k_vrh` `g_voigt` `g_reuss` `g_vrh` `universal_anisotropy` `homogeneous_poisson` `e_total` `e_ionic` `e_electronic` `n` `e_ij_max` `weighted_surface_energy_EV_PER_ANG2` `weighted_surface_energy` `weighted_work_function` `surface_anisotropy` `shape_factor` `has_reconstructed` `possible_species` `has_props` `theoretical` `database_IDs`",
    )
    return_mode: str | None = Field(
        default="file",
        description="Return mode for the structure. Options are 'text' or 'file'",
    )


class ElasticitySchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    k_voigt_max: float | None = Field(
        None,
        description="Maximum value for the Voigt average of the bulk modulus in GPa",
    )
    k_voigt_min: float | None = Field(
        None,
        description="Minimum value for the Voigt average of the bulk modulus in GPa",
    )
    k_reuss_max: float | None = Field(
        None,
        description="Maximum value for the Reuss average of the bulk modulus in GPa",
    )
    k_reuss_min: float | None = Field(
        None,
        description="Minimum value for the Reuss average of the bulk modulus in GPa",
    )
    k_vrh_max: float | None = Field(
        None,
        description="Maximum value for the Voigt-Reuss-Hill average of the bulk modulus in GPa",
    )
    k_vrh_min: float | None = Field(
        None,
        description="Minimum value for the Voigt-Reuss-Hill average of the bulk modulus in GPa",
    )
    g_voigt_max: float | None = Field(
        None,
        description="Maximum value for the Voigt average of the shear modulus in GPa",
    )
    g_voigt_min: float | None = Field(
        None,
        description="Minimum value for the Voigt average of the shear modulus in GPa",
    )
    g_reuss_max: float | None = Field(
        None,
        description="Maximum value for the Reuss average of the shear modulus in GPa",
    )
    g_reuss_min: float | None = Field(
        None,
        description="Minimum value for the Reuss average of the shear modulus in GPa",
    )
    g_vrh_max: float | None = Field(
        None,
        description="Maximum value for the Voigt-Reuss-Hill average of the shear modulus in GPa",
    )
    g_vrh_min: float | None = Field(
        None,
        description="Minimum value for the Voigt-Reuss-Hill average of the shear modulus in GPa",
    )
    elastic_anisotropy_max: float | None = Field(
        None, description="Maximum value for the elastic anisotropy"
    )
    elastic_anisotropy_min: float | None = Field(
        None, description="Minimum value for the elastic anisotropy"
    )
    poisson_max: float | None = Field(
        None, description="Maximum value for the Poisson ratio"
    )
    poisson_min: float | None = Field(
        None, description="Minimum value for the Poisson ratio"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=5,
        description="Max number of entries to return in a single query. Limited to 1000.",
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,elastic_tensor",
        description="Fields to project from ElasticityDoc as a list of comma separated strings. Fields include: 'material_id' 'formula_pretty' 'elastic_tensor' 'builder_meta', 'nsites', 'elements', 'nelements', 'composition', 'composition_reduced', 'formula_anonymous', 'chemsys', 'volume', 'density', 'density_atomic', 'symmetry', 'property_name', 'deprecated', 'deprecation_reasons', 'last_updated', 'origins', 'warnings', 'structure', 'order', 'compliance_tensor', 'bulk_modulus', 'shear_modulus', 'sound_velocity', 'thermal_conductivity', 'young_modulus', 'universal_anisotropy', 'homogeneous_poisson', 'debye_temperature', 'fitting_data', 'fitting_method', 'state'",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class SynthesisSchema(BaseModel):
    keywords: str | None = Field(
        None,
        description="Comma-delimited list of keywords to search synthesis paragraph text with",
    )
    synthesis_type: str | None = Field(
        None,
        description="Comma-delimited list of synthesis types to include. Options include: 'solid_state', 'sol_gel'",
    )
    target_formula: str | None = Field(
        None, description="Chemical formula of the target material"
    )
    precursor_formula: str | None = Field(
        None, description="Chemical formula of the precursor material"
    )
    operations: str | None = Field(
        None,
        description="Comma-delimited list of operations that syntheses must have. Options include: 'starting', 'mixing', 'shaping', 'drying', 'heating', 'quenching'",
    )
    condition_heating_temperature_max: float | None = Field(
        None, description="Maximum heating temperature in K"
    )
    condition_heating_temperature_min: float | None = Field(
        None, description="Minimum heating temperature in K"
    )
    condition_heating_time_max: float | None = Field(
        None, description="Maximum heating time in hours"
    )  # TODO: check if this is correct
    condition_heating_time_min: float | None = Field(
        None, description="Minimum heating time in hours"
    )
    condition_heating_atmosphere: str | None = Field(
        None,
        description="Comma-delimited list of required heating atmospheres",
        examples=[
            "air",
            "oxygen",
            "argon",
            "nitrogen",
            "hydrogen",
            "vacuum",
            "nirogen-oxygen",
        ],  # TODO: check if the example is the intended format
    )
    condition_mixing_device: str | None = Field(
        None,
        description="Comma-delimited list of required mixing devices",
        examples=["zirconia", "Al2O3", "zirconia-Al2O3"],
    )
    condition_mixing_media: str | None = Field(
        None,
        description="Comma-delimited list of required mixing media",
        examples=["alcohol", "water"],
    )
    limit: int | None = Field(
        default=5,
        description="Maximum number of entries to return",
    )

class SynthesisOperation(BaseModel):
    reaction: str | None = Field(None, description="Reaction equation of this operation")
    details: str | None = Field(None, description="Text details (conditions, instruments, time, etc.) of this operation")

class SynthesisRecipe(BaseModel):
    doi: str | None = Field(..., description="DOI of the synthesis recipe")
    methods: list[str] | None = Field(None, description="List of methods/techniques used in the synthesis recipe")
    operations: list[SynthesisOperation]

class ThermoSchema(BaseModel):
    thermo_ids: str | None = Field(
        None, description="Comma-separated list of thermo_ids to query on"
    )
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_id to query on"
    )
    thermo_types: list[ThermoType | str] | None = Field(
        default=[ThermoType.R2SCAN],
        description=f"List of thermo types to query on: {', '.join([t.value for t in ThermoType]) }",
    )
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    is_stable: bool | None = Field(None, description="Whether the material is stable")
    nsites_max: int | None = Field(None, description="Maximum number of sites")
    nsites_min: int | None = Field(None, description="Minimum number of sites")
    nsites: int | None = Field(
        None, description="Query for nsites being equal to an exact value"
    )
    nsites_not_eq: int | None = Field(
        None, description="Query for nsites not being equal to an exact value"
    )
    nsites_eq_any: int | None = Field(
        None,
        description="Query for nsites being equal to any value in a comma separated list",
    )
    nsites_neq_any: int | None = Field(
        None,
        description="Query for nsites not being equal to any value in a comma separated list",
    )
    nelements_max: int | None = Field(None, description="Maximum number of elements")
    nelements_min: int | None = Field(None, description="Minimum number of elements")
    nelements: int | None = Field(
        None, description="Query for nelements being equal to an exact value"
    )
    nelements_not_eq: int | None = Field(
        None, description="Query for nelements not being equal to an exact value"
    )
    nelements_eq_any: int | None = Field(
        None,
        description="Query for nelements being equal to any value in a comma separated list",
    )
    nelements_neq_any: int | None = Field(
        None,
        description="Query for nelements not being equal to any value in a comma separated list",
    )
    volume_max: float | None = Field(None, description="Maximum volume in Å^3")
    volume_min: float | None = Field(None, description="Minimum volume in Å^3")
    density_max: float | None = Field(None, description="Maximum density in g/cm^3")
    density_min: float | None = Field(None, description="Minimum density in g/cm^3")
    density_atomic_max: float | None = Field(
        None, description="Maximum atomic density in atoms/Å^3"
    )
    density_atomic_min: float | None = Field(
        None, description="Minimum atomic density in atoms/Å^3"
    )
    uncorrected_energy_per_atom_max: float | None = Field(
        None, description="Maximum uncorrected energy per atom in eV/atom"
    )
    uncorrected_energy_per_atom_min: float | None = Field(
        None, description="Minimum uncorrected energy per atom in eV/atom"
    )
    energy_per_atom_max: float | None = Field(
        None, description="Maximum energy per atom in eV/atom"
    )
    energy_per_atom_min: float | None = Field(
        None, description="Minimum energy per atom in eV/atom"
    )
    formation_energy_per_atom_max: float | None = Field(
        None, description="Maximum formation energy per atom in eV/atom"
    )
    formation_energy_per_atom_min: float | None = Field(
        None, description="Minimum formation energy per atom in eV/atom"
    )
    energy_above_hull_max: float | None = Field(
        None, description="Maximum energy above hull in eV/atom"
    )
    energy_above_hull_min: float | None = Field(
        None, description="Minimum energy above hull in eV/atom"
    )
    equilibrium_reaction_energy_per_atom_max: float | None = Field(
        None, description="Maximum equilibrium reaction energy per atom in eV/atom"
    )
    equilibrium_reaction_energy_per_atom_min: float | None = Field(
        None, description="Minimum equilibrium reaction energy per atom in eV/atom"
    )
    decomposition_enthalpy_max: float | None = Field(
        None, description="Maximum decomposition enthalpy in eV/atom"
    )
    decomposition_enthalpy_min: float | None = Field(
        None, description="Minimum decomposition enthalpy in eV/atom"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=10, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,thermo_id,formula_pretty,thermo_type,uncorrected_energy_per_atom,formation_energy_per_atom,energy_above_hull,decomposes_to",
        description="Fields to project from ThermoDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `thermo_type` `thermo_id` `uncorrected_energy_per_atom` `energy_per_atom` `energy_uncertainy_per_atom` `formation_energy_per_atom` `energy_above_hull` `is_stable` `equilibrium_reaction_energy_per_atom` `decomposes_to` `decomposition_enthalpy` `decomposition_enthalpy_decomposes_to` `energy_type` `entry_types` `entries`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class MagnetismSchema(BaseModel):
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    total_magnetization_max: float | None = Field(
        None, description="Maximum total magnetization in Bohr magnetons"
    )
    total_magnetization_min: float | None = Field(
        None, description="Minimum total magnetization in Bohr magnetons"
    )
    total_magnetization_normalized_vol_max: float | None = Field(
        None, description="Maximum normalized total magnetization in Bohr magnetons/Å^3"
    )
    total_magnetization_normalized_vol_min: float | None = Field(
        None, description="Minimum normalized total magnetization in Bohr magnetons/Å^3"
    )
    total_magnetization_normalized_formula_units_max: float | None = Field(
        None,
        description="Maximum normalized total magnetization in Bohr magnetons/formula unit",
    )
    total_magnetization_normalized_formula_units_min: float | None = Field(
        None,
        description="Minimum normalized total magnetization in Bohr magnetons/formula unit",
    )
    num_magnetic_sites_max: int | None = Field(
        None, description="Maximum number of magnetic sites"
    )
    num_magnetic_sites_min: int | None = Field(
        None, description="Minimum number of magnetic sites"
    )
    num_unique_magnetic_sites_max: int | None = Field(
        None, description="Maximum number of unique magnetic sites"
    )
    num_unique_magnetic_sites_min: int | None = Field(
        None, description="Minimum number of unique magnetic sites"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=10, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,ordering,total_magnetization,exchange_symmetry,types_of_magnetic_species,magmoms",
        description="Fields to project from MagnetismDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `ordering` `is_magnetic` `exchange_symmetry` `num_magnetic_sites` `num_unique_magnetic_sites` `types_of_magnetic_species` `magmoms` `total_magnetization` `total_magnetization_normalized_vol` `total_magnetization_normalized_formula_units`",
        # examples=["material_id,formula_pretty,ordering,total_magnetization,exchange_symmetry,types_of_magnetic_species,magmoms"]
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class DielectricSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    e_total_max: float | None = Field(
        None, description="Maximum total dielectric constant"
    )
    e_total_min: float | None = Field(
        None, description="Minimum total dielectric constant"
    )
    e_ionic_max: float | None = Field(
        None, description="Maximum ionic dielectric constant"
    )
    e_ionic_min: float | None = Field(
        None, description="Minimum ionic dielectric constant"
    )
    e_electronic_max: float | None = Field(
        None, description="Maximum electronic dielectric constant"
    )
    e_electronic_min: float | None = Field(
        None, description="Minimum electronic dielectric constant"
    )
    n_max: int | None = Field(
        None, description="Maximum value for the refractive index"
    )
    n_min: int | None = Field(
        None, description="Minimum value for the refractive index"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=10,
        description="Maximum number of entries to return",
    )
    fields: str | None = Field(
        description="Fields to project from DielectricDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `total` `ionic` `electronic` `e_total` `e_ionic` `e_electronic` `n`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class PiezoSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    piezo_modulus_max: str | None = Field(
        None, description="Maximum piezoelectric modulus in C/m^2"
    )
    piezo_modulus_min: str | None = Field(
        None, description="Minimum piezoelectric modulus in C/m^2"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=10, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        description="Fields to project from PiezoDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `total` `ionic` `electronic` `e_ij_max` `max_direction` `strain_for_max`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class SimilaritySchema(BaseModel):
    material_id: str = Field(description="Material ID to find similar materials to")
    fields: str | None = Field(
        default="sim,material_id",
        description="Fields to project from SimilarityDoc as a list of comma-delimited strings. Field include: `sim` `material_id`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class RobocrysSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    keywords: str | None = Field(
        None,
        description="Comma-delimited list of keywords to search robocrystallographer description text with",
    )
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=5, description="Maximum number of entries to return"
    )


class OxidationSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    formual: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    possible_species: str | None = Field(
        None,
        description="Comma-delimited list of possible oxidation states to query on",
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=5, description="Maximum number of entries to return"
    )
    fields: str = Field(
        description="Fields to project from OxidationStateDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `structure` `possible_species` `possible_valences` `average_oxidation_states` `method`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class BondsSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    max_bond_length_max: float | None = Field(
        None, description="Maximum value for the maximum bond length in Å"
    )
    max_bond_length_min: float | None = Field(
        None, description="Minimum value for the maximum bond length in Å"
    )
    min_bond_length_max: float | None = Field(
        None, description="Maximum value for the minimum bond length in Å"
    )
    min_bond_length_min: float | None = Field(
        None, description="Minimum value for the minimum bond length in Å"
    )
    mean_bond_length_max: float | None = Field(
        None, description="Maximum value for the mean bond length in Å"
    )
    mean_bond_length_min: float | None = Field(
        None, description="Minimum value for the mean bond length in Å"
    )
    coordination_envs: str | None = Field(
        None,
        description="Comma-delimited list of coordination environments to query on",
    )
    coordination_envs_anonymous: str | None = Field(
        None,
        description="Comma-delimited list of anonymous coordination environments to query on",
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=10, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,coordination_envs,max_bond_length,min_bond_length,mean_bond_length",
        description="Fields to project from BondDoc as a list of comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `property_name` `material_id` `deprecated` `deprecation_reasons` `last_updated` `origins` `warnings` `structure` `max_bond_length` `min_bond_length` `mean_bond_length` `coordination_envs` `coordination_envs_anonymous`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class TasksSchema(BaseModel):
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    elements: str | None = Field(
        None, description="A comma delimited string list of elements to query on"
    )
    exclude_elements: str | None = Field(
        None, description="A comma delimited string list of elements to exclude"
    )
    task_ids: str | None = Field(
        None, description="Comma-separated list of task_ids to query on"
    )
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    # _page: int = Field(description="Page number to request (takes precedent over _limit and _skip)")
    # _per_page: int = Field(description="Number of entries to show per page (takes precedent over _limit and _skip). Limited to 1000")
    # _skip: int = Field(description="Number of entries to skip")
    limit: int | None = Field(
        default=3, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,composition,task_ids",
        description="Fields to project from TaskDoc as comma separated strings. Fields include: `builder_meta` `nsites` `elements` `nelements` `composition` `composition_reduced` `formula_pretty` `formula_anonymous` `chemsys` `volume` `density` `density_atomic` `symmetry` `tags` `dir_name` `state` `calcs_reversed` `structure` `task_type` `task_id` `orig_inputs` `input` `output` `included_objects` `vasp_objects` `entry` `task_label` `author` `icsd_id` `transformations` `additional_json` `custodian` `analysis` `last_updated`",
    )
    all_fields: bool | None = Field(
        False, description="Whether to return all fields in results"
    )


class ElectronicSchema(BaseModel):
    material_ids: str | None = Field(
        None, description="Comma-separated list of material_ids to query on"
    )
    band_gap_max: float | None = Field(None, description="Maximum band gap in eV")
    band_gap_min: float | None = Field(None, description="Minimum band gap in eV")
    chemsys: str | None = Field(
        None,
        description="A comma delimited string list of chemical systems. Wildcards for unknown elements only supported for single chemsys queries",
    )
    formula: str | None = Field(
        None,
        description="Query by formula including anonymized formula or by including wild cards. A comma delimited string list of anonymous formulas or regular formulas can also be provided.",
    )
    elements: str | None = Field(
        None, description="A comma delimited string list of elements to query on"
    )
    exclude_elements: str | None = Field(
        None, description="A comma delimited string list of elements to exclude"
    )
    efermi_max: float | None = Field(None, description="Maximum Fermi energy in eV")
    efermi_min: float | None = Field(None, description="Minimum Fermi energy in eV")
    magnetic_ordering: Ordering | None = Field(
        None, description="Magnetic ordering: FM, AFM, FiM, NM, Unknown"
    )
    nelements_max: int | None = Field(None, description="Maximum number of elements")
    nelements_min: int | None = Field(None, description="Minimum number of elements")
    is_gap_direct: bool | None = Field(
        None, description="Whether the band gap is direct"
    )
    is_metal: bool | None = Field(None, description="Whether the material is a metal")
    sort_fields: str | None = Field(
        None,
        description="Comma-delimited list of fields to sort on. Prefix with - for descending order.",
    )
    limit: int | None = Field(
        default=10, description="Maximum number of entries to return"
    )
    fields: str | None = Field(
        default="material_id,formula_pretty,band_gap,efermi,is_gap_direct,is_metal,magnetic_ordering",
        description="Fields to project from ElectronicStructureDoc as comma separated strings. Fields include: 'task_id', 'band_gap', 'cbm', 'vbm', 'efermi', 'is_gap_direct', 'is_metal', 'magnetic_ordering', 'builder_meta', 'nsites', 'elements', 'nelements', 'composition', 'composition_reduced', 'formula_pretty', 'formula_anonymous', 'chemsys', 'volume', 'density', 'density_atomic', 'symmetry', 'property_name', 'material_id', 'deprecated', 'deprecation_reasons', 'last_updated', 'origins', 'warnings', 'bandstructure', 'dos'",
    )
