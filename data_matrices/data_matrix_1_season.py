from data_matrix import getDataMatrix

for year in range(2017,2002,-1):
    result = getDataMatrix([year])
    result.to_csv('{}dataMatrix.csv'.format(year))
    print("Data matrix created and saved to {}dataMatrix.csv".format(year))
