#
# cov_plot.py
#   - Show the covariance heatmap of the data.
#

import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from utils import remove_init_rows, get_data_and_labels


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/2017season.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)

    df = df.drop(['Unnamed: 0', 'year', 'id_0', 'id_1'], axis=1)
    df = df.drop(['label'], axis=1)

    cov = df.corr()

    mask = np.zeros_like(cov, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(cov, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    plt.savefig("./plots/cov_plot.png", dpi=300)
    plt.show()

    # X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.25)


if __name__ == '__main__':
    main()
