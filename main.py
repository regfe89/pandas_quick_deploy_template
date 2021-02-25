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
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from pprint import pprint
import math

myFmt = mdates.DateFormatter('%Y-%m-%d')

def make_custom_plot(dataframe, filename, name):
    # fig, ax = plt.subplots(figsize=(10, 10))
    # y=np.array(dataframe[name + '_value'].values, dtype=float)
    x_orig = pd.to_datetime(dataframe['date'])
    x=np.array(pd.to_datetime(dataframe['date']).index.values, dtype=float)
    # x = pd.to_datetime(dataframe['date'])
    y = dataframe['north_value']
    stats = linregress(x, y)
    m = stats.slope
    b = stats.intercept
    # ax.plot(x_orig, y)
    # ax.plot(x_orig, m * x + b, color="red")
    regres_y = m * x + b
    result_row = []
    for index, value in enumerate(regres_y):
        res_value = y[index] - value
        result_row.append(res_value)
    

    for day in range(365):
        sinus_row = []
        fig, ax = plt.subplots(figsize=(10, 10))
        for index, value in enumerate(result_row):
            sinus = math.sin(value * index + day)
            sinus_row.append(sinus)
        ax.plot(x, sinus_row)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
        ax.xaxis.set_major_formatter(myFmt)
        ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series')
        plt.setp(ax.get_xticklabels(), rotation=45)
        plt.savefig(str(day + 1) + '_' + filename + '_' + name + ".png")
    # print(sinus_row)
    # ax.plot(x, m * x + b, color="red")
    


def make_custom():
    for file in os.listdir('data/'):
        filename = file[:-4]
        dataframe = pd.read_csv("data/" + file, parse_dates=['date'])
        dataframe.set_index('date')
        # make_raw_plot(dataframe, filename, 'east')
        make_custom_plot(dataframe, filename, 'north')



make_custom()


