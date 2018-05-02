import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from utils import remove_init_rows, get_data_and_labels, drop_irrelevant_columns
import numpy as np
import pylab as lab
from sklearn import preprocessing

def display_component(pca, compNum, header):
    comp = pca.components_[compNum]
    indeces = np.argsort(comp).tolist()
    indeces.reverse()
    terms = [header[index] for index in indeces[0:10]]  
    weights = [comp[index] for index in indeces[0:10]]
    terms.reverse()
    weights.reverse()
    positions = lab.arange(10) + .5    # the bar centers on the y axis
    
    lab.figure("Weights")
    lab.barh(positions, weights, align='center')
    lab.yticks(positions, terms)
    lab.xlabel('Weight')
    lab.title('Strongest features for component %d' % (compNum))
    lab.grid(True)
    lab.show() 

def apply_pca(data, num_components, normalized = False):
    if normalized:
        # Apply Scaling to data (min max or std norm)
        # z-transform: data = preprocessing.scale(data)
        # min max: min_max_scaler = preprocessing.MinMaxScaler()
        #          data = min_max_scaler.fit_transform(data)
        min_max_scaler = preprocessing.MinMaxScaler()
        data = min_max_scaler.fit_transform(data)
    # PCA
    pca = PCA(n_components=num_components)
    projected = pca.fit(data).transform(data)    
    
    return (pca, projected)  

def plot_eigenvalues(pca):
    plt.figure("Eigenvalues")    
    plt.plot(pca.explained_variance_ratio_) 
    plt.ylabel("explained variance")
    plt.title("Eigenvalues")
    plt.show()
    
def main():
    """
    Main entry point.
    """
    filename = "data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    df = drop_irrelevant_columns(df)
    header = df.columns.tolist()
    header = [x for x in header if x not in ['Unnamed: 0', 'tourny', 'year', 'id_0', 'id_1', 'label']]
    data, labels = get_data_and_labels(df)
    
    pca, projected = apply_pca(data, num_components = 50, normalized = True)
    
    display_component(pca, 0, header)
    
    plot_eigenvalues(pca)
    
    print()
    plt.figure("Projection")
    for i, color in zip([0, 1], ["navy", "darkorange"]):
        plt.scatter(projected[labels == i, 0], projected[labels == i, 1], alpha=0.5, color=color)
    plt.xlabel("PC1 ({:.4}%) ".format(pca.explained_variance_ratio_[0] * 100))
    plt.ylabel("PC2 ({:.4}%)".format(pca.explained_variance_ratio_[1] * 100))
    plt.savefig('plots/pca.png', dpi=300)
    plt.show()


#if __name__ == '__main__':
 #   main()
