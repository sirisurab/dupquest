# common functions to make plots

from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
sns.set_context('paper')
sns.set_style('darkgrid')

# function to plot the roc curve given the false positive rate, true positive rate and the area under curve
def plot_roc(fpr, tpr, roc_auc):
    df_real = pd.DataFrame(fpr, columns=['false positive rate'])
    df_real['true positive rate'] = pd.Series(tpr)
    df_real['curve'] = 'model'
    fpr_ideal = np.insert(fpr, 1, 0.00001)
    df_ideal = pd.DataFrame(fpr_ideal, columns=['false positive rate'])
    df_ideal['true positive rate'] = 1.0
    df_ideal['true positive rate'][0] = 0.0
    df_ideal['curve'] = 'ideal'
    df_worst = pd.DataFrame(fpr, columns=['false positive rate'])
    df_worst['true positive rate'] = pd.Series(fpr)
    df_worst['curve'] = 'random guess'
    df = pd.concat([df_real, df_ideal, df_worst])
    pal = {'model': "#3498db", 'random guess':"#e74c3c", 'ideal':"#34495e"}
    ax = sns.relplot('false positive rate', 'true positive rate', hue='curve', data=df,
                linewidth=2.0, palette=pal, kind="line", legend='full', height=5, aspect=7/5)
    ax.set(xlim=(-.05, 1.0), ylim=(0.0, 1.05), title='Receiver operating characteristic\n(area under curve = %0.2f)' % roc_auc)
    return

# function to make a custom bar with option to use logscale along the x-axis
def bar_plot_maker(data, value_col, name_col, label, title, logscale=False, xticks=None, xticklabels=None):
    f, ax = plt.subplots(figsize=(7, 10))
    # Plot variances
    sns.set_color_codes("pastel")
    sns.barplot(x=value_col, y=name_col, data=data,
                label=label, color="b")

    # Add a legend and informative axis label
    ax.legend(ncol=1, loc="lower right", frameon=True)
    ax.set(ylabel="", title=title)
    if logscale:
        ax.set(xscale='log')
    if xticks:
        ax.set(xticks=xticks, xticklabels=xticklabels)
    if logscale:
        ax.get_xaxis().set_major_formatter(ScalarFormatter())
    sns.despine(left=True, bottom=True)
    return