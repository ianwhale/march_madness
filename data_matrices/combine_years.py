# Combine all years in a folder together

import numpy as np
import pandas as pd
import sys
from subprocess import call
import os

folders = os.listdir("./DataMatrices")

for folder_name in folders:
    folder = './DataMatrices/{}'.format(folder_name)
    files = os.listdir(folder)
    files = [file for file in files if file.endswith('.csv' ) and not file.endswith('_combined')]
    df = pd.DataFrame()
    for filename in files:
        path_and_file = folder + '/' + filename
        new_df = pd.read_csv(path_and_file)
        df = pd.concat([df,new_df])
    df.to_csv(folder + '/' + folder_name + '_combined.csv')
    print("Made concatenated matrix and saved to {}".format(folder + '/' + folder_name + '_combined.csv'))
