from tournament import Bracket, Team, get_row

#Simple example function
def lower_id_wins(t1,t2):
    if t1.id > t2.id:
        return t2
    return t1

#Example function using a row from a data_matrix
#t1 and t2 are team objects
#they have .name and .id member variables (and others that shouldn't be needed in these types of functions)
def higher_glicko_wins(t1,t2):
    row = get_row(t1,t2)#This returns the row from the data_matrix representing the game between teams t1 and t2
    #use it to predict just like you normally would
    if row.iloc[0].glicko_0 > row.iloc[0].glicko_1:
        return t1 if t1.id > t2.id else t2
    else:
        return t2 if t1.id > t2.id else t1

#Need to specify path for calculation of team stats, results and glicko scores
path = "./data_matrices/DataMatrices/1_seasons/"
filename = '1_seasons_combined.csv'

#make prediction function as shown in examples above
prediction_function = higher_glicko_wins

#source: https://www.ncaa.com/news/basketball-men/bracket-beat/2017-01-10/march-madness-how-do-your-past-brackets-stack
#2018 source: ESPN Tournament Challenge app has a bracket getting a 60 as 50.5 percentile
average_scores = {2011: 53.12637, 2012: 82.98597, 2013: 69.97803, 2014: 60.14319, 2015: 83.25845, 2016: 68.17819, 2017: 65.66010, 2018: 59.9}
brackets = {}
for year in range(2003,2018):
    brackets[year] = Bracket(path,filename,year)
    if year in average_scores:
        print("{} Score: {}, Average Score: {}".format(year, brackets[year].score_tournament(prediction_function), average_scores[year]))
    else:
        print("{} Score: {}".format(year, brackets[year].score_tournament(prediction_function)))

path = "./data_matrices/DataMatrices/2_seasons/"
filename = '2_seasons_combined.csv'

#make prediction function as shown in examples above
prediction_function = higher_glicko_wins

#source: https://www.ncaa.com/news/basketball-men/bracket-beat/2017-01-10/march-madness-how-do-your-past-brackets-stack
#2018 source: ESPN Tournament Challenge app has a bracket getting a 60 as 50.5 percentile
average_scores = {2011: 53.12637, 2012: 82.98597, 2013: 69.97803, 2014: 60.14319, 2015: 83.25845, 2016: 68.17819, 2017: 65.66010, 2018: 59.9}
brackets = {}
for year in range(2004,2018):
    brackets[year] = Bracket(path,filename,year)
    if year in average_scores:
        print("{} Score: {}, Average Score: {}".format(year, brackets[year].score_tournament(prediction_function), average_scores[year]))
    else:
        print("{} Score: {}".format(year, brackets[year].score_tournament(prediction_function)))
