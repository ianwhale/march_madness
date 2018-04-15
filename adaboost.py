#
# adaboost.py
#   - Classify data into wins/losses with AdaBoost algorithm.
#

import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from utils import remove_init_rows, get_data_and_labels, get_tournament, drop_irrelevant_columns


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/2017season.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    df = drop_irrelevant_columns(df)
    data, labels = get_data_and_labels(df)

    X, X_test, y, y_test = get_tournament(data, labels)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25)

    model_file = os.path.join(".", "models", "adaboost.pkl")
    if os.path.isfile(model_file):
        with open(model_file, 'rb') as fptr:
            clf = pickle.load(fptr)

    else:
        clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=250)
        clf.fit(X_train, y_train)

        with open(model_file, 'wb') as fptr:
            pickle.dump(clf, fptr)

    print("Validation accuracy: {}".format(accuracy_score(y_val, clf.predict(X_val))))
    print("Testing accuracy: {}".format(accuracy_score(y_test, clf.predict(X_test))))

    importance_pairs = list(zip(df.columns.values, clf.feature_importances_))

    zeros = importance_pairs[:len(importance_pairs) // 2]
    ones = importance_pairs[len(importance_pairs) // 2:]

    pairs_unique = []
    for (name, val_0), (_, val_1) in zip(zeros, ones):
        name = name.replace("opponents", "ops")
        pairs_unique.append((name[:-2], val_0 + val_1))

    pairs_unique = sorted(pairs_unique, key=lambda x: x[1], reverse=True)
    features, importances = zip(*pairs_unique)

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
