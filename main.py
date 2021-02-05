#! env/bin/python
import pandas as pd
import re
import os
import fnmatch
from shutil import copyfile

ROOTDIR = 'data/2019'
DESTDIR = '/data/temporary/'
PATTERN = '^ATM_ZEN X ABRA'
FIRST_LINE = 'type corrected station  id year month day  hour  minute value plus_minus   error    unknown'

dirname = os.path.dirname(__file__)[:-2]

for subdir, dirs, files in os.walk(ROOTDIR):
    for file in files:
        if fnmatch.fnmatch(file, 'ostana.*'):
            copyfile(os.path.join(subdir, file), dirname + DESTDIR + file)
            # print(os.path.join(subdir, file))
            newfile = open('data/actual/' + file + '_atm_zen.txt', 'a')
            newfile.write(FIRST_LINE)
            newfile.write('\n')
            newfile.close()


            with open('data/temporary/' + file) as datafile:
                newfile = None
                for line in datafile:
                    if re.match(PATTERN, line):
                        newfile = open('data/actual/'  + file + '_atm_zen.txt', 'a')
                        newfile.write(line)
                        newfile.close()




# data = pd.read_csv('data/data.txt', sep = '\n')
# dataframe = pd.DataFrame(data)
# data.head()
# print(dataframe.head())