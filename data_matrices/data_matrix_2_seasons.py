from data_matrix import getDataMatrix

for year in range(2017,2003,-1):
    result = getDataMatrix([year-1,year])
    result.to_csv('{}-{}dataMatrix.csv'.format(year-1,year))
    with open("{}-{}_team_stats.p".format(year-1,year), 'wb') as file:
        pickle.dump(team_stats, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}-{}_team_results.p".format(year-1,year), 'wb') as file:
        pickle.dump(team_results, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("{}-{}_glicko.p".format(year-1,year), 'wb') as file:
        pickle.dump(team_stats, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Data matrix created and saved to {}-{}dataMatrix.csv".format(year-1,year))
