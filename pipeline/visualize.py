
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
    columnwidth_in_inches = (textwidth_in_inches - columnsep_in_inches) #/ 2
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

    # plt.rcParams['figure.constrained_layout.use'] = True
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
    plot_setup(ratio=1, column_frac=1)
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

# def task6_conf_mat(data):
#     data = data.replace({'': 'N/A', 'N/A': 'N/A', 'N/A': 'N/A', np.nan: 'N/A'})
#     actual_mapped = data["ordering"]
#     predicted1_mapped = data["llamp_magnetic_ordering"]
#     predicted2_mapped = data["gpt_magnetic_ordering"]
#     categories = ['FM', 'AFM', 'N/A', 'FiM', 'NM']

#     # Llamp Confusion Matrix
#     fig, ax = plot_setup()
#     cm1_normalized = confusion_matrix(predicted1_mapped, actual_mapped, labels=categories, normalize='true')
#     sns.heatmap(cm1_normalized, annot=True, fmt=".2f", cmap='Blues', xticklabels=categories, yticklabels=categories, ax=ax)
#     ax.set_title('Llamp Confusion Matrix')
#     ax.set_xlabel('Actual Labels')
#     ax.set_ylabel('Predicted Labels')
#     plot_done("llamp_confusion_matrix")

#     # GPT3.5 Confusion Matrix
#     fig, ax = plot_setup()
#     cm2_normalized = confusion_matrix(predicted2_mapped, actual_mapped, labels=categories, normalize='true')
#     sns.heatmap(cm2_normalized, annot=True, fmt=".2f", cmap='Blues', xticklabels=categories, yticklabels=categories, ax=ax)
#     ax.set_title('GPT3.5 Confusion Matrix')
#     ax.set_xlabel('Actual Labels')
#     ax.set_ylabel('Predicted Labels')
#     plot_done("gpt_confusion_matrix")


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

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
def task6_magnetization_unit(data):
    fig, ax = plot_setup()  # Initialize plot with the custom setup
    task = "magnetization_unit"
    sns.scatterplot(data=data, x=f'{task}', y=f'llamp_{task}', color='red', label=f'LLAMP for {task}', ax=ax)
    sns.scatterplot(data=data, x=f'{task}', y=f'gpt_{task}', color='green', label=f'GPT for {task}', ax=ax)
    ax.axline([0, 0], [1, 1], color='blue', linestyle='--', linewidth=2)

    ax.set_xlabel('Ground Truth')
    ax.set_ylabel(f"{task}")
    ax.legend()
    plot_done(f"{task}")

    # Calculate stats
    def mean_absolute_percentage_error(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-12))) * 100

    def root_mean_squared_log_error(y_true, y_pred):
        return np.sqrt(np.mean(np.square(np.log1p(y_pred) - np.log1p(y_true))))

    # Calculate stats
    y_true_llamp = data[f'llamp_{task}']
    y_pred_llamp = data[f'{task}']  
    mae_llamp = mean_absolute_error(y_true_llamp, y_pred_llamp)
    mse_llamp = mean_squared_error(y_true_llamp, y_pred_llamp)
    r_squared_llamp = r2_score(y_true_llamp, y_pred_llamp)
    # Additional metrics for LLAMP prediction
    mape_llamp = mean_absolute_percentage_error(y_true_llamp, y_pred_llamp)
    rmsle_llamp = root_mean_squared_log_error(y_true_llamp, y_pred_llamp)

    y_true_gpt = data[f'gpt_{task}']
    y_pred_gpt = data[f'{task}'] 
    mae_gpt = mean_absolute_error(y_true_gpt, y_pred_gpt)
    mse_gpt = mean_squared_error(y_true_gpt, y_pred_gpt)
    r_squared_gpt = r2_score(y_true_gpt, y_pred_gpt)
    # Additional metrics for GPT prediction
    mape_gpt = mean_absolute_percentage_error(y_true_gpt, y_pred_gpt)
    rmsle_gpt = root_mean_squared_log_error(y_true_gpt, y_pred_gpt)

    # output = {
    #     f"Llamp {task} prediction": {"MAE": mae_llamp, "MSE": mse_llamp, "R-squared": r_squared_llamp,
    #                                 "MAPE": mape_llamp, "RMSLE": rmsle_llamp},
    #     f"GPT3.5 {task} prediction": {"MAE": mae_gpt, "MSE": mse_gpt, "R-squared": r_squared_gpt,
    #                                 "MAPE": mape_gpt, "RMSLE": rmsle_gpt}
    # }

    output = {
        f"Llamp {task} prediction": {"MAE": mae_llamp, "MSE": mse_llamp, "R-squared": r_squared_llamp},
        f"GPT3.5 {task} prediction": {"MAE": mae_gpt, "MSE": mse_gpt, "R-squared": r_squared_gpt} }

    
    print(output)

    
def task8_space_group(data):
    task = "space_group"
    data = data.replace({'': 'N/A', 'N/A': 'N/A', 'N/A': 'N/A', np.nan: 'N/A'})
    actual =  data[f"{task}"]
    predicted1 = data[f"llamp_{task}"]
    predicted2 = data[f"gpt_{task}"]
    print(predicted1.unique(), predicted2.unique(), actual.unique())
    # breakpoint()

    known_labels = np.unique(actual)
    predicted1 = np.where(np.isin(predicted1, known_labels), predicted1, 'Other')
    predicted2 = np.where(np.isin(predicted2, known_labels), predicted2, 'Other')

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

# def task8_lattice_parameter(data):
#     fig, ax = plot_setup()  # Initialize plot with the custom setup
#     task = "lattice_parameters"
    
#     sns.scatterplot(data=data, x=f'{task}', y=f'llamp_{task}', color='red', label=f'LLAMP for {task}', ax=ax)
#     sns.scatterplot(data=data, x=f'{task}', y=f'gpt_{task}', color='green', label=f'GPT for {task}', ax=ax)
#     ax.axline([0, 0], [1, 1], color='blue', linestyle='--', linewidth=2)

#     ax.set_xlabel('Ground Truth')
#     ax.set_ylabel(f"{task}")
#     ax.legend()
#     plot_done(f"{task}")

#     # Calculate stats
#     def mean_absolute_percentage_error(y_true, y_pred):
#         return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-12))) * 100

#     def root_mean_squared_log_error(y_true, y_pred):
#         return np.sqrt(np.mean(np.square(np.log1p(y_pred) - np.log1p(y_true))))

#     # Calculate stats
#     y_true_llamp = data[f'llamp_{task}']
#     y_pred_llamp = data[f'{task}']  
#     mae_llamp = mean_absolute_error(y_true_llamp, y_pred_llamp)
#     mse_llamp = mean_squared_error(y_true_llamp, y_pred_llamp)
#     r_squared_llamp = r2_score(y_true_llamp, y_pred_llamp)
#     # Additional metrics for LLAMP prediction
#     mape_llamp = mean_absolute_percentage_error(y_true_llamp, y_pred_llamp)
#     rmsle_llamp = root_mean_squared_log_error(y_true_llamp, y_pred_llamp)

#     y_true_gpt = data[f'gpt_{task}']
#     y_pred_gpt = data[f'{task}'] 
#     mae_gpt = mean_absolute_error(y_true_gpt, y_pred_gpt)
#     mse_gpt = mean_squared_error(y_true_gpt, y_pred_gpt)
#     r_squared_gpt = r2_score(y_true_gpt, y_pred_gpt)
#     # Additional metrics for GPT prediction
#     mape_gpt = mean_absolute_percentage_error(y_true_gpt, y_pred_gpt)
#     rmsle_gpt = root_mean_squared_log_error(y_true_gpt, y_pred_gpt)

#     output = {
#         f"Llamp {task} prediction": {"MAE": mae_llamp, "MSE": mse_llamp, "R-squared": r_squared_llamp},
#         f"GPT3.5 {task} prediction": {"MAE": mae_gpt, "MSE": mse_gpt, "R-squared": r_squared_gpt} }

#     print(output)

def task8_lattice_parameter(data):
    task = "lattice_parameters"
    num_components = 6
    fig, axs = plt.subplots(num_components, 1, figsize=(10, num_components * 5))
    actual =  data[f"{task}"]
    predicted1 = data[f"llamp_{task}"]
    predicted2 = data[f"gpt_{task}"]
    def is_numeric_tuple(t):
        return all(isinstance(x, (int, float, np.number)) and not np.isnan(x) for x in eval(t))

    # Filter out non-numeric tuples
    index = actual.apply(is_numeric_tuple) & predicted1.apply(is_numeric_tuple) & predicted2.apply(is_numeric_tuple)
    actual = actual[index]
    predicted1 = predicted1[index]
    predicted2 = predicted2[index]

    def extract_unique_types(series):
        type_set = set()
        for item in series:
            if len(eval(item)) != 6:
                breakpoint()
            type_set.add(len(eval(item)))
        return type_set

    # Extract unique types from each series
    unique_types_actual = extract_unique_types(actual)
    unique_types_predicted1 = extract_unique_types(predicted1)
    unique_types_predicted2 = extract_unique_types(predicted2)
    print("Unique types in actual data:", unique_types_actual)
    print("Unique types in LLAMP predictions:", unique_types_predicted1)
    print("Unique types in GPT predictions:", unique_types_predicted2)


    def mean_absolute_percentage_error(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-12))) * 100

    def root_mean_squared_log_error(y_true, y_pred):
        return np.sqrt(np.mean(np.square(np.log1p(y_pred) - np.log1p(y_true))))

    output = {}
    item_dict = {0:"a", 1:"b", 2:"c", 3:"alpha", 4:"beta", 5:"gamma"}
    for i in range(num_components):
        breakpoint()
        ax = axs[i]
        sns.scatterplot(x=actual.apply(lambda x: eval(x)[i]), y=predicted1.apply(lambda x: eval(x)[i]), color='red', label=f'LLAMP for {task}', ax=ax)
        sns.scatterplot(x=actual.apply(lambda x: eval(x)[i]), y=predicted2.apply(lambda x: eval(x)[i]), color='green', label=f'GPT for {task}', ax=ax)
        ax.axline([0, 0], [1, 1], color='blue', linestyle='--', linewidth=2)
        ax.set_xlabel('Ground Truth')
        ax.set_ylabel(f"{task} {item_dict[i]}")
        ax.legend()

        y_true_llamp = actual.apply(lambda x: eval(x)[i])
        y_pred_llamp = predicted1.apply(lambda x: eval(x)[i])
        mae_llamp = mean_absolute_error(y_true_llamp, y_pred_llamp)
        mse_llamp = mean_squared_error(y_true_llamp, y_pred_llamp)
        r_squared_llamp = r2_score(y_true_llamp, y_pred_llamp)
        mape_llamp = mean_absolute_percentage_error(y_true_llamp, y_pred_llamp)
        rmsle_llamp = root_mean_squared_log_error(y_true_llamp, y_pred_llamp)

        y_true_gpt = actual.apply(lambda x: eval(x)[i])
        y_pred_gpt = predicted2.apply(lambda x: eval(x)[i])
        mae_gpt = mean_absolute_error(y_true_gpt, y_pred_gpt)
        mse_gpt = mean_squared_error(y_true_gpt, y_pred_gpt)
        r_squared_gpt = r2_score(y_true_gpt, y_pred_gpt)
        mape_gpt = mean_absolute_percentage_error(y_true_gpt, y_pred_gpt)
        rmsle_gpt = root_mean_squared_log_error(y_true_gpt, y_pred_gpt)

        output[f"{item_dict[i]}"] = {
            "LLAMP Prediction": {"MAE": mae_llamp, "MSE": mse_llamp, "R-squared": r_squared_llamp, "MAPE": mape_llamp, "RMSLE": rmsle_llamp},
            "GPT Prediction": {"MAE": mae_gpt, "MSE": mse_gpt, "R-squared": r_squared_gpt, "MAPE": mape_gpt, "RMSLE": rmsle_gpt}
        }

    plt.tight_layout()
    plot_done(f"{task}")
    print(output)


df = pd.read_csv("cache/8_eval_dataset_copy.csv")
df = df.iloc[:500]

############################ Benchmark 6 ############################
# task6_conf_mat(df)

# Numeral Task Preprocessing
# df = df.replace({'': 0, 'N/A': 0, None: 0, np.nan: 0})
# task6_magnetization_unit(df)

############################ Benchmark 7 ############################
# task = "density"
# task = "volume"

# Numeral Task Preprocessing
# df = df.replace({'': 0, 'N/A': 0, None: 0, np.nan: 0})
# filtered_df = df[(df[f'gpt_{task}'] <= 100) & (df[f'{task}'] <= 100) & (df[f'llamp_{task}'] <= 100)]
# task7_regression(filtered_df, task)

############################ Benchmark 8 ############################
# task = "density"
task = "volume"

# Numeral Task Preprocessing
# filler = "(0, 0, 0, 0, 0, 0)"
filler = "['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']"
df = df.replace({'[]': filler, '': filler, 'N/A': filler, None: filler, np.nan: filler})
# task8_space_group(df)
task8_lattice_parameter(df)
