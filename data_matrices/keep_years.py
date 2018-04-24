#Call as python3 remove_year.py FILENAME YEAR_TO_DELETE

import numpy as np
import pandas as pd
import sys
from subprocess import call
import os

for i in range(2,5):
    folder = './DataMatrices/{}_seasons'.format(i)
    files = os.listdir(folder)
    files = [file for file in files if file.endswith('.csv' )]
    for filename in files:
        year_to_keep =  int(filename[5:9])
        path_and_file = folder + '/' + filename
        df = pd.read_csv(path_and_file)
        new_df = df.loc[df['year'] == year_to_keep]
        new_df.to_csv(path_and_file)
        print("Removed all years except {} and saved to {}".format(year_to_keep, path_and_file))
