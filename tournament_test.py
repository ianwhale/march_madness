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
year = 2017

#make prediction function as shown in examples above
prediction_function = higher_glicko_wins

b = Bracket(path,filename,year)
b.play_tournament(prediction_function)
print("Score: ", b.score_tournament(prediction_function))
