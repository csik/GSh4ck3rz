import pandas as pd
import os

# Quick hack to test CSVs and pandas

directory = r'/Users/csik/Downloads/INFO4240_STS4240_Design_Workbook_Unit_1 2'

dfs=[]
for entry in os.scandir(directory):
    if (entry.path.endswith(".csv")):
        print(entry.path)
        csv = pd.read_csv(entry.path)
        csv = csv.drop([len(csv)-1, len(csv)-2, len(csv)-3])
        csv.loc[:,'question'] = entry.name # create a column to keep track of what question sheet this was from
        dfs.append(csv)

# Concatinate all the csvs
df = pd.concat(dfs, axis=0)

df[df.Score!=0].groupby(['Grader']).median()
df[df.Score!=0].groupby(['Grader']).mean()
df[df.Score!=0].groupby(['Grader']).std()

df[df.Score>0].groupby(['question']).mean()
df[df.Score>0].groupby(['question']).std()
df[df.Score>0].groupby(['question']).size()
df[df.Score>0].groupby(['question']).median()


