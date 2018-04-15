from data_matrix import getDataMatrix

for year in range(2017,2005,-1):
    result = getDataMatrix([year-3,year-2,year-1,year])
    result.to_csv('{}-{}dataMatrix.csv'.format(year-3,year))
    print("Data matrix created and saved to {}-{}dataMatrix.csv".format(year-3,year))
