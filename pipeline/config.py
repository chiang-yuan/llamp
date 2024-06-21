from dataclasses import dataclass, field


@dataclass
class PromptingConfig:
    task: int = 8
    gpt_model : str = "gpt-4-turbo-2024-04-09"
    # gpt_model : str = ""gpt-3.5-turbo-1106""
    evaluator_model : str = "gpt-3.5-turbo-1106"
    # TODO: Possible chice: "gpt-4-1106-preview", "gpt-4"
    type: str = "eval"
    csv_path: str = f"cache/{task}_{type}_dataset_gpt4.csv"
    # TODO: specify small or full dataset to use
    eval_prompt: dict = field(default_factory=lambda: {
        # 6: magnetism ordering benchmark, prompt: What is the magnetic ordering of {formula}? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit
        6: """You are a language model evaluator that can extract data from the given language model output.

        You don't need to add your interpretation and don't correct the wrong information even if you know that's wrong.

        In the following task, you are required to extract the magnetic ordering, total magnetization normalized formula units, and material_id, which starts with mp-XXX.

        After you reason through the response and extract the magnetic ordering, total magnetization normalized formula units, and material_id,
        please output it in the format of python dictionary below

        {
            "magnetic_ordering": [extracted magnetic ordering],
            "total_magnetization_normalized_formula_units": [extracted total magnetization normalized formula units],
            "material_id": [extracted material_id]
        }

        Tip: 
        1. for magnetic_ordering, make sure the [extracted information] be acronym in the set: {'FiM', 'Unknown', 'NM', 'FM', 'AFM'}
        2. convert total_magnetization_normalized_formula_units's unit as μB and only include the number in the dictionary.
        3. if the response doesn't include the information you need to extract, put "N/A" string as [extracted information] and don't just output empty string

        Below is the response you need to extract the information specified above:

        Response: """,
        # 7: material volume benchmark, prompt: Please give me the mass density (in g/cm^3) and volume per atom (in Angstrom^3/atom) of stable {formula}.
        7: """You are a language model evaluator that can extract data from the given language model output.

        You don't need to add your interpretation and don't correct the wrong information even if you know that's wrong.

        In the following task, you are required to extract mass density (in g/cm^3) and volume per atom (in Angstrom^3/atom) from the response you are given below

        After you reason through the response and extract the required information above, please output it in the format of python dictionary below

        {
        "mass_density": [extracted mass density],
        "volume": [extracted volume per atom],
        }

        Tip: 
        1. for mass density and volume per atom please only include the number in the dictionary instead of string.
        2. if the response doesn't include the information you need to extract, put "N/A" string as [extracted information] for that

        Below is the response you need to extract the information specified above:

        Response: """,
        # 8: Give me the space group of the ground state {formula} as well as its lattice parameters.
        8: """You are a language model evaluator that can extract data from the given language model output.

        You don't need to add your interpretation and don't correct the wrong information even if you know that's wrong.

        In the following task, you are required to extract space group and lattice parameters (a, b, c, ) from the response you are given below

        After you reason through the response and extract the required information above, please output it in the format of python dictionary below

        {
        "space_group": [extracted space group],
        "lattice_parameters": [extracted lattice_parameters],
        }

        Tip: 
        1. for space_group, please only include the string value.
        2. for lattice_parameters, please output an array of 6 numeric value.
        3. if the response doesn't include the information you need to extract, put "N/A" string as [extracted information] for that.

        Below is the response you need to extract the information specified above:

        Response: """,
    })


