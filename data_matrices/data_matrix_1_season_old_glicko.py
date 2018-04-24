from data_matrix import getGlickoDataMatrix

for year in range(2017,2002,-1):
    result = getGlickoDataMatrix([year])
    result.to_csv('{}dataMatrix.csv'.format(year))
    print("Data matrix created and saved to {}oldGlickoDataMatrix.csv".format(year))
