from data_matrix import getDataMatrix
import pickle

for year in range(2017,2002,-1):
    result, team_stats, team_results, glicko = getDataMatrix([year])
    result.to_csv('{}dataMatrix.csv'.format(year))
    with open("{}_team_stats.p".format(year), 'wb') as file:
        pickle.dump(team_stats, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}_team_results.p".format(year), 'wb') as file:
        pickle.dump(team_results, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}_glicko.p".format(year), 'wb') as file:
        pickle.dump(glicko, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Data matrix created and saved to {}dataMatrix.csv".format(year))
