import numpy as np
import pandas as pd
import os
import csv

DIR_PATH = '../data/'

## loading data as Pandas dataframes
train = pd.read_csv(os.path.join(DIR_PATH, 'train.csv'), 
                        header='infer', 
                        index_col='id',
                        parse_dates=['timestamp'])
macro = pd.read_csv(os.path.join(DIR_PATH, 'macro.csv'), 
                    header='infer')

tnames = list(train.columns)
mnames = list(macro.columns)

"""
with open('main_columns.txt','w') as f:
    wr = csv.writer(f, dialect='excel')
    wr.writerow(tnames)

with open('macro_columns.txt','w') as f:
    wr = csv.writer(f, dialect='excel')
    wr.writerow(mnames)
"""

with open('main_columns.txt','w') as f:
    for i in tnames:
        f.write(i)
        f.write('\n')

with open('macro_columns.txt','w') as f:
    for j in mnames:
        f.write(j)
        f.write('\n')
