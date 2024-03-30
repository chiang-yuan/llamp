from mp_api.client import MPRester
import csv
import random

MP_API_KEY ="NBKjdxICwx77pM1cLk9TU7fUQ93fjTIl"
with MPRester(MP_API_KEY) as mpr:

    summary_doc = mpr.materials.summary.search(
        is_stable=True,
        num_elements=[1,3],
        # material_ids=["mp-149", "mp-13", "mp-22526"],
        fields=["material_id", "formula_pretty", "total_magnetization_normalized_formula_units", "ordering"],
    )

def process_prompt(formula):
    return f"What is the magnetic ordering of {formula}? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit."

# summary_doc = list(summary_doc)
# random.shuffle(summary_doc)
# summary_doc = summary_doc[:100]
data_rows = [
    [process_prompt(doc.formula_pretty), doc.formula_pretty, doc.material_id, doc.total_magnetization_normalized_formula_units, doc.ordering]
    for doc in summary_doc
]

csv_file_path = 'cache/full_dataset.csv'
headers = ["prompt", "formula", "material_id", "total_magnetization_normalized_formula_units", "ordering"]

# Writing the data to a CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the column headers
    writer.writerows(data_rows)  # Write the data rows

print(f"Data has been successfully saved to {csv_file_path}.")
   