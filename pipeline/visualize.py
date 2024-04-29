
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib.ticker import FuncFormatter

def plot_setup(ratio=1, column_frac=1):
    
    plt.rcParams['font.family'] = 'STIXGeneral'
    # Alternatively, to specifically use serif fonts, you can use 'STIXGeneral'
    plt.rcParams['mathtext.fontset'] = 'stix'

    textwidth_in_inches = 6.75  # Full text width
    columnsep_in_inches = 0.25  # Column separation
    columnwidth_in_inches = (textwidth_in_inches - columnsep_in_inches) / 2
    # figure_width = textwidth_in_inches 
    figure_width = columnwidth_in_inches * column_frac
    figure_height = figure_width * ratio 
    # plt.figure(figsize=(figure_width, figure_height))
    ax, fig = plt.subplots(figsize=(figure_width, figure_height))

    # Set the style to "paper"
    sns.set_context("paper")

    # Enable dark grid
    sns.set_style("darkgrid")

    sns.color_palette('muted')

    plt.rcParams['figure.constrained_layout.use'] = True
    # plt.rcParams['font.family'] = 'Times New Roman'
    return ax, fig

def plot_done(name):
    name = name.replace(" ", "_")
    directory = "./saved_graphs"
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist
    plt.savefig(f"./saved_graphs/{name}.pdf", format='pdf')
    print(f"Saved graph to {directory}/{name}.pdf")
    plt.show()

def task7_regression(data, task):
    # plot_setup(ratio=1, column_frac=1)
    #ordering, llamp_magnetic_ordering, gpt_magnetic_ordering
    sns.scatterplot(data=data, x=f'{task}', y=f'llamp_{task}', color='red', label=f'LLAMP for {task}')
    sns.scatterplot(data=data, x=f'{task}', y=f'gpt_{task}', color='green', label=f'GPT for {task}')
    ax = plt.gca()
    ax.axline([0, 0], [1, 1], color='blue', linestyle='--', linewidth=2)

    plt.xlabel('Groud Truth')
    plt.ylabel(f"{task}")
    plt.legend()
    plot_done(f"{task}")

from sklearn.metrics import confusion_matrix
def task6_conf_mat(data):
    # plot_setup(ratio=1, column_frac=1)
    data = data.replace({'': 'N/A', 'N/A': 'N/A', 'N/A': 'N/A', np.nan: 'N/A'})
    actual_mapped = data["ordering"]
    predicted1_mapped = data["llamp_magnetic_ordering"]
    predicted2_mapped = data["gpt_magnetic_ordering"]
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    # {'FM', 'AFM', nan, 'FiM', 'NM'}
    categories = ['FM', 'AFM', 'N/A', 'FiM', 'NM']

    # Llamp Confusion Matrix
    cm1 = confusion_matrix(predicted1_mapped, actual_mapped, labels=categories)
    cm2 = confusion_matrix(predicted2_mapped, actual_mapped, labels=categories)
    cm1_normalized = confusion_matrix(predicted1_mapped, actual_mapped, labels=categories, normalize='true')
    cm2_normalized = confusion_matrix(predicted2_mapped, actual_mapped, labels=categories, normalize='true')
    sns.heatmap(cm1_normalized, annot=cm1, fmt="d", cmap='Blues', xticklabels=categories, yticklabels=categories, ax=ax[0])
    ax[0].set_title('Llamp Confusion Matrix')
    ax[0].set_xlabel('Actual Labels')
    ax[0].set_ylabel('Predicted Labels')

    # GPT3.5 Confusion Matrix
    sns.heatmap(cm2_normalized, annot=cm2, fmt="d", cmap='Blues', xticklabels=categories, yticklabels=categories, ax=ax[1])
    ax[1].set_title('GPT3.5 Confusion Matrix')
    ax[1].set_xlabel('Actual Labels')
    ax[1].set_ylabel('Predicted Labels')

    task = "confusion matrix"
    plot_done(f"{task}")

from sklearn.metrics import accuracy_score, precision_score, f1_score
def task6_table(data, task):
    data = data.replace({'': 'N/A', 'N/A': 'N/A', 'N/A': 'N/A', np.nan: 'N/A'})
    if task == "mp_id":
        actual = data[f"material_id"]
    elif task == "magnetic_ordering":
        actual = data[f"ordering"]
    predicted1 = data[f"llamp_{task}"]
    predicted2 = data[f"gpt_{task}"]

    # Llamp
    accuracy1 = accuracy_score(actual, predicted1)
    # Set average='macro' for multi-class classification
    precision1 = precision_score(actual, predicted1, average='macro', zero_division=0)
    f1_score1 = f1_score(actual, predicted1, average='macro', zero_division=0)
    
    # GPT3.5
    accuracy2 = accuracy_score(actual, predicted2)
    precision2 = precision_score(actual, predicted2, average='macro', zero_division=0)
    f1_score2 = f1_score(actual, predicted2, average='macro', zero_division=0)
    

    print({
        f"Llamp {task} prediction": {"Accuracy": accuracy1, "Precision": precision1, "F1 Score": f1_score1},
        f"GPT3.5 {task} prediction": {"Accuracy": accuracy2, "Precision": precision2, "F1 Score": f1_score2}
    })

def task6_magnetization_unit(data, task):
    # TODO: do regression on it
    sns.scatterplot(data=data, x=f'{task}', y=f'llamp_{task}', color='red', label=f'LLAMP for {task}')
    sns.scatterplot(data=data, x=f'{task}', y=f'gpt_{task}', color='green', label=f'GPT for {task}')
    ax = plt.gca()
    ax.axline([0, 0], [1, 1], color='blue', linestyle='--', linewidth=2)

    plt.xlabel('Groud Truth')
    plt.ylabel(f"{task}")
    plt.legend()
    plot_done(f"{task}")
    



df = pd.read_csv("cache/6_eval_dataset.csv")
# df = df.iloc[:800]

############################ Benchmark 6 ############################
# task6_conf_mat(df)
task = "mp_id" 
# task = "magnetic_ordering"
task6_table(df, task)

############################ Benchmark 7 ############################
# task = "density"
# task = "volume"

# Numeral Task Preprocessing
# df = df.replace({'': 0, 'N/A': 0, None: 0, np.nan: 0})
# filtered_df = df[(df[f'gpt_{task}'] <= 100) & (df[f'{task}'] <= 100) & (df[f'llamp_{task}'] <= 100)]
# task7_regression(filtered_df, task)

