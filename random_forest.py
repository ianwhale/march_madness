#
# random_forest.py
#   - Classify data into wins/losses with random forest.
#
# Mean validation accuracy: 0.6739969135802469
# Testing accuracy: 0.7014925373134329
# Best estimators found: 55
#

import os
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from utils import remove_init_rows, get_data_and_labels, drop_irrelevant_columns, get_tourney_reg_season


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/DataMatrices/2017dataMatrix.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    reg_season_df, tourney_df = get_tourney_reg_season(df)
    X, y = get_data_and_labels(drop_irrelevant_columns(reg_season_df))
    X_test, y_test = get_data_and_labels(drop_irrelevant_columns(tourney_df))

    model_file = os.path.join(".", "models", "random_forest.pkl")
    if os.path.isfile(model_file):
        with open(model_file, 'rb') as fptr:
            clf = pickle.load(fptr)

    else:
        rf = RandomForestClassifier(n_estimators=50)
        clf = GridSearchCV(rf,
                           {
                                'n_estimators': [i for i in range(40, 61, 5)]
                           },
                           n_jobs=-1,
                           cv=5)
        clf.fit(X, y)

        with open(model_file, 'wb') as fptr:
            pickle.dump(clf, fptr)

    print("Mean validation accuracy: {}".format(clf.best_score_))
    print("Testing accuracy: {}".format(accuracy_score(y_test, clf.predict(X_test))))
    print("Best estimators found: {}".format(clf.best_params_['n_estimators']))


if __name__ == '__main__':
    main()
