#
# adaboost.py
#   - Classify data into wins/losses with AdaBoost algorithm.
#
# Mean validation accuracy: 0.673804012345679
# Testing accuracy: 0.6567164179104478
# Best estimators found: 75
#

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from utils import remove_init_rows, get_data_and_labels, get_tourney_reg_season, drop_irrelevant_columns


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

    model_file = os.path.join(".", "models", "adaboost.pkl")
    if os.path.isfile(model_file):
        with open(model_file, 'rb') as fptr:
            clf = pickle.load(fptr)

    else:
        ada = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1))
        clf = GridSearchCV(ada,
                           {
                                'n_estimators': [50, 75, 100, 125, 150, 175, 200, 225, 250]
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
    plt.ylabel("Adaboost Feature Importance")
    plt.tight_layout()
    plt.savefig("./plots/adaboost_feature_importance.png", dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
