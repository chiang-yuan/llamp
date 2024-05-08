from mp_api.client import MPRester
from config import PromptingConfig
import csv
import random
import os
from dotenv import load_dotenv
load_dotenv() # it import the key from .env

def process_prompt(formula, config):
    if config.task == 6:
        # TODO: choose which prompt format to use
        return f"""What is the magnetic ordering of {formula}? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit.
        After you reason through, please output it in the format of python dictionary below.
        
        "magnetic_ordering": [your answer for mass density],
        "magnetization_per_formula_unit": [your answer for magnetization per formula unit],
        "material_id": [your answer for material_id],

        Tips:
        1. don't include the calculation process, only include the answers in one sentence

        """
        # return f"What is the magnetic ordering of {formula}? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit."
    elif config.task == 7:
        # TODO: choose which prompt format to use
        return f"""Please give me the mass density (in g/cm^3) and volume per atom (in Angstrom^3/atom) of stable {formula}. 
        After you reason through, please output it in the python dictionary format below.
        
        "mass_density": [your answer for mass density],
        "volume": [your answer for volume per atom],

        Tips:
        1. don't include the calculation process, only include the answers in one sentence
        
        """
        # return f"Please give me the mass density (in g/cm^3) and volume per atom (in Angstrom^3/atom) of stable {formula}. "
    elif config.task == 8:
        return f"""Give me the space group of the ground state {formula} as well as its lattice parameters
        space group should be one of 230 classes (string)
        lattice parameters should be 6 numbers (array of a, b, c, angle1, angle2, angle3)
        After you reason through, please output it in the python dictionary format below.
        
        "space_group": [your answer for mass density],
        "lattice_parameters": [your answer for volume per atom],

        Tips:
        1. don't include the calculation process, only include the answers in one sentence
        
        """
    else:
        raise NotImplementedError("This task hasn't been implemented yet.")
if __name__ == "__main__":
    config = PromptingConfig()
    MP_API_KEY = os.getenv("MP_API_KEY", None)
    
    with MPRester(MP_API_KEY) as mpr:

        summary_doc = mpr.materials.summary.search(
            is_stable=True,
            num_elements=[1,3],
            # material_ids=["mp-21166"],
            # material_ids=["mp-21166", "mp-149", "mp-13", "mp-22526"],
            fields=["material_id", "formula_pretty", "total_magnetization_normalized_formula_units", "ordering", "volume", "density", "nsites", "symmetry", "structure"],
        )


    summary_doc = list(summary_doc)
    random.shuffle(summary_doc)
    summary_doc = summary_doc[:1000]


    task_number = config.task
    type = "small" if len(summary_doc) == 10 else "full"
    type = "eval"
    csv_file_path = f'cache/{task_number}_{type}_dataset.csv'
    if task_number == 6:
        data_rows = [
        [process_prompt(doc.formula_pretty, config), doc.formula_pretty, doc.material_id, doc.total_magnetization_normalized_formula_units, doc.ordering]
        for doc in summary_doc
        ]
        headers = ["prompt", "formula", "material_id", "total_magnetization_normalized_formula_units", "ordering"]
    elif task_number == 7:
        data_rows = [
        [process_prompt(doc.formula_pretty, config), doc.formula_pretty, doc.material_id, doc.volume, doc.density, doc.nsites]
        for doc in summary_doc
        ]
        headers = ["prompt", "formula", "material_id", "volume", "density", "nsites"]
    elif task_number == 8:
        data_rows = [
        [process_prompt(doc.formula_pretty, config), doc.formula_pretty, doc.material_id, doc.structure.lattice.abc + doc.structure.lattice.angles, doc.symmetry.symbol ]
        for doc in summary_doc
        ]
        headers = ["prompt", "formula", "material_id", "space_group", "lattice_parameters"]
    else:
            raise NotImplementedError("This task hasn't been implemented yet.")

    # Writing the data to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the column headers
        writer.writerows(data_rows)  # Write the data rows

    print(f"Data has been successfully saved to {csv_file_path}.")
   