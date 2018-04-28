import numpy as np
import pandas as pd

file = "./data_matrices/DataMatrices/1_seasons/2017dataMatrix.csv"
year = 2017

class Bracket:
    bracket = [[[[[["W01","W16"], ["W08", "W09"]], [["W05", "W12"], ["W04", "W13"]]], [[["W06","W11"], ["W03","W14"]], [["W07", "W10"], ["W02", "W15"]]]], [[[["X01","X16"], ["X08", "X09"]], [["X05", "X12"], ["X04", "X13"]]], [[["X06","X11"], ["X03","X14"]], [["X07", "X10"], ["X02", "X15"]]]]], [[[[["Y01","Y16"], ["Y08", "Y09"]], [["Y05", "Y12"], ["Y04", "Y13"]]], [[["Y06","Y11"], ["Y03","Y14"]], [["Y07", "Y10"], ["Y02", "Y15"]]]], [[[["Z01","Z16"], ["Z08", "Z09"]], [["Z05", "Z12"], ["Z04", "Z13"]]], [[["Z06","Z11"], ["Z03","Z14"]], [["Z07", "Z10"], ["Z02", "Z15"]]]]]]
    level = 6

    def replace_seeds(self, teams):
        def recurse_seeds_help(li, teams):
            if isinstance(li[0], str):
                li[0] = teams[li[0]]
                li[1] = teams[li[1]]
                return li
            else:
                ret = []
                for l in li:
                    ret.append(recurse_seeds_help(l,teams))
                return ret
        return recurse_seeds_help(self.bracket, teams)

    def get_games(self):
        def recurse_lists(li):
            if not isinstance(li[0], (list,)):
                return [li]
            else:
                ret = []
                for l in li:
                    ret += recurse_lists(l)
                return ret
        return recurse_lists(self.bracket)




TEAMS = pd.read_csv('./data_matrices/data/Teams.csv')
SEEDS = pd.read_csv('./data_matrices/data/NCAATourneySeeds.csv')
SLOTS = pd.read_csv('./data_matrices/data/NCAATourneySlots.csv')

class Team:
    def __init__(self, id):
        self.id = id
        global TEAMS
        self.name = TEAMS[TEAMS['TeamID'] == id]['TeamName'].values[0]
        global SEEDS
        self.seed = SEEDS[np.logical_and(SEEDS['TeamID'] == id, SEEDS['Season'] == year)].values[0][1]
        #global SLOTS
        #print(SLOTS[np.logical_or(np.logical_and(SLOTS['StrongSeed'] == id, SLOTS['Season'] == year), np.logical_and(SLOTS['WeakSeed'] == id, SLOTS['Season'] == year))].values)




df = pd.read_csv(file)
tournament = df[df['tourny'] == 1]
num_games = len(tournament)
play_in_games = tournament.iloc[0:num_games-63]
for game in play_in_games.itertuples():
    if game.label == 0:
        id_to_delete = SEEDS[np.logical_and(SEEDS['TeamID'] == game.id_1, SEEDS['Season'] == year)].TeamID.values[0]
        SEEDS = SEEDS[SEEDS.TeamID != id_to_delete]
    else:
        id_to_delete = SEEDS[np.logical_and(SEEDS['TeamID'] == game.id_0, SEEDS['Season'] == year)].TeamID.values[0]
        SEEDS = SEEDS[SEEDS.TeamID != id_to_delete]
tournament = tournament.iloc[num_games-63:num_games]




teams_by_seed = dict(zip(list(SEEDS[SEEDS['Season'] == year]['Seed']), list([Team(i) for i in list(SEEDS[SEEDS['Season'] == year]['TeamID'])])))

b = Bracket()
b.replace_seeds(teams_by_seed)
games = b.get_games()
#print(games)
for game in games:
    print('{} vs {}'.format(game[0].name,game[1].name))

