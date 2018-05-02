#
# ensemble_serial.py
#
#******************************
# Results for model: random_forest
# data_matrices/DataMatrices/old_glicko_1_seasons/old_glicko_1_seasons_combined.csv
# Tournament prediction score: 96
# data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv
# Tournament prediction score: 65
# data_matrices/DataMatrices/2_seasons/2_seasons_combined.csv
# Tournament prediction score: 66
# data_matrices/DataMatrices/3_seasons/3_seasons_combined.csv
# Tournament prediction score: 67
# data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv
# Tournament prediction score: 58
# ******************************
# Results for model: adaboost
# data_matrices/DataMatrices/old_glicko_1_seasons/old_glicko_1_seasons_combined.csv
# Tournament prediction score: 90
# data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv
# Tournament prediction score: 120
# data_matrices/DataMatrices/2_seasons/2_seasons_combined.csv
# Tournament prediction score: 52
# data_matrices/DataMatrices/3_seasons/3_seasons_combined.csv
# Tournament prediction score: 128
# data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv
# Tournament prediction score: 78

import os
import pickle
from utils import drop_irrelevant_columns
from tournament import Bracket, get_row


class PredictionWrapper:
    """
    Wrapper class to adapt the tournament code to Sklearn models.
    """
    def __init__(self, model):
        self.model = model

    def __call__(self, team_1, team_2):
        """
        :param team_1: pandas.DataFrame, represents a team's stats.
        :param team_2: pandas.DataFrame, the other team's stats.
        :return: pandas.DataFrame, the winning team.
        """
        row = get_row(team_1, team_2)

        x = drop_irrelevant_columns(row).drop("label", axis=1).as_matrix()

        # If the model predicts the team with the lower ID to win, return team 1.
        if self.model.predict(x):
            return team_1 if team_1.id > team_2.id else team_2
        else:
            return team_2 if team_1.id > team_2.id else team_1


def main():
    """
    Main entry point.
    """
    models = ["random_forest", "adaboost"]
    filepaths = [
        "data_matrices/DataMatrices/old_glicko_1_seasons/old_glicko_1_seasons_combined.csv",
        "data_matrices/DataMatrices/1_seasons/1_seasons_combined.csv",
        "data_matrices/DataMatrices/2_seasons/2_seasons_combined.csv",
        "data_matrices/DataMatrices/3_seasons/3_seasons_combined.csv",
        "data_matrices/DataMatrices/4_seasons/4_seasons_combined.csv"
    ]

    for model_str in models:
        print("*" * 30)
        print("Results for model: {}".format(model_str))
        for filepath in filepaths:
            dirname = os.path.dirname(filepath) + "/"
            basename = os.path.basename(filepath)
            pkl_name = basename.split('.')[0] + "_" + model_str + ".pkl"

            with open(os.path.join("models", pkl_name), 'rb') as fptr:
                model = pickle.load(fptr)

            bracket = Bracket(dirname, basename, 2017)
            score = bracket.score_tournament(PredictionWrapper(model))

            print(filepath)
            print("Tournament prediction score: {}".format(score))


if __name__ == '__main__':
    main()
