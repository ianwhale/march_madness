#Call as python3 remove_year.py FILENAME YEAR_TO_DELETE

import numpy as np
import pandas as pd
import sys
from subprocess import call

filename = sys.argv[1]
year_to_delete =  int(sys.argv[1][5:9])
script = "cat key.csv {} > temp.csv".format(filename)
call(script, shell = True)
df = pd.read_csv("temp.csv")
new_df = df.loc[df['year'] != year_to_delete]
new_df.to_csv(filename)
script = "rm temp.csv"
call(script, shell = True)
print("Removed year except {}".format(year_to_delete))