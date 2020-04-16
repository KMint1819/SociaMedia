import pandas as pd
import numpy as np

p = '../data/hw2/smm-hw2-fakenewsdetecion/train.csv'
df = pd.read_csv(p)
print(df.shape)

#

new_df = df[~df['text'].isnull()]
print(new_df.shape)