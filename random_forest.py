#
# random_forest.py
#   - Classify data into wins/losses with random forest.
#

import os
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from utils import remove_init_rows, get_data_and_labels, get_tournament


def main():
    """
    Main entry point.
    """
    filename = "data_matrices/2017season.csv"
    df = pd.read_csv(filename)
    df = remove_init_rows(df)
    data, labels = get_data_and_labels(df)

    X, X_test, y, y_test = get_tournament(data, labels)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25)

    model_file = os.path.join(".", "models", "random_forest.pkl")
    if os.path.isfile(model_file):
        with open(model_file, 'rb') as fptr:
            clf = pickle.load(fptr)

    else:
        clf = RandomForestClassifier(n_estimators=50)
        clf.fit(X_train, y_train)

        with open(model_file, 'wb') as fptr:
            pickle.dump(clf, fptr)

    print("Validation accuracy: {}".format(accuracy_score(y_val, clf.predict(X_val))))
    print("Testing accuracy: {}".format(accuracy_score(y_test, clf.predict(X_test))))


if __name__ == '__main__':
    main()
