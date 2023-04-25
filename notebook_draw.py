import numpy as np
import pandas as pd
import pathlib

import matplotlib.pyplot as plt
import seaborn as sns

from pprint import pprint as print
from notebook_utils import *
from taxonomy_metrics import *
from comparative_measures import *

plt.rcParams['figure.figsize'] = [7, 5]
plt.rcParams['figure.dpi'] = 90
pd.options.display.float_format = '{:,.2f}'.format
sns.set_style("whitegrid", {'axes.grid' : False})


def left_plot():
    """ starts a new figure and creates a left sub plot """
    plt.figure(figsize=(15,5))
    plt.subplot(1, 2, 1)

def right_plot():
    """ must be used after the left_plot is called """
    plt.subplot(1, 2, 2)   
    
def draw_hist(series, label="", title=None, x_label="", y_label="Frequency", kde=False, color="green",bins=25):
    """
        draw a hystogram using seaborn library
    """
    sns.distplot(series,kde=kde, color=color, bins=bins, label=label)
    plt.legend(prop={'size': 12})
    plt.title(title if title is not None else "" + label + " histogram")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    

def describe(series, index):
    """
        takes a list of series and a list of indexes and provides descriptive statistics for them
    """
    return pd.DataFrame( data=[ stats.describe(s) for s in series], index=index )