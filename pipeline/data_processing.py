import pandas as pd
import re
from query_llm import construct_openai_message, call_openai

csv_file = "cache/6_eval_dataset_gpt4.csv"
df = pd.read_csv(csv_file)

####################### regex filltering #######################
def regex(df):
    def extract_numerical_value(cell):
        if isinstance(cell, str):  # Check if cell is a string
            numerical_value = re.findall(r"[-+]?\d*\.\d+|\d+", cell)  # Extracts numerical values using regex
            if numerical_value:  # Check if any numerical value is found
                return float(numerical_value[0])  # Convert the extracted value to float
        return cell

    # Apply the function to the 'magnetization' column
    df['gpt_magnetization_unit'] = df['gpt_magnetization_unit'].apply(extract_numerical_value)
    df['llamp_magnetization_unit'] = df['llamp_magnetization_unit'].apply(extract_numerical_value)
    return df

####################### dropping columns #######################
def col(df):
    df.drop(columns=["llamp_output", "gpt_output", "llamp_space_group", "llamp_lattice_parameters", "gpt_space_group", "gpt_lattice_parameters"], inplace=True)
    return df

def remove_tip(df):
    substring_to_remove = "Tips:\n        1. don't include the calculation process, only include the answers in one sentence"
    substring_to_remove= "μB"
    df = df.applymap(lambda x: x.replace(substring_to_remove, '').strip() if isinstance(x, str) else x)
    return df

def parse(df):
    """LLM Evalluator"""
    def llm_parse(data):
        if isinstance(data, str):
            data = data.replace('```python', '').replace('```json', '').replace('```', '').strip()
            prompt = """You are a language model evaluator that can extract data from the given language model output.

            You don't need to add your interpretation and don't correct the wrong information even if you know that's wrong.

            In the following task, you are required to extract the magnetic ordering, total magnetization normalized formula units, and material_id, which starts with mp-XXX.

            After you reason through the response and extract the magnetic ordering, total magnetization normalized formula units, and material_id,
            please output it in the format of dictionary below
            "
            {
                "magnetic_ordering": [extracted magnetic ordering, data_type=string],
                "total_magnetization_normalized_formula_units": [extracted total magnetization normalized formula units, data_type=float/int],
                "material_id": [extracted material_id,  data_type=string]
            }
            "

            Tip: 
            1. for magnetic_ordering, make sure the [extracted information] be acronym in the set: {'FiM', 'Unknown', 'NM', 'FM', 'AFM'}
            2. convert total_magnetization_normalized_formula_units's unit as μB and only include the float/int in the dictionary.
            3. if the response doesn't include the information you need to extract, put "N/A" string as [extracted information] and don't just output empty string

            Below is the response you need to extract the information specified above:

            Response: """
            try: 
                message_content = prompt + data
            except: 
                print("Config task number and eval_prompt mismatch")

            request_body = construct_openai_message(
                    message_content,
                    temperature=0,
                    max_tokens=1000,
                    model="gpt-4-turbo",
                )
            
            value = call_openai(request_body, "gpt-4-turbo")
            print("value", value)
            if "Unknown" in value or "N/A" in value or "python" in value:
                return data, data, data
            try: 
                mag_order, mag_unit, mp_id =  eval(value)["magnetic_ordering"], eval(value)["total_magnetization_normalized_formula_units"], eval(value)["material_id"]
                data = mag_order, mag_unit, mp_id
            except:
                breakpoint()
                data = data, data, data
        else: 
            data = data, data, data
        if len(data) != 3:
            breakpoint()
            data = data, data, data
        return data
    csv_file = "cache/6_eval_dataset_gpt4.csv"
    for index, row in df.iterrows():
        print("index: ", index)
        parsed_data = llm_parse(row['llamp_output'])
        df.at[index, 'llamp_magnetic_ordering'] = parsed_data[0]
        df.at[index, 'llamp_magnetization_unit'] = parsed_data[1]
        df.at[index, 'llamp_mp_id'] = parsed_data[2]
        if index % 20 == 0:
            df.to_csv(csv_file, index=False)
        
    # predicted2_mapped = data["gpt_magnetic_ordering"].apply(llm_parse)
    return df
    
    

    
df = parse(df)

# csv_file = "cache/6_eval_dataset_gpt4.csv"
# df.to_csv(csv_file, index=False)