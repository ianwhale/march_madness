#
# random_forest.py
#   - Classify data into wins/losses with random forest.
#
# 2017 Data Results
# Mean validation accuracy: 0.6739969135802469
# Testing accuracy: 0.7014925373134329
# Best estimators found: 55
#
# 2014-2017 Data Results
# Mean validation accuracy: 0.6721037998146432
# Testing accuracy: 0.6716417910447762
# Best estimators found: 70
#
# 4 Seasons Combined
#
#
#
# Old Glicko 2017 Results
#
#
#

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from utils import remove_init_rows, get_data_and_labels, drop_irrelevant_columns, get_tourney_reg_season


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv"
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
                                'n_estimators': [i for i in range(40, 101, 5)]
                           },
                           n_jobs=-1,
                           cv=5)
        clf.fit(X, y)

        with open(model_file, 'wb') as fptr:
            pickle.dump(clf, fptr)

    print("Mean validation accuracy: {}".format(clf.best_score_))
    print("Testing accuracy: {}".format(accuracy_score(y_test, clf.predict(X_test))))
    print("Best estimators found: {}".format(clf.best_params_['n_estimators']))

    importance_pairs = list(zip(drop_irrelevant_columns(df).columns.values, clf.best_estimator_.feature_importances_))

    zeros = importance_pairs[:len(importance_pairs) // 2]
    ones = importance_pairs[len(importance_pairs) // 2:]

    pairs_unique = []
    for (name, val_0), (_, val_1) in zip(zeros, ones):
        name = name.replace("opponents", "ops")
        pairs_unique.append((name[:-2], val_0 + val_1))

    pairs_unique = sorted(pairs_unique, key=lambda x: x[1], reverse=True)

    pairs_nonzero = []
    for pair in pairs_unique:
        if pair[1] > 0:
            pairs_nonzero.append(pair)

    features, importances = zip(*pairs_nonzero)

    indx = [i for i in range(len(features))]

    plt.tick_params(axis="x", labelsize=8)
    plt.bar(indx, importances)
    plt.xticks(indx, features, rotation="vertical")
    plt.ylabel("Random Forest Feature Importance")
    plt.tight_layout()
    plt.savefig("./plots/random_forest_feature_importance.png", dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
