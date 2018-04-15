from data_matrix import getDataMatrix

for year in range(2017,2004,-1):
    result = getDataMatrix([year-2,year-1,year])
    result.to_csv('{}-{}dataMatrix.csv'.format(year-2,year))
    print("Data matrix created and saved to {}-{}dataMatrix.csv".format(year-2,year))
