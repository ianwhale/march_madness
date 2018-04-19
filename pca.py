import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from utils import remove_init_rows, get_data_and_labels


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/DataMatrices/2017dataMatrix.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    data, labels = get_data_and_labels(df)

    pca = PCA(n_components=2)
    projected = pca.fit(data).transform(data)

    print()

    for i, color in zip([0, 1], ["navy", "darkorange"]):
        plt.scatter(projected[labels == i, 0], projected[labels == i, 1], alpha=0.8, color=color)

    plt.xlabel("PC1 ({:.4}%) ".format(pca.explained_variance_ratio_[0] * 100))
    plt.ylabel("PC2 ({:.4}%)".format(pca.explained_variance_ratio_[1] * 100))
    plt.savefig('plots/pca.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
