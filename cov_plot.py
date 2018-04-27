#
# cov_plot.py
#   - Show the covariance heatmap of the data.
#

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import remove_init_rows, drop_irrelevant_columns


def main():
    """
    Main entry point.
    """

    from pprint import PrettyPrinter
    print = PrettyPrinter(indent=4).pprint

    filename = "data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    df = drop_irrelevant_columns(df)
    df = df.drop(['label'], axis=1)

    #
    # Add columns corresponding to the same feature.
    # This will not affect correlation of pairwise features, e.g. rpi-0 and rpi-1 are the same feature.
    #

    headers = df.columns.values

    zeros = headers[:len(headers) // 2]
    ones = headers[len(headers) // 2:]

    headers = []
    for name in zeros:
        headers.append(name.replace("opponents", "ops")[:-2])

    zeros = df[zeros]
    ones = df[ones]

    summed = pd.DataFrame(data=zeros.as_matrix() + ones.as_matrix(), columns=headers)

    cov = summed.corr()

    mask = np.zeros_like(cov, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(cov, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    plt.tight_layout()
    plt.savefig("./plots/cov_plot.png", dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
