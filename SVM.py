 # filename = "data_matrices/2014-2017dataMatrix.csv"
    # max-min normalizer
    #{'C': 10, 'kernel': 'linear'}
    #Validation accuracy: 0.7021316033364227
    #Testing accuracy: 0.7761194029850746
    # original data
    #{'C': 10, 'kernel': 'linear'}
    #Validation accuracy: 0.6971269694161261
    #Testing accuracy: 0.746268656716418


import os
import pickle
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn import svm
from utils import remove_init_rows, get_data_and_labels, drop_irrelevant_columns, get_tourney_reg_season
from sklearn.model_selection import GridSearchCV

def tune_parameters(X, Y, tuned_parameters):
    # cv k fold
    clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=5)
    clf.fit(X, Y)
    
    return clf

def normalize_data(data, normalizer):
    if normalizer == 'minmax':
        min_max_scaler = preprocessing.MinMaxScaler()
        data = min_max_scaler.fit_transform(data)
    elif normalizer == 'normal':
        data = preprocessing.scale(data)
    
    return data            

def main(filename):
    """
    Main entry point.
    """
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    reg_season_df, tourney_df = get_tourney_reg_season(df)
    X, y = get_data_and_labels(drop_irrelevant_columns(reg_season_df))
    X_test, y_test = get_data_and_labels(drop_irrelevant_columns(tourney_df))
    
            
    normalizers = ['original', 'minmax', 'normal']
        
    for normalizer in normalizers:

        base_name = os.path.basename(filename).split(".")[0]
        model_file = os.path.join(".", "models", base_name + "_SVM_" + normalizer + ".pkl")
        if os.path.isfile(model_file):
            with open(model_file, 'rb') as fptr:
                clf = pickle.load(fptr)
        else:       
        
        # Set the parameters by cross-validatio
        #    # Set the parameters by cross-validation
        #Best parameters set found on development set:
        
            tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                                 'C': [1, 10, 100, 1000]},
                                {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    
            X = normalize_data(X, normalizer)
            clf = tune_parameters(X, y, tuned_parameters)
            with open(model_file, 'wb') as fptr:
                pickle.dump(clf, fptr)
                    
        X_test = normalize_data(X_test, normalizer)
        print("Best parameters set found on development set: {}".format(clf.best_params_))
        print("Normalizer: {}".format(normalizer))
        print("Validation accuracy: {}".format(clf.best_score_))
        print("Testing accuracy: {}".format(accuracy_score(y_test, clf.predict(X_test))))


if __name__ == '__main__':
    
    filepaths = [
        "data_matrices/DataMatrices/old_glicko_1_seasons/old_glicko_1_seasons_combined.csv",
        "data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv",
        "data_matrices/DataMatrices/2_seasons/2_seasons_combined.csv",
        "data_matrices/DataMatrices/3_seasons/3_seasons_combined.csv",
        "data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv"
    ]

    for f in filepaths:
        print(f)
        main(f)
