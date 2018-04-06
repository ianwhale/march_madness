import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./data/RegularSeasonCompactResults.csv')
year = 2017

df_sp = df.loc[df['Season'] == year]

team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

from glicko2 import Player

def glicko_rounds(glicko, df):
    for row in df.itertuples():
        w = row.WTeamID
        l = row.LTeamID

        w_rating, l_rating = glicko[w].getRating(), glicko[l].getRating()
        w_rd, l_rd = glicko[w].getRd(), glicko[l].getRd()

        glicko[w].update_player([l_rating], [l_rd], [1])
        glicko[l].update_player([w_rating], [w_rd], [0])

def predict(glickos, preds, df):
    for row in df.itertuples():
        if glickos[row.WTeamID].rating > glickos[row.LTeamID].rating:
            preds.append(1.)
        else:
            preds.append(0.)

#Establish glickos for regular season
glicko = dict(zip(list(team_ids), [Player() for _ in range(len(team_ids))]))
glicko_rounds(glicko, df_sp)


preds = []
predict(glicko, preds, df_sp)
print ("Regular season results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/ConferenceTourneyGames.csv')
df_sp = df.loc[df['Season'] == year]
predict(glicko, preds, df_sp)
print ("Conference tournement results:",sum(preds) / len(preds))

preds = []
df = pd.read_csv('./data/NCAATourneyCompactResults.csv')
df_sp = df.loc[df['Season'] == year]
predict(glicko, preds, df_sp)
print ("Tournement Results:",sum(preds) / len(preds))