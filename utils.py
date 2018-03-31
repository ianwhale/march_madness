#
# utils.py
#

import pandas as pd
from glicko2.glicko2 import Player, glicko_rounds


def append_glicko(df):
    """
    Appends the glicko2 ratings of the winning and losing team to each row.
    * Dataframe should probably only be the regular season.
    Inspired by: https://www.kaggle.com/lpkirwin/fivethirtyeight-elo-ratings
    :param df: pandas.DataFrame, some MM data with WTeamID and LTeamID columns.
    :return: pandas.DataFrame, same dataframe but with w_glicko and l_glicko appended.
    """
    team_ids = set(df.WTeamID).union(set(df.LTeamID))
    glicko = {team_id: Player() for team_id in team_ids}

    w_glicko, l_glicko = glicko_rounds(glicko, [], df)

    df['w_glicko'] = w_glicko
    df['l_glicko'] = l_glicko

    return df


def get_labels(df):
    """
    Get the standard labeling scheme from a particular dataframe.
    :param df: pandas.DataFrame, some MM data with WTeamID and LTeamID columns.
    :return: list, binary list, 1 if team with smaller ID value won, 0 otherwise.
    """
    return [int(row.WTeamID < row.LTeamID) for row in df.itertuples()]
