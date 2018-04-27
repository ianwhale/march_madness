#
# random_forest.py
#   - Classify data into wins/losses with random forest.
#
# data_matrices/DataMatrices/old_glicko_1_seasons/old_glicko_1_seasons_combined.csv
# Mean validation accuracy: 0.7022396995591357
# Testing accuracy: 0.7043832823649337
# Best estimators found: 170

# data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv
# Mean validation accuracy: 0.6939939040984052
# Testing accuracy: 0.7023445463812437
# Best estimators found: 160

# data_matrices/DataMatrices/2_seasons/2_seasons_combined.csv
# Mean validation accuracy: 0.6928921670764401
# Testing accuracy: 0.7099236641221374
# Best estimators found: 180

# data_matrices/DataMatrices/3_seasons/3_seasons_combined.csv
# Mean validation accuracy: 0.6840403441115396
# Testing accuracy: 0.7080890973036342
# Best estimators found: 160

# data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv
# Mean validation accuracy: 0.680605577689243
# Testing accuracy: 0.6932826362484157
# Best estimators found: 180

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from utils import remove_init_rows, get_data_and_labels, drop_irrelevant_columns, get_tourney_reg_season


def main(filename):
    """
    Main entry point.
    :param filename: string, the full filepath.
    """
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    reg_season_df, tourney_df = get_tourney_reg_season(df)
    X, y = get_data_and_labels(drop_irrelevant_columns(reg_season_df))
    X_test, y_test = get_data_and_labels(drop_irrelevant_columns(tourney_df))

    base_name = os.path.basename(filename).split(".")[0]
    model_file = os.path.join(".", "models", base_name + "_random_forest.pkl")
    if os.path.isfile(model_file):
        with open(model_file, 'rb') as fptr:
            clf = pickle.load(fptr)

    else:
        rf = RandomForestClassifier(n_estimators=50)
        clf = GridSearchCV(rf,
                           {
                                'n_estimators': [i for i in range(90, 201, 10)]
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
    plt.savefig("./plots/" + base_name + "_random_forest_feature_importance.png", dpi=300)
    plt.close()


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
