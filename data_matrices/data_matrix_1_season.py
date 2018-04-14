import numpy as np
import pandas as pd
from glicko2 import Player

def glicko_rounds(glicko, df):
    for row in df.itertuples():
        w = row.WTeamID
        l = row.LTeamID

        w_rating, l_rating = glicko[w].getRating(), glicko[l].getRating()
        w_rd, l_rd = glicko[w].getRd(), glicko[l].getRd()

        glicko[w].update_player([l_rating], [l_rd], [1])
        glicko[l].update_player([w_rating], [w_rd], [0])

def getDataMatrix(years):
    """
    df: dataframe to calculate statistics on (Regular season, postseason tournements, both)
    year: year to analyze
    """
    df_reg_season = pd.read_csv('data/RegularSeasonDetailedResults.csv')
    df_ncaa_tourny = pd.read_csv('data/NCAATourneyDetailedResults.csv')
    df = pd.concat([df_reg_season,df_ncaa_tourny])
    df.sort_values(by=['DayNum'])
    df_sp = df.loc[df['Season'].isin(years)]

    team_ids = set(df_sp.WTeamID).union(set(df_sp.LTeamID))

    glicko = dict(zip(list(team_ids), [Player() for _ in range(len(team_ids))]))
    team_results = {}
    team_stats = {}
    for id in team_ids:
        team_results[id] = []
        team_stats[id] = {'games': 0.0, 'points': 0, 'fgm': 0, 'fga': 0, 'fgm3': 0, 'fga3': 0, 'ftm': 0, 'fta': 0, 'or': 0, 'dr': 0, 'to': 0, 'ast': 0, 'stl': 0, 'blk': 0, 'pf': 0,'opp_points': 0, 'opp_fgm': 0, 'opp_fga': 0, 'opp_fgm3': 0, 'opp_fga3': 0, 'opp_ftm': 0, 'opp_fta': 0, 'opp_or': 0, 'opp_dr': 0, 'opp_to': 0, 'opp_ast': 0, 'opp_stl': 0, 'opp_blk': 0, 'opp_pf': 0, 'possesions': 0}


    data_matrix = df_sp["Season"].to_dict()

    for row in df_sp.itertuples():
        data_matrix[row.Index] = {'year': data_matrix[row.Index]}
        if row.LTeamID < row.WTeamID:
            #glicko
            w_rating, l_rating = glicko[row.WTeamID].getRating(), glicko[row.LTeamID].getRating()
            w_rd, l_rd = glicko[row.WTeamID].getRd(), glicko[row.LTeamID].getRd()

            data_matrix[row.Index]['glicko_0'] = l_rating
            data_matrix[row.Index]['glicko_1'] = w_rating

            glicko[row.LTeamID].update_player([l_rating], [l_rd], [1])
            glicko[row.WTeamID].update_player([w_rating], [w_rd], [0])

            #RPI and win percentage
            #win percentage
            temp = 0
            for game in team_results[row.LTeamID]:
                temp += game['result']
            if len(team_results[row.LTeamID]) == 0:
                wp0 = 0
            else:
                wp0 = float(temp)/len(team_results[row.LTeamID])
            data_matrix[row.Index]['win_rate_0'] = wp0

            temp = 0
            for game in team_results[row.WTeamID]:
                temp += game['result']
            if len(team_results[row.WTeamID]) == 0:
                wp1 = 0
            else:
                wp1 = float(temp)/len(team_results[row.WTeamID])
            data_matrix[row.Index]['win_rate_1'] = wp1

            #weighted win percentage
            temp = 0.0
            for game in team_results[row.LTeamID]:
                if game['loc'] == 'N':
                    temp += 1*game['result']
                elif game['loc'] == 'H':
                    temp += 1.4*game['result']
                else:
                    temp += .6*game['result']
            if len(team_results[row.LTeamID]) == 0:
                wwp0 = 0
            else:
                wwp0 = temp/len(team_results[row.LTeamID])
            data_matrix[row.Index]['win_rate_0'] = wwp0

            temp = 0.0
            for game in team_results[row.WTeamID]:
                if game['loc'] == 'N':
                    temp += 1*game['result']
                elif game['loc'] == 'A':
                    temp += 1.4*game['result']
                else:
                    temp += .6*game['result']
            if len(team_results[row.WTeamID]) == 0:
                wwp1 = 0
            else:
                wwp1 = temp/len(team_results[row.WTeamID])
            data_matrix[row.Index]['weighted_win_rate_1'] = wwp1

            #Opponents win percentage
            temp = 0
            denom = 0.0
            for game in team_results[row.LTeamID]:
                for game2 in team_results[game['opponent']]:
                    if game2['opponent'] != row.LTeamID:
                        temp += game2['result']
                        denom += 1
            if denom == 0:
                owp0 = 0
            else:
                owp0 = temp/denom
            data_matrix[row.Index]['opponents_win_rate_0'] = owp0

            temp = 0
            denom = 0.0
            for game in team_results[row.WTeamID]:
                for game2 in team_results[game['opponent']]:
                    if game2['opponent'] != row.WTeamID:
                        temp += game2['result']
                        denom += 1
            if denom == 0:
                owp1 = 0
            else:
                owp1 = temp/denom
            data_matrix[row.Index]['opponents_win_rate_1'] = owp1

            #Opponents opponents win percentage
            temp = 0
            denom = 0.0
            for game in team_results[row.LTeamID]:
                for game2 in team_results[game['opponent']]:
                    for game3 in team_results[game2['opponent']]:
                        if game3['opponent'] != row.LTeamID:
                            temp += game3['result']
                            denom += 1
            if denom == 0:
                oowp0 = 0
            else:
                oowp0 = temp/denom
            data_matrix[row.Index]['opponents_opponents_win_rate_0'] = oowp0

            temp = 0
            denom = 0.0
            for game in team_results[row.WTeamID]:
                for game2 in team_results[game['opponent']]:
                    for game3 in team_results[game2['opponent']]:
                        if game3['opponent'] != row.WTeamID:
                            temp += game3['result']
                            denom += 1
            if denom == 0:
                oowp1 = 0
            else:
                oowp1 = temp/denom
            data_matrix[row.Index]['opponents_opponents_win_rate_1'] = oowp1

            team_results[row.WTeamID].append({'opponent': row.LTeamID, 'result': 1, 'loc': row.WLoc})
            if row.WLoc == 'A':
                l = 'H'
            elif row.WLoc == 'H':
                l = 'A'
            else:
                l = 'N'
            team_results[row.LTeamID].append({'opponent': row.WTeamID, 'result': 0, 'loc': l})

            data_matrix[row.Index]['rpi_0'] = .25*wwp0 + .5*owp0 + .25*oowp0
            data_matrix[row.Index]['rpi_1'] = .25*wwp1 + .5*owp1 + .25*oowp1

            #ids and labels
            data_matrix[row.Index]['id_0'] = row.LTeamID
            data_matrix[row.Index]['id_1'] = row.WTeamID
            data_matrix[row.Index]['label'] = 1

            if team_stats[row.LTeamID]['games'] == 0:
                team_stats[row.LTeamID]['games'] = -1
            if team_stats[row.WTeamID]['games'] == 0:
                team_stats[row.WTeamID]['games'] = -1

            data_matrix[row.Index]['points_0'] = team_stats[row.LTeamID]['points']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['points_1'] = team_stats[row.WTeamID]['points']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fgm_0'] = team_stats[row.LTeamID]['fgm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fgm_1'] = team_stats[row.WTeamID]['fgm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fga_0'] = team_stats[row.LTeamID]['fga']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fga_1'] = team_stats[row.WTeamID]['fga']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fgm3_0'] = team_stats[row.LTeamID]['fgm3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fgm3_1'] = team_stats[row.WTeamID]['fgm3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fga3_0'] = team_stats[row.LTeamID]['fga3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fga3_1'] = team_stats[row.WTeamID]['fga3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fta_0'] = team_stats[row.LTeamID]['fta']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fta_1'] = team_stats[row.WTeamID]['fta']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['ftm_0'] = team_stats[row.LTeamID]['ftm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['or_0'] = team_stats[row.LTeamID]['or']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['ftm_1'] = team_stats[row.WTeamID]['ftm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['or_1'] = team_stats[row.WTeamID]['or']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['dr_0'] = team_stats[row.LTeamID]['dr']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['dr_1'] = team_stats[row.WTeamID]['dr']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['ast_0'] = team_stats[row.LTeamID]['ast']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['ast_1'] = team_stats[row.WTeamID]['ast']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['to_0'] = team_stats[row.LTeamID]['to']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['to_1'] = team_stats[row.WTeamID]['to']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['stl_0'] = team_stats[row.LTeamID]['stl']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['stl_1'] = team_stats[row.WTeamID]['stl']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['blk_0'] = team_stats[row.LTeamID]['blk']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['blk_1'] = team_stats[row.WTeamID]['blk']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['pf_0'] = team_stats[row.LTeamID]['pf']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['pf_1'] = team_stats[row.WTeamID]['pf']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_points_0'] = team_stats[row.LTeamID]['opp_points']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_points_1'] = team_stats[row.WTeamID]['opp_points']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fgm_0'] = team_stats[row.LTeamID]['opp_fgm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fgm_1'] = team_stats[row.WTeamID]['opp_fgm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fga_0'] = team_stats[row.LTeamID]['opp_fga']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fga_1'] = team_stats[row.WTeamID]['opp_fga']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fgm3_0'] = team_stats[row.LTeamID]['opp_fgm3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fgm3_1'] = team_stats[row.WTeamID]['opp_fgm3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fga3_0'] = team_stats[row.LTeamID]['opp_fga3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fga3_1'] = team_stats[row.WTeamID]['opp_fga3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fta_0'] = team_stats[row.LTeamID]['opp_fta']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fta_1'] = team_stats[row.WTeamID]['opp_fta']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_ftm_0'] = team_stats[row.LTeamID]['opp_ftm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_or_0'] = team_stats[row.LTeamID]['opp_or']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_ftm_1'] = team_stats[row.WTeamID]['opp_ftm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_or_1'] = team_stats[row.WTeamID]['opp_or']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_dr_0'] = team_stats[row.LTeamID]['opp_dr']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_dr_1'] = team_stats[row.WTeamID]['opp_dr']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_ast_0'] = team_stats[row.LTeamID]['opp_ast']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_ast_1'] = team_stats[row.WTeamID]['opp_ast']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_to_0'] = team_stats[row.LTeamID]['opp_to']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_to_1'] = team_stats[row.WTeamID]['opp_to']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_stl_0'] = team_stats[row.LTeamID]['opp_stl']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_stl_1'] = team_stats[row.WTeamID]['opp_stl']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_blk_0'] = team_stats[row.LTeamID]['opp_blk']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_blk_1'] = team_stats[row.WTeamID]['opp_blk']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_pf_0'] = team_stats[row.LTeamID]['opp_pf']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_pf_1'] = team_stats[row.WTeamID]['opp_pf']/team_stats[row.WTeamID]['games']

            #possesions and offensive/defensive defensive efficiencies
            poss_0 = row.LFGA-row.LOR+row.LTO+(.4*row.LFTA)
            poss_1 = row.WFGA-row.WOR+row.WTO+(.4*row.WFTA)
            data_matrix[row.Index]['poss_0'] = team_stats[row.LTeamID]['possesions']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['poss_1'] = team_stats[row.WTeamID]['possesions']/team_stats[row.WTeamID]['games']

            if team_stats[row.LTeamID]['games'] == -1:
                team_stats[row.LTeamID]['games'] = 0
            if team_stats[row.WTeamID]['games'] == -1:
                team_stats[row.WTeamID]['games'] = 0

            if team_stats[row.LTeamID]['possesions'] == 0:
                team_stats[row.LTeamID]['possesions'] = -1
            if team_stats[row.WTeamID]['possesions'] == 0:
                team_stats[row.WTeamID]['possesions'] = -1

            data_matrix[row.Index]['def_eff_0'] = team_stats[row.LTeamID]['opp_points']/team_stats[row.LTeamID]['possesions']*100.0
            data_matrix[row.Index]['def_eff_1'] = team_stats[row.WTeamID]['opp_points']/team_stats[row.WTeamID]['possesions']*100.0
            data_matrix[row.Index]['off_eff_0'] = team_stats[row.WTeamID]['points']/team_stats[row.LTeamID]['possesions']*100.0
            data_matrix[row.Index]['off_eff_1'] = team_stats[row.WTeamID]['points']/team_stats[row.WTeamID]['possesions']*100.0

            if team_stats[row.LTeamID]['possesions'] == -1:
                team_stats[row.LTeamID]['possesions'] = 0
            if team_stats[row.WTeamID]['possesions'] == -1:
                team_stats[row.WTeamID]['possesions'] = 0

            #Pythagorean expectation
            if team_stats[row.LTeamID]['points'] == 0:
                data_matrix[row.Index]['pyth_exp_0'] = 0
            else:
                data_matrix[row.Index]['pyth_exp_0'] = 1.0/(1 + (team_stats[row.LTeamID]['opp_points']*1.0/team_stats[row.LTeamID]['points'])**8)
            if team_stats[row.WTeamID]['points'] == 0:
                data_matrix[row.Index]['pyth_exp_1'] = 0
            else:
                data_matrix[row.Index]['pyth_exp_1'] = 1.0/(1 + (team_stats[row.WTeamID]['opp_points']*1.0/team_stats[row.WTeamID]['points'])**8)

            #Update Basic statistics
            team_stats[row.LTeamID]['possesions'] += row.LFGA-row.LOR+row.LTO+(.4*row.LFTA)
            team_stats[row.WTeamID]['possesions'] += row.WFGA-row.WOR+row.WTO+(.4*row.WFTA)
            team_stats[row.LTeamID]['games'] += 1
            team_stats[row.WTeamID]['games'] += 1
            team_stats[row.LTeamID]['points'] += row.LScore
            team_stats[row.WTeamID]['points'] += row.WScore
            team_stats[row.LTeamID]['fgm'] += row.LFGM
            team_stats[row.WTeamID]['fgm'] += row.WFGM
            team_stats[row.LTeamID]['fga'] += row.LFGA
            team_stats[row.WTeamID]['fga'] += row.WFGA
            team_stats[row.LTeamID]['fgm3'] += row.LFGM3
            team_stats[row.WTeamID]['fgm3'] += row.WFGM3
            team_stats[row.LTeamID]['fga3'] += row.LFGA3
            team_stats[row.WTeamID]['fga3'] += row.WFGA3
            team_stats[row.LTeamID]['fta'] += row.LFTA
            team_stats[row.WTeamID]['fta'] += row.WFTA
            team_stats[row.LTeamID]['ftm'] += row.LFTM
            team_stats[row.WTeamID]['ftm'] += row.WFTM
            team_stats[row.LTeamID]['or'] += row.LOR
            team_stats[row.WTeamID]['or'] += row.WOR
            team_stats[row.LTeamID]['dr'] += row.LDR
            team_stats[row.WTeamID]['dr'] += row.WDR
            team_stats[row.LTeamID]['ast'] += row.LAst
            team_stats[row.WTeamID]['ast'] += row.WAst
            team_stats[row.LTeamID]['to'] += row.LTO
            team_stats[row.WTeamID]['to'] += row.WTO
            team_stats[row.LTeamID]['stl'] += row.LStl
            team_stats[row.WTeamID]['stl'] += row.WStl
            team_stats[row.LTeamID]['blk'] += row.LBlk
            team_stats[row.WTeamID]['blk'] += row.WBlk
            team_stats[row.LTeamID]['pf'] += row.LPF
            team_stats[row.WTeamID]['pf'] += row.WPF
            team_stats[row.LTeamID]['opp_points'] += row.WScore
            team_stats[row.WTeamID]['opp_points'] += row.LScore
            team_stats[row.LTeamID]['opp_fgm'] += row.WFGM
            team_stats[row.WTeamID]['opp_fgm'] += row.LFGM
            team_stats[row.LTeamID]['opp_fga'] += row.WFGA
            team_stats[row.WTeamID]['opp_fga'] += row.LFGA
            team_stats[row.LTeamID]['opp_fgm3'] += row.WFGM3
            team_stats[row.WTeamID]['opp_fgm3'] += row.LFGM3
            team_stats[row.LTeamID]['opp_fga3'] += row.WFGA3
            team_stats[row.WTeamID]['opp_fga3'] += row.LFGA3
            team_stats[row.LTeamID]['opp_fta'] += row.WFTA
            team_stats[row.WTeamID]['opp_fta'] += row.LFTA
            team_stats[row.LTeamID]['opp_ftm'] += row.WFTM
            team_stats[row.WTeamID]['opp_ftm'] += row.LFTM
            team_stats[row.LTeamID]['opp_or'] += row.WOR
            team_stats[row.WTeamID]['opp_or'] += row.LOR
            team_stats[row.LTeamID]['opp_dr'] += row.WDR
            team_stats[row.WTeamID]['opp_dr'] += row.LDR
            team_stats[row.LTeamID]['opp_ast'] += row.WAst
            team_stats[row.WTeamID]['opp_ast'] += row.LAst
            team_stats[row.LTeamID]['opp_to'] += row.WTO
            team_stats[row.WTeamID]['opp_to'] += row.LTO
            team_stats[row.LTeamID]['opp_stl'] += row.WStl
            team_stats[row.WTeamID]['opp_stl'] += row.LStl
            team_stats[row.LTeamID]['opp_blk'] += row.WBlk
            team_stats[row.WTeamID]['opp_blk'] += row.LBlk
            team_stats[row.LTeamID]['opp_pf'] += row.WPF
            team_stats[row.WTeamID]['opp_pf'] += row.LPF

        else:
            #glicko
            w_rating, l_rating = glicko[row.WTeamID].getRating(), glicko[row.LTeamID].getRating()
            w_rd, l_rd = glicko[row.WTeamID].getRd(), glicko[row.LTeamID].getRd()

            data_matrix[row.Index]['glicko_1'] = l_rating
            data_matrix[row.Index]['glicko_0'] = w_rating

            glicko[row.LTeamID].update_player([l_rating], [l_rd], [1])
            glicko[row.WTeamID].update_player([w_rating], [w_rd], [0])

            #win percentage
            temp = 0
            for game in team_results[row.LTeamID]:
                temp += game['result']
            if len(team_results[row.LTeamID]) == 0:
                wp1 = 0
            else:
                wp1 = float(temp)/len(team_results[row.LTeamID])
            data_matrix[row.Index]['win_rate_1'] = wp1

            temp = 0
            for game in team_results[row.WTeamID]:
                temp += game['result']
            if len(team_results[row.WTeamID]) == 0:
                wp0 = 0
            else:
                wp0 = float(temp)/len(team_results[row.WTeamID])
            data_matrix[row.Index]['win_rate_0'] = wp0

            #weighted win percentage
            temp = 0.0
            for game in team_results[row.LTeamID]:
                if game['loc'] == 'N':
                    temp += 1*game['result']
                elif game['loc'] == 'H':
                    temp += 1.4*game['result']
                else:
                    temp += .6*game['result']
            if len(team_results[row.LTeamID]) == 0:
                wwp1 = 0
            else:
                wwp1 = temp/len(team_results[row.LTeamID])
            data_matrix[row.Index]['weighted_win_rate_1'] = wwp1

            temp = 0.0
            for game in team_results[row.WTeamID]:
                if game['loc'] == 'N':
                    temp += 1*game['result']
                elif game['loc'] == 'A':
                    temp += 1.4*game['result']
                else:
                    temp += .6*game['result']
            if len(team_results[row.WTeamID]) == 0:
                wwp0 = 0
            else:
                wwp0 = temp/len(team_results[row.WTeamID])
            data_matrix[row.Index]['weighted_win_rate_0'] = wwp0

            #Opponents win percentage
            temp = 0
            denom = 0.0
            for game in team_results[row.LTeamID]:
                for game2 in team_results[game['opponent']]:
                    if game2['opponent'] != row.LTeamID:
                        temp += game2['result']
                        denom += 1
            if denom == 0:
                owp1 = 0
            else:
                owp1 = temp/denom
            data_matrix[row.Index]['opponents_win_rate_1'] = owp1

            temp = 0
            denom = 0.0
            for game in team_results[row.WTeamID]:
                for game2 in team_results[game['opponent']]:
                    if game2['opponent'] != row.WTeamID:
                        temp += game2['result']
                        denom += 1
            if denom == 0:
                owp0 = 0
            else:
                owp0 = temp/denom
            data_matrix[row.Index]['opponents_win_rate_0'] = owp0

            #Opponents opponents win percentage
            temp = 0
            denom = 0.0
            for game in team_results[row.LTeamID]:
                for game2 in team_results[game['opponent']]:
                    for game3 in team_results[game2['opponent']]:
                        if game3['opponent'] != row.LTeamID:
                            temp += game3['result']
                            denom += 1
            if denom == 0:
                oowp1 = 0
            else:
                oowp1 = temp/denom
            data_matrix[row.Index]['opponents_opponents_win_rate_1'] = oowp1

            temp = 0
            denom = 0.0
            for game in team_results[row.WTeamID]:
                for game2 in team_results[game['opponent']]:
                    for game3 in team_results[game2['opponent']]:
                        if game3['opponent'] != row.WTeamID:
                            temp += game3['result']
                            denom += 1
            if denom == 0:
                oowp0 = 0
            else:
                oowp0 = temp/denom
            data_matrix[row.Index]['opponents_opponents_win_rate_0'] = oowp1

            data_matrix[row.Index]['rpi_1'] = .25*wwp1 + .5*owp1 + .25*oowp1
            data_matrix[row.Index]['rpi_0'] = .25*wwp0 + .5*owp0 + .25*oowp0

            team_results[row.WTeamID].append({'opponent': row.LTeamID, 'result': 1, 'loc': row.WLoc})
            if row.WLoc == 'A':
                l = 'H'
            elif row.WLoc == 'H':
                l = 'A'
            else:
                l = 'N'
            team_results[row.LTeamID].append({'opponent': row.WTeamID, 'result': 0, 'loc': l})

            #ids and labels
            data_matrix[row.Index]['id_1'] = row.LTeamID
            data_matrix[row.Index]['id_0'] = row.WTeamID
            data_matrix[row.Index]['label'] = 0

            if team_stats[row.LTeamID]['games'] == 0:
                team_stats[row.LTeamID]['games'] = -1
            if team_stats[row.WTeamID]['games'] == 0:
                team_stats[row.WTeamID]['games'] = -1

            data_matrix[row.Index]['points_1'] = team_stats[row.LTeamID]['points']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['points_0'] = team_stats[row.WTeamID]['points']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fgm_1'] = team_stats[row.LTeamID]['fgm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fgm_0'] = team_stats[row.WTeamID]['fgm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fga_1'] = team_stats[row.LTeamID]['fga']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fga_0'] = team_stats[row.WTeamID]['fga']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fgm3_1'] = team_stats[row.LTeamID]['fgm3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fgm3_0'] = team_stats[row.WTeamID]['fgm3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fga3_1'] = team_stats[row.LTeamID]['fga3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fga3_0'] = team_stats[row.WTeamID]['fga3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['fta_1'] = team_stats[row.LTeamID]['fta']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['fta_0'] = team_stats[row.WTeamID]['fta']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['ftm_1'] = team_stats[row.LTeamID]['ftm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['or_1'] = team_stats[row.LTeamID]['or']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['ftm_0'] = team_stats[row.WTeamID]['ftm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['or_0'] = team_stats[row.WTeamID]['or']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['dr_1'] = team_stats[row.LTeamID]['dr']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['dr_0'] = team_stats[row.WTeamID]['dr']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['ast_1'] = team_stats[row.LTeamID]['ast']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['ast_0'] = team_stats[row.WTeamID]['ast']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['to_1'] = team_stats[row.LTeamID]['to']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['to_0'] = team_stats[row.WTeamID]['to']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['stl_1'] = team_stats[row.LTeamID]['stl']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['stl_0'] = team_stats[row.WTeamID]['stl']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['blk_1'] = team_stats[row.LTeamID]['blk']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['blk_0'] = team_stats[row.WTeamID]['blk']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['pf_1'] = team_stats[row.LTeamID]['pf']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['pf_0'] = team_stats[row.WTeamID]['pf']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_points_1'] = team_stats[row.LTeamID]['opp_points']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_points_0'] = team_stats[row.WTeamID]['opp_points']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fgm_1'] = team_stats[row.LTeamID]['opp_fgm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fgm_0'] = team_stats[row.WTeamID]['opp_fgm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fga_1'] = team_stats[row.LTeamID]['opp_fga']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fga_0'] = team_stats[row.WTeamID]['opp_fga']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fgm3_1'] = team_stats[row.LTeamID]['opp_fgm3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fgm3_0'] = team_stats[row.WTeamID]['opp_fgm3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fga3_1'] = team_stats[row.LTeamID]['opp_fga3']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fga3_0'] = team_stats[row.WTeamID]['opp_fga3']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_fta_1'] = team_stats[row.LTeamID]['opp_fta']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_fta_0'] = team_stats[row.WTeamID]['opp_fta']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_ftm_1'] = team_stats[row.LTeamID]['opp_ftm']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_or_1'] = team_stats[row.LTeamID]['opp_or']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_ftm_0'] = team_stats[row.WTeamID]['opp_ftm']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_or_0'] = team_stats[row.WTeamID]['opp_or']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_dr_1'] = team_stats[row.LTeamID]['opp_dr']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_dr_0'] = team_stats[row.WTeamID]['opp_dr']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_ast_1'] = team_stats[row.LTeamID]['opp_ast']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_ast_0'] = team_stats[row.WTeamID]['opp_ast']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_to_1'] = team_stats[row.LTeamID]['opp_to']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_to_0'] = team_stats[row.WTeamID]['opp_to']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_stl_1'] = team_stats[row.LTeamID]['opp_stl']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_stl_0'] = team_stats[row.WTeamID]['opp_stl']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_blk_1'] = team_stats[row.LTeamID]['opp_blk']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_blk_0'] = team_stats[row.WTeamID]['opp_blk']/team_stats[row.WTeamID]['games']
            data_matrix[row.Index]['opp_pf_1'] = team_stats[row.LTeamID]['opp_pf']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['opp_pf_0'] = team_stats[row.WTeamID]['opp_pf']/team_stats[row.WTeamID]['games']

            #possesions and offensive/defensive defensive efficiencies
            poss_1 = row.LFGA-row.LOR+row.LTO+(.4*row.LFTA)
            poss_0 = row.WFGA-row.WOR+row.WTO+(.4*row.WFTA)
            data_matrix[row.Index]['poss_1'] = team_stats[row.LTeamID]['possesions']/team_stats[row.LTeamID]['games']
            data_matrix[row.Index]['poss_0'] = team_stats[row.WTeamID]['possesions']/team_stats[row.WTeamID]['games']

            if team_stats[row.LTeamID]['games'] == -1:
                team_stats[row.LTeamID]['games'] = 0
            if team_stats[row.WTeamID]['games'] == -1:
                team_stats[row.WTeamID]['games'] = 0

            if team_stats[row.LTeamID]['possesions'] == 0:
                team_stats[row.LTeamID]['possesions'] = -1
            if team_stats[row.WTeamID]['possesions'] == 0:
                team_stats[row.WTeamID]['possesions'] = -1

            data_matrix[row.Index]['def_eff_1'] = team_stats[row.LTeamID]['opp_points']/team_stats[row.LTeamID]['possesions']*100.0
            data_matrix[row.Index]['def_eff_0'] = team_stats[row.WTeamID]['opp_points']/team_stats[row.WTeamID]['possesions']*100.0
            data_matrix[row.Index]['off_eff_1'] = team_stats[row.WTeamID]['points']/team_stats[row.LTeamID]['possesions']*100.0
            data_matrix[row.Index]['off_eff_0'] = team_stats[row.WTeamID]['points']/team_stats[row.WTeamID]['possesions']*100.0

            if team_stats[row.LTeamID]['possesions'] == -1:
                team_stats[row.LTeamID]['possesions'] = 0
            if team_stats[row.WTeamID]['possesions'] == -1:
                team_stats[row.WTeamID]['possesions'] = 0

            #Pythagorean expectation
            if team_stats[row.LTeamID]['points'] == 0:
                data_matrix[row.Index]['pyth_exp_1'] = .5
            else:
                data_matrix[row.Index]['pyth_exp_1'] = 1.0/(1 + (team_stats[row.LTeamID]['opp_points']*1.0/team_stats[row.LTeamID]['points'])**8)
            if team_stats[row.WTeamID]['points'] == 0:
                data_matrix[row.Index]['pyth_exp_0'] = .5
            else:
                data_matrix[row.Index]['pyth_exp_0'] = 1.0/(1 + (team_stats[row.WTeamID]['opp_points']*1.0/team_stats[row.WTeamID]['points'])**8)


            #Update basic statistics
            team_stats[row.LTeamID]['possesions'] += row.LFGA-row.LOR+row.LTO+(.4*row.LFTA)
            team_stats[row.WTeamID]['possesions'] += row.WFGA-row.WOR+row.WTO+(.4*row.WFTA)
            team_stats[row.LTeamID]['games'] += 1
            team_stats[row.WTeamID]['games'] += 1
            team_stats[row.LTeamID]['points'] += row.LScore
            team_stats[row.WTeamID]['points'] += row.WScore
            team_stats[row.LTeamID]['fgm'] += row.LFGM
            team_stats[row.WTeamID]['fgm'] += row.WFGM
            team_stats[row.LTeamID]['fga'] += row.LFGA
            team_stats[row.WTeamID]['fga'] += row.WFGA
            team_stats[row.LTeamID]['fgm3'] += row.LFGM3
            team_stats[row.WTeamID]['fgm3'] += row.WFGM3
            team_stats[row.LTeamID]['fga3'] += row.LFGA3
            team_stats[row.WTeamID]['fga3'] += row.WFGA3
            team_stats[row.LTeamID]['fta'] += row.LFTA
            team_stats[row.WTeamID]['fta'] += row.WFTA
            team_stats[row.LTeamID]['ftm'] += row.LFTM
            team_stats[row.WTeamID]['ftm'] += row.WFTM
            team_stats[row.LTeamID]['or'] += row.LOR
            team_stats[row.WTeamID]['or'] += row.WOR
            team_stats[row.LTeamID]['dr'] += row.LDR
            team_stats[row.WTeamID]['dr'] += row.WDR
            team_stats[row.LTeamID]['ast'] += row.LAst
            team_stats[row.WTeamID]['ast'] += row.WAst
            team_stats[row.LTeamID]['to'] += row.LTO
            team_stats[row.WTeamID]['to'] += row.WTO
            team_stats[row.LTeamID]['stl'] += row.LStl
            team_stats[row.WTeamID]['stl'] += row.WStl
            team_stats[row.LTeamID]['blk'] += row.LBlk
            team_stats[row.WTeamID]['blk'] += row.WBlk
            team_stats[row.LTeamID]['pf'] += row.LPF
            team_stats[row.WTeamID]['pf'] += row.WPF
            team_stats[row.LTeamID]['opp_points'] += row.WScore
            team_stats[row.WTeamID]['opp_points'] += row.LScore
            team_stats[row.LTeamID]['opp_fgm'] += row.WFGM
            team_stats[row.WTeamID]['opp_fgm'] += row.LFGM
            team_stats[row.LTeamID]['opp_fga'] += row.WFGA
            team_stats[row.WTeamID]['opp_fga'] += row.LFGA
            team_stats[row.LTeamID]['opp_fgm3'] += row.WFGM3
            team_stats[row.WTeamID]['opp_fgm3'] += row.LFGM3
            team_stats[row.LTeamID]['opp_fga3'] += row.WFGA3
            team_stats[row.WTeamID]['opp_fga3'] += row.LFGA3
            team_stats[row.LTeamID]['opp_fta'] += row.WFTA
            team_stats[row.WTeamID]['opp_fta'] += row.LFTA
            team_stats[row.LTeamID]['opp_ftm'] += row.WFTM
            team_stats[row.WTeamID]['opp_ftm'] += row.LFTM
            team_stats[row.LTeamID]['opp_or'] += row.WOR
            team_stats[row.WTeamID]['opp_or'] += row.LOR
            team_stats[row.LTeamID]['opp_dr'] += row.WDR
            team_stats[row.WTeamID]['opp_dr'] += row.LDR
            team_stats[row.LTeamID]['opp_ast'] += row.WAst
            team_stats[row.WTeamID]['opp_ast'] += row.LAst
            team_stats[row.LTeamID]['opp_to'] += row.WTO
            team_stats[row.WTeamID]['opp_to'] += row.LTO
            team_stats[row.LTeamID]['opp_stl'] += row.WStl
            team_stats[row.WTeamID]['opp_stl'] += row.LStl
            team_stats[row.LTeamID]['opp_blk'] += row.WBlk
            team_stats[row.WTeamID]['opp_blk'] += row.LBlk
            team_stats[row.LTeamID]['opp_pf'] += row.WPF
            team_stats[row.WTeamID]['opp_pf'] += row.LPF

    data_matrix = pd.DataFrame.from_dict(data_matrix, 'index')
    cols = ['year', 'id_0', 'id_1', 'ftm_0', 'fta_0', 'fgm_0', 'fga_0', 'fgm3_0', 'fga3_0', 'ast_0', 'blk_0', 'or_0', 'dr_0', 'stl_0', 'to_0', 'pf_0', 'points_0', 'poss_0', 'opp_ftm_0', 'opp_fta_0', 'opp_fgm_0', 'opp_fga_0', 'opp_fgm3_0', 'opp_fga3_0', 'opp_ast_0', 'opp_blk_0', 'opp_or_0', 'opp_dr_0', 'opp_stl_0', 'opp_to_0', 'opp_pf_0', 'opp_points_0', 'pyth_exp_0', 'win_rate_0', 'opponents_win_rate_0', 'opponents_opponents_win_rate_0', 'weighted_win_rate_0', 'rpi_0', 'off_eff_0', 'def_eff_0', 'glicko_0', 'ftm_1', 'fta_1', 'fgm_1', 'fga_1', 'fgm3_1', 'fga3_1', 'ast_1', 'blk_1', 'or_1', 'dr_1', 'stl_1', 'to_1', 'pf_1', 'points_1', 'poss_1', 'opp_ftm_1', 'opp_fta_1', 'opp_fgm_1', 'opp_fga_1', 'opp_fgm3_1', 'opp_fga3_1', 'opp_ast_1', 'opp_blk_1', 'opp_or_1', 'opp_dr_1', 'opp_stl_1', 'opp_to_1', 'opp_pf_1', 'opp_points_1', 'pyth_exp_1', 'win_rate_1', 'opponents_win_rate_1', 'opponents_opponents_win_rate_1', 'weighted_win_rate_1', 'rpi_1', 'off_eff_1', 'def_eff_1', 'glicko_1', 'label']
    data_matrix = data_matrix[cols]
    return data_matrix

for year in range(2017,2002,-1):
    result = getDataMatrix([year])
    result.to_csv('{}dataMatrix.csv'.format(year))
    print("Data matrix created and saved to {}dataMatrix.csv".format(year))
