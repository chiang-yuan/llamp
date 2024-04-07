
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