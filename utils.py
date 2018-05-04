#
# utils.py
#

import pandas as pd
import numpy as np


# def append_glicko(df):
#     """
#     Appends the glicko2 ratings of the winning and losing team to each row.
#     * Dataframe should probably only be the regular season.
#     :param df: pandas.DataFrame, some MM data with WTeamID and LTeamID columns.
#     :return: (pandas.DataFrame, dict) same dataframe but with w_glicko and l_glicko appended and glicko score dict.
#     """
#     team_ids = set(df.WTeamID).union(set(df.LTeamID))
#     glicko = {team_id: Player() for team_id in team_ids}
#
#     w_glicko, l_glicko = glicko_rounds(glicko, [], df)
#
#     df['w_glicko'] = w_glicko
#     df['l_glicko'] = l_glicko
#
#     return df, glicko


def get_labels(df):
    """
    Get the standard labeling scheme from a particular dataframe.
    :param df: pandas.DataFrame, some MM data with WTeamID and LTeamID columns.
    :return: list, binary list, 1 if team with smaller ID value won, 0 otherwise.
    """
    return [int(row.WTeamID < row.LTeamID) for row in df.itertuples()]


def remove_init_rows(df):
    """
    Rows corresponding to initialization values may be damaging to prediction accuracy as they are useless for learning.
    So we can just remove them.
    :param df: pd.DataFrame, data frame for prediction tasks.
    """
    df = df[df.points_0 != 0]
    return df[df.points_1 != 0]


def drop_irrelevant_columns(df):
    """
    Drop columns that do not have predictive quality.
    :param df: pd.DataFrame.
    :return: pd.DataFrame.
    """
    irrel = []
    for val in df.columns.values:
        if "unnamed" in val.lower():
            irrel.append(val)

    irrel += ['tourny', 'year', 'id_0', 'id_1']

    return df.drop(irrel, axis=1)


def get_data_and_labels(df):
    """
    Get the labels and data matrices.
    :param df: pd.DataFrame, data for prediction tasks.
    :return: np.ndarray
    """
    mat = df.as_matrix()
    return mat[:, :-1], mat[:, -1]


def get_tourney_reg_season(df):
    """
    Separate out the tournament and regular season data.
    :param df: pandas.DataFrame
    :return: (pandas.DataFrame, pandas.DataFrame)
    """
    return df[df.tourny == 0], df[df.tourny == 1]
