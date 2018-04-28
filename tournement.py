import numpy as np
import pandas as pd
import pickle
import sys
sys.path.insert(0, 'data_matrices/')
from data_matrix import make_row


def predict_tournement(prediction_function, path = "./data_matrices/DataMatrices/1_seasons/", filename = '1_seasons_combined.csv', year = 2017):

    class Bracket:
        bracket = [[[[[["W01","W16"], ["W08", "W09"]], [["W05", "W12"], ["W04", "W13"]]], [[["W06","W11"], ["W03","W14"]], [["W07", "W10"], ["W02", "W15"]]]], [[[["X01","X16"], ["X08", "X09"]], [["X05", "X12"], ["X04", "X13"]]], [[["X06","X11"], ["X03","X14"]], [["X07", "X10"], ["X02", "X15"]]]]], [[[[["Y01","Y16"], ["Y08", "Y09"]], [["Y05", "Y12"], ["Y04", "Y13"]]], [[["Y06","Y11"], ["Y03","Y14"]], [["Y07", "Y10"], ["Y02", "Y15"]]]], [[[["Z01","Z16"], ["Z08", "Z09"]], [["Z05", "Z12"], ["Z04", "Z13"]]], [[["Z06","Z11"], ["Z03","Z14"]], [["Z07", "Z10"], ["Z02", "Z15"]]]]]]

        def __init__(self, path, filename, year):
            file = path+filename
            team_names = pd.read_csv('./data_matrices/data/Teams.csv')
            team_seeds = pd.read_csv('./data_matrices/data/NCAATourneySeeds.csv')
            df = pd.read_csv(file)
            tournament = df[np.logical_and(df['tourny'] == 1, df['year'] == year)]
            num_games = len(tournament)
            #Delete play in games from the seeds dataframe
            play_in_games = tournament.iloc[0:num_games-63]
            for game in play_in_games.itertuples():
                if game.label == 0:
                    id_to_delete = team_seeds[np.logical_and(team_seeds['TeamID'] == game.id_1, team_seeds['Season'] == year)].TeamID.values[0]
                    team_seeds = team_seeds[team_seeds.TeamID != id_to_delete]
                else:
                    id_to_delete = team_seeds[np.logical_and(team_seeds['TeamID'] == game.id_0, team_seeds['Season'] == year)].TeamID.values[0]
                    team_seeds = team_seeds[team_seeds.TeamID != id_to_delete]
            tournament = tournament.iloc[num_games-63:num_games]
            print("Here")
            self.replace_seeds(dict(zip(list(team_seeds[team_seeds['Season'] == year]['Seed']), list([Team(i,file,year,team_names,team_seeds,path) for i in list(team_seeds[team_seeds['Season'] == year]['TeamID'])]))))

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
                if not isinstance(li, (list,)):
                    return li
                if not isinstance(li[0], (list,)):
                    return [li]
                else:
                    ret = []
                    for l in li:
                        ret += recurse_lists(l)
                    return ret
            return recurse_lists(self.bracket)

        def play_round(self, prediction_function):
            def play_round_help(li, prediction_function):
                if not isinstance(li[0], (list,)):
                    return prediction_function(li[0],li[1])
                else:
                    ret = []
                    for l in li:
                        ret.append(play_round_help(l,prediction_function))
                    return ret
            self.bracket = play_round_help(self.bracket, prediction_function)

        def play_tournement(self,prediction_function):
            print("\nRound of 64")
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nRound of 32")
            self.play_round(prediction_function)
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nSweet 16")
            self.play_round(prediction_function)
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nElite Eight")
            self.play_round(prediction_function)
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nFinal Four")
            self.play_round(prediction_function)
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nNational Champianship")
            self.play_round(prediction_function)
            games = self.get_games()
            for game in games:
                print('{} vs {}'.format(game[0].name,game[1].name))

            print("\nWinner")
            self.play_round(prediction_function)
            game = self.get_games()
            print('{} wins!'.format(game.name))

    class Team:
        def __init__(self, id, file, year, teams, seeds, path):
            self.id = id
            self.name = teams[teams['TeamID'] == id]['TeamName'].values[0]
            self.seed = seeds[np.logical_and(seeds['TeamID'] == id, seeds['Season'] == year)].values[0][1]
            self.year = year
            self.path = path




    b = Bracket(path,filename,year)
    b.play_tournement(prediction_function)
    #t = Team(1112,path+filename,year,pd.read_csv('./data_matrices/data/Teams.csv'),pd.read_csv('./data_matrices/data/NCAATourneySeeds.csv'),path)


def get_row(t1, t2):
    with open(t1.path + '{}_team_stats.p'.format(t1.year), 'rb') as file:
        team_stats = pickle.load(file)
    with open(t1.path + '{}_team_results.p'.format(t1.year), 'rb') as file:
        team_results = pickle.load(file)
    with open(t1.path + '{}_glicko.p'.format(t1.year), 'rb') as file:
        glicko = pickle.load(file)
    if t1.id < t2.id:
        return make_row(team_stats, team_results, glicko, t1.id, t2.id, t1.year)
    else:
        return make_row(team_stats, team_results, glicko, t2.id, t1.id, t1.year)


def lower_id_wins(t1,t2):
    if t1.id > t2.id:
        return t2
    return t1

def higher_glicko_wins(t1,t2):
    row = get_row(t1,t2)
    if row.iloc[0].glicko_0 > row.iloc[0].glicko_1:
        return t1 if t1.id > t2.id else t2
    else:
        return t2 if t1.id > t2.id else t1

predict_tournement(higher_glicko_wins)