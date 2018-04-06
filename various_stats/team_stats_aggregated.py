import numpy as np
import pandas as pd

df = pd.read_csv('data/RegularSeasonDetailedResults.csv')
year = 2017

def getDataMatrix(df, year):
    """
    df: dataframe to calculate statistics on (Regular season, postseason tournements, both)
    year: year to analyze
    """
    df_sp = df.loc[df['Season'] == year]

    team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

    data_matrix = pd.DataFrame(data = {'team_id': list(team_ids)})

    #Calculate averages for detailed results statistics
    for id in team_ids:
        l = df_sp.loc[df_sp['LTeamID'] == id]
        w = df_sp.loc[df_sp['WTeamID'] == id]
        num_games = len(l) + len(w)*1.0
        data_matrix.loc[data_matrix['team_id'] == id,'num_games'] = num_games

        #This teams stats, averaged over number of games
        FGM =  (sum(l.ix[:,'LFGM']) + sum(w.ix[:,'WFGM']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FGM'] = FGM
        FGA =  (sum(l.ix[:,'LFGA']) + sum(w.ix[:,'WFGA']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FGA'] = FGA
        FGM3 = (sum(l.ix[:,'LFGM3']) + sum(w.ix[:,'WFGM3']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FGM3'] = FGM3
        FGA3 = (sum(l.ix[:,'LFGA3']) + sum(w.ix[:,'WFGA3']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FGA3'] = FGA3
        FTM =  (sum(l.ix[:,'LFTM']) + sum(w.ix[:,'WFTM']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FTM'] = FTM
        FTA =  (sum(l.ix[:,'LFTA']) + sum(w.ix[:,'WFTA']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'FTA'] = FTA
        OR =  (sum(l.ix[:,'LOR']) + sum(w.ix[:,'WOR']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'OR'] = OR
        DR =  (sum(l.ix[:,'LDR']) + sum(w.ix[:,'WDR']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'DR'] = DR
        Ast = (sum(l.ix[:,'LAst']) + sum(w.ix[:,'WAst']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'Ast'] = Ast
        TO =  (sum(l.ix[:,'LTO']) + sum(w.ix[:,'WTO']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'TO'] = TO
        STL = (sum(l.ix[:,'LStl']) + sum(w.ix[:,'WStl']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'STL'] = STL
        PF = (sum(l.ix[:,'LPF']) + sum(w.ix[:,'WPF']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'PF'] = PF
        Blk = (sum(l.ix[:,'LBlk']) + sum(w.ix[:,'WBlk']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'Blk'] = Blk
        score = sum(l.ix[:,'LScore']) + sum(w.ix[:,'WScore'])/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'Score'] = score

        #Opposing teams stats, averaged over number of games
        O_FGM =  (sum(l.ix[:,'LFGM']) + sum(w.ix[:,'WFGM']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FGM'] = O_FGM
        O_FGA =  (sum(l.ix[:,'LFGA']) + sum(w.ix[:,'WFGA']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FGA'] = O_FGA
        O_FGM3 = (sum(l.ix[:,'LFGM3']) + sum(w.ix[:,'WFGM3']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FGM3'] = O_FGM3
        O_FGA3 = (sum(l.ix[:,'LFGA3']) + sum(w.ix[:,'WFGA3']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FGA3'] = O_FGA3
        O_FTM =  (sum(l.ix[:,'LFTM']) + sum(w.ix[:,'WFTM']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FTM'] = O_FTM
        O_FTA =  (sum(l.ix[:,'LFTA']) + sum(w.ix[:,'WFTA']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_FTA'] = O_FTA
        O_OR =  (sum(l.ix[:,'LOR']) + sum(w.ix[:,'WOR']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_OR'] = O_OR
        O_DR =  (sum(l.ix[:,'LDR']) + sum(w.ix[:,'WDR']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_DR'] = O_DR
        O_AST = (sum(l.ix[:,'LAst']) + sum(w.ix[:,'WAst']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_AST'] = O_AST
        O_TO =  (sum(l.ix[:,'LTO']) + sum(w.ix[:,'WTO']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_TO'] = O_TO
        O_STL = (sum(l.ix[:,'LStl']) + sum(w.ix[:,'WStl']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_STL'] = O_STL
        O_PF = (sum(l.ix[:,'LPF']) + sum(w.ix[:,'WPF']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_PF'] = O_PF
        O_Blk = (sum(l.ix[:,'LBlk']) + sum(w.ix[:,'WBlk']))/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_Blk'] = O_Blk
        O_score = sum(l.ix[:,'LScore']) + sum(w.ix[:,'WScore'])/num_games
        data_matrix.loc[data_matrix['team_id'] == id,'O_Score'] = O_score

        possesions = (FGA-OR+TO+(.4*FTA))
        data_matrix.loc[data_matrix['team_id'] == id,'possesions'] = possesions

    defensive_efficiencies = {}
    for id in team_ids:
        l = df_sp.loc[df_sp['LTeamID'] == id]
        w = df_sp.loc[df_sp['WTeamID'] == id]
        FGA =  sum(l.ix[:,'LFGA']) + sum(w.ix[:,'WFGA'])
        OR =  sum(l.ix[:,'LOR']) + sum(w.ix[:,'WOR'])
        TO =  sum(l.ix[:,'LTO']) + sum(w.ix[:,'WTO'])
        FTA =  sum(l.ix[:,'LFTA']) + sum(w.ix[:,'WFTA'])
        points_against = sum(l.ix[:,'WScore']) + sum(w.ix[:,'LScore'])
        possesions = FGA-OR+TO+(.4*FTA)
        def_eff = points_against/possesions*100
        #print(type(id))
        defensive_efficiencies[int(id)] = def_eff
        data_matrix.loc[data_matrix['team_id'] == id,'def_eff'] = def_eff

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
        data_matrix.loc[data_matrix['team_id'] == id,'off_eff'] = off_eff


    pythagorean_expectation = {}
    for id in team_ids:
        l = df_sp.loc[df_sp['LTeamID'] == id]
        w = df_sp.loc[df_sp['WTeamID'] == id]
        points_for = sum(l.ix[:,'LScore']) + sum(w.ix[:,'WScore'])
        points_against = sum(l.ix[:,'WScore']) + sum(w.ix[:,'LScore'])
        pyth_exp = 1./(1 + (1.*points_against/points_for)**8)
        pythagorean_expectation[id] = pyth_exp
        data_matrix.loc[data_matrix['team_id'] == id,'pyth_exp'] = pyth_exp

    wps = {}
    for id in team_ids:
        l = df_sp.loc[df_sp['LTeamID'] == id]
        w = df_sp.loc[df_sp['WTeamID'] == id]
        win_rate = 1.*len(w)/(len(w)+len(l))
        wps[id] = win_rate
        data_matrix.loc[data_matrix['team_id'] == id,'win_rate'] = win_rate


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

    weighted_wps = {}
    for id in team_ids:
        l = df_sp.loc[df_sp['LTeamID'] == id]
        w = df_sp.loc[df_sp['WTeamID'] == id]
        wins = 0
        games = 0
        for row in l.itertuples():
            if row.WLoc == 'N':
                games += 1.
            elif row.WLoc == 'H':
                games += .6
            else:
                games += 1.4
        for row in w.itertuples():
            if row.WLoc == 'N':
                games += 1.
                wins += 1.
            elif row.WLoc == 'H':
                games += .6
                wins += .6
            else:
                games += 1.4
                wins += 1.4
        weighted_wps[id] = wins/games


    rpis = {}
    for id in team_ids:
        rpis[id] = .25 *weighted_wps[id] + .5*owps[id] + .25*oowps[id]
        data_matrix.loc[data_matrix['team_id'] == id,'rpi'] = rpis[id]
    return data_matrix
print(getDataMatrix(df,year))