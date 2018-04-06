import numpy as np
import pandas as pd


df = pd.read_csv('data/RegularSeasonDetailedResults.csv')
year = 2017

df_sp = df.loc[df['Season'] == year]

team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

offensive_efficiencies = {}
for id in team_ids:
    l = df_sp.loc[df_sp['LTeamID'] == id]
    w = df_sp.loc[df_sp['WTeamID'] == id]
    FGA =  sum(l.ix[:,'LFGA']) + sum(w.ix[:,'WFGA'])
    OR =  sum(l.ix[:,'LOR']) + sum(w.ix[:,'WOR'])
    TO =  sum(l.ix[:,'LTO']) + sum(w.ix[:,'WTO'])
    FTA =  sum(l.ix[:,'LFTA']) + sum(w.ix[:,'WFTA'])
    points = sum(l.ix[:,'LScore']) + sum(w.ix[:,'WScore'])
    possesions = FGA-OR+TO+(.4*FTA)
    off_eff = points/possesions*100
    offensive_efficiencies[id] = off_eff


def predict(offensive_efficiencies, preds, df):
    for row in df.itertuples():
        if offensive_efficiencies[row.WTeamID] > offensive_efficiencies[row.LTeamID]:
            preds.append(1.)
        else:
            preds.append(0.)

preds = []
predict(offensive_efficiencies, preds, df_sp)
print ("Regular season results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/ConferenceTourneyGames.csv')
df_sp = df.loc[df['Season'] == year]
predict(offensive_efficiencies, preds, df_sp)
print("Conference tournement results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/NCAATourneyCompactResults.csv')
df_sp = df.loc[df['Season'] == year]
predict(offensive_efficiencies, preds, df_sp)
print ("Tournement Results:",sum(preds) / len(preds))