#! env/bin/python
import pandas as pd
import re
import os
import fnmatch
from shutil import copyfile
import datetime as dt
import matplotlib.pyplot as plt
from scipy.stats import linregress
import matplotlib.dates as mdates
import matplotlib


SRCDIR = 'data/2020'
DESTDIR = '/data/temporary/'
PATTERN = '^ATM_ZEN X ABRA'
FIRST_LINE = '\"datetime\",\"value\"'

dirname = os.path.dirname(__file__)[:-2]
# open('data/data.csv', 'w').close()

def make_single_file():
    newfile = open('data/data.csv', 'a')
    newfile.write(FIRST_LINE)
    newfile.write('\n')
    newfile.close()
    for subdir, dirs, files in os.walk(SRCDIR):
        for file in files:
            if fnmatch.fnmatch(file, 'ostana.*'):
                copyfile(os.path.join(subdir, file), dirname + DESTDIR + file)

    list_dir = os.listdir('data/temporary')
    for filename in sorted(list_dir):
        with open('data/temporary/' + filename) as datafile:
            newfile = None
            for line in datafile:
                if re.match(PATTERN, line):
                    station = line.split()[2]
                    year = line.split()[4]
                    month = line.split()[5]
                    day = line.split()[6]
                    hour = line.split()[7]
                    value = abs(float(line.split()[9]))
                    datestring = year + '/' + month +  '/' + day +  ' ' + hour + ':0:0'
                    datetime_object = datetime.strptime(datestring, '%Y/%m/%d %H:%M:%S')
                    datestring = datetime_object.strftime("%Y/%m/%d %H:%M:%S")
                    newline = '\"' + datestring + '\"' + ',' + str(value)
                    newfile = open('data/data.csv', 'a')
                    newfile.write(newline)
                    newfile.write('\n')
                    newfile.close()

    for file in os.listdir('data/temporary'):
        os.remove('data/temporary/' + file)


# make_single_file()


# dataframe = pd.read_csv('data/humidity_data.csv')

def make_plot(name):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(dataframe['date'], dataframe[name + '_value'])
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    ax.xaxis.set_major_formatter(myFmt)
    ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig(filename + '_' + name + ".png")


for file in os.listdir('data/'):
    filename = file[:-4]
    dataframe = pd.read_csv("data/" + file, parse_dates=['date'])
    dataframe.set_index('date')
    x = dataframe.date
    myFmt = mdates.DateFormatter('%Y-%m-%d')
    make_plot('east')
    make_plot('north')
    # ax.plot(dataframe['date'], dataframe['value'])
    # ax.get_yaxis().set_major_formatter(
    #     matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    # ax.xaxis.set_major_formatter(myFmt)
    # ax.set(xlabel='date', ylabel='baseline length', title= filename + ' baseline time series')

    # plt.setp(ax.get_xticklabels(), rotation=45)

    # plt.savefig(filename + ".png")


# dataframe['start_time']=dataframe['start_time'].map(dt.datetime.toordinal)

# new_x = dates.datestr2num(date) # where date is '01/02/1991'
# x = dataframe.Height
# y = dataframe.Latitude
# stats = linregress(x, y)
# m = stats.slope
# b = stats.intercept

# plt.scatter(x, y)
# plt.plot(x, m * x + b, color="red")   # I've added a color argument here


# ax.scatter(dataframe.index.values, dataframe['num_value'])

# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)
