#! env/bin/python
import pandas as pd
import re


PATTERN = '^ATM_ZEN X ABRA'
FIRST_LINE = 'type corrected station  id year month day  hour  minute value plus_minus   error    unknown'
newfile = open('data/data.txt', 'w')
newfile.write(FIRST_LINE)
newfile.write('\n')
newfile.close()


with open('data/ostana.332') as file:
    newfile = None
    newfile = open('data/data.txt', 'a')

    for line in file:
        if re.match(PATTERN, line):
            newfile = open('data/data.txt', 'a')
            newfile.write(line)
            newfile.close()

data = pd.read_csv('data/data.txt', sep = '\n')
dataframe = pd.DataFrame(data)
data.head()
print(dataframe.head())