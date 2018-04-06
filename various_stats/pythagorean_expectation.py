import numpy as np
import pandas as pd


df = pd.read_csv('data/RegularSeasonDetailedResults.csv')
year = 2017

df_sp = df.loc[df['Season'] == year]

team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

pythagorean_expectation = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    points_for = sum(l.ix[:,'LScore']) + sum(w.ix[:,'WScore'])
    points_against = sum(l.ix[:,'WScore']) + sum(w.ix[:,'LScore'])
    pyth_exp = 1./(1 + (1.*points_against/points_for)**8)
    pythagorean_expectation[id] = pyth_exp


def predict(pythagorean_expectation, preds, df):
    for row in df.itertuples():
        if pythagorean_expectation[row.WTeamID] > pythagorean_expectation[row.LTeamID]:
            preds.append(1.)
        else:
            preds.append(0.)

preds = []
predict(pythagorean_expectation, preds, df_sp)
print ("Regular season results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/ConferenceTourneyGames.csv')
df_sp = df.loc[df['Season'] == year]
predict(pythagorean_expectation, preds, df_sp)
print("Conference tournement results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/NCAATourneyCompactResults.csv')
df_sp = df.loc[df['Season'] == year]
predict(pythagorean_expectation, preds, df_sp)
print ("Tournement Results:",sum(preds) / len(preds))