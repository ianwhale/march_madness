import numpy as np
import pandas as pd


df = pd.read_csv('data/RegularSeasonDetailedResults.csv')
year = 2017

df_sp = df.loc[df['Season'] == year]

team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

win_percentages = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    win_rate = 1.*len(w)/(len(w)+len(l))
    win_percentages[id] = win_rate

def predict(rpis, preds, df):
    for row in df.itertuples():
        if rpis[row.WTeamID] > rpis[row.LTeamID]:
            preds.append(1.)
        else:
            preds.append(0.)

rpis = win_percentages
preds = []
predict(rpis, preds, df_sp)
print "Regular season results:",sum(preds) / len(preds)

preds = []
df = pd.read_csv('./data/ConferenceTourneyGames.csv')
df_sp = df.loc[df['Season'] == year]
predict(rpis, preds, df_sp)
print "Conference tournement results:",sum(preds) / len(preds)

preds = []
df = pd.read_csv('./data/NCAATourneyCompactResults.csv')
df_sp = df.loc[df['Season'] == year]
predict(rpis, preds, df_sp)
print "Tournement Results:",sum(preds) / len(preds)