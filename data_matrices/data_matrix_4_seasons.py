from data_matrix import getDataMatrix
import pickle

for year in range(2017,2005,-1):
    result, team_stats, team_results, glicko = getDataMatrix([year-3,year-2,year-1,year])
    result.to_csv('{}-{}dataMatrix.csv'.format(year-3,year))
    with open("{}-{}_team_stats.p".format(year-3,year), 'wb') as file:
        pickle.dump(team_stats, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}-{}_team_results.p".format(year-3,year), 'wb') as file:
        pickle.dump(team_results, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}-{}_glicko.p".format(year-3,year), 'wb') as file:
        pickle.dump(glicko, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Data matrix created and saved to {}-{}dataMatrix.csv".format(year-3,year))
