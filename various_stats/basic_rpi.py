import numpy as np
import pandas as pd


df = pd.read_csv('data/RegularSeasonDetailedResults.csv')
year = 2017

df_sp = df.loc[df['Season'] == year]

team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

wps = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    win_rate = 1.*len(w)/(len(w)+len(l))
    wps[id] = win_rate


owps = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    owp = 0
    for row in l.itertuples():
        owp += wps[int(row.WTeamID)]
    for row in w.itertuples():
        owp += wps[int(row.LTeamID)]
    owps[id] = owp/(1.*len(l) + len(w))

oowps = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    oowp = 0
    games = 0
    for row in l.itertuples():
        oowp += owps[row.WTeamID]
        games += 1.
    for row in w.itertuples():
        oowp += owps[row.LTeamID]
        games += 1.
    oowps[id] = oowp/games

rpis = {}
for id in team_ids:
    rpis[id] = .25 *wps[id] + .5*owps[id] + .25*oowps[id]

def predict(rpis, preds, df):
    for row in df.itertuples():
        if rpis[row.WTeamID] > rpis[row.LTeamID]:
            preds.append(1.)
        else:
            preds.append(0.)

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