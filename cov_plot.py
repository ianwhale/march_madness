#
# cov_plot.py
#   - Show the covariance heatmap of the data.
#

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import remove_init_rows


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/2017season.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)

    df = df.drop(['Unnamed: 0', 'year', 'id_0', 'id_1'], axis=1)
    df = df.drop(['label'], axis=1)

    print(df.head())

    cov = df.corr()

    print(cov.shape)

    exit()

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


if __name__ == '__main__':
    main()
