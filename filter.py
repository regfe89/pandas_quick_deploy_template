#! env/bin/python
import os
import fnmatch
from shutil import copyfile
import shutil

rootdir = 'data/2019'
destdir = 'data/actual/'

dirname = os.path.dirname(__file__)
dirname = dirname[:-2]

print(dirname)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if fnmatch.fnmatch(file, 'qstana.*'):
            copyfile(os.path.join(subdir, file), dirname + '/data/actual/' + file)
            print(os.path.join(subdir, file))