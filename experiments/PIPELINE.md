## Usage

This project consists of three main parts:
1. **Defining the experiment configuration in `config.py`**
2. **Creating a dataset with `dataset.py`**
3. **Running the experiment with `prompting.py`**

### Configuring the Experiment

The `config.py` file contains the `PromptingConfig` class, which defines various configuration options for your experiment, such as the task number, models to use, and the path to the dataset CSV file.

You should edit this file to set the desired configuration for your experiment before running `dataset.py` and `prompting.py`.

You can edit the evaluator model prompt, which gpt model to used, and your apis in `config.py`.


### Creating a Dataset

The `dataset.py` script is used to create a CSV file that contains the dataset for your experiment, containing . You can specify the prompt structure and the size of the dataset in `dataset.py`.

The current default prompt: 
f"""What is the magnetic ordering of {formula}? If there are multiple magnetic orderings, please give me the most stable one with its material id, space group, and magnetization per formula unit.
        After you reason through, please output it in the format of python dictionary below
        
        "magnetic_ordering": [your answer for mass density],
        "magnetization_per_formula_unit": [your answer for magnetization per formula unit],
        "material_id": [your answer for material_id],

        Tips:
        1. don't include the calculation process, only include the answers in one sentence

"""
Without specifying the output format, the evaluator model had a hardtime to extract the required information. 

To create the dataset, simply run:

```bash
python dataset.py
```

This will generate a CSV file in the `cache` directory with a name based on the task number and dataset size (small or full).

### Running the Experiment

After configuring the experiment and creating the dataset, you can run the experiment with:

```bash
python prompting.py
```

This script will load the configuration from `config.py`, load the dataset from the CSV file, and perform the experiment as defined by your configuration. The results will be e saved to a CSV file you created with `dataset.py`.