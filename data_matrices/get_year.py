from data_matrix import getDataMatrix
import sys

year = int(sys.argv[1])
data_matrix = getDataMatrix([year])
data_matrix.to_csv('{}dataMatrix.csv'.format(year))
print("Data matrix created and saved to {}dataMatrix.csv".format(year))
