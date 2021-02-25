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

def make_raw_plot(dataframe, filename, name):
    fig, ax = plt.subplots(figsize=(10, 10))
    # y=np.array(dataframe[name + '_value'].dropna().values, dtype=float)
    # x=np.array(pd.to_datetime(dataframe['date'].dropna()).index.values, dtype=float)
    y=np.array(dataframe[name + '_value'].values, dtype=float)
    x=np.array(pd.to_datetime(dataframe['date']).index.values, dtype=float)
    stats = linregress(x, y)
    m = stats.slope
    b = stats.intercept
    ax.plot(x, y)
    ax.plot(x, m * x + b, color="red")
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    ax.xaxis.set_major_formatter(myFmt)
    ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig(filename + '_' + name + ".png")

def make_decomposed_plot(dataframe, filename, name):
    # fig, ax = plt.subplots(figsize=(30, 30))
    # y=np.array(dataframe[name + '_value'].dropna().values, dtype=float)
    # x=np.array(pd.to_datetime(dataframe['date'].dropna()).index.values, dtype=float)
    # y=np.array(dataframe[name + '_value'].values, dtype=float)
    # x=np.array(pd.to_datetime(dataframe['date']).index.values, dtype=float)
    # x = dataframe['date']
    # if(name == 'north'):
    #     y = dataframe['north_value']
    # else:
    #     y = dataframe['east_value']
    # stats = linregress(x, y)
    # m = stats.slope
    # b = stats.intercept
    # y_original = y
    y = seasonal_decompose(dataframe, model='additive', period = 365)
    print('seasonal:')
    print(y.seasonal)
    print('observed:')
    print(y_original)
    y.plot()
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gcf().set_size_inches(10, 10)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gca().get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    # disabling the offset on y axis
    # ax.xticklabel_format(useOffset=False)
    # ax.plot(x, y_original)
    # ax.plot(x, m * x + b, color="red")
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    ax.xaxis.set_major_formatter(myFmt)
    # ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig(filename + '_' + name + ".png")


def make_decomposed():
    for file in os.listdir('data/'):
        filename = file[:-4]
        dataframe = pd.read_csv("data/" + file, header=0, index_col=0)
        # dataframe['date'] = pd.to_datetime(dataframe['date'])
        decomposed = seasonal_decompose(dataframe, model='additive', period=365)
        # decomposed = seasonal_decompose(dataframe, model='multiplicative', period=365)
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(decomposed.observed)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
        plt.savefig('observed_' + filename + '_' + 'north' + ".png")
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(decomposed.trend)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
        plt.savefig('trend_' + filename + '_' + 'north' + ".png")
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(decomposed.seasonal)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
        plt.savefig('seasonal_' + filename + '_' + 'north' + ".png")
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(decomposed.resid)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
        plt.savefig('residual_' + filename + '_' + 'north' + ".png")
    
        # dataframe = dataframe.set_index('date')
        # dataframe = dataframe.asfreq('YS')
        # dataframe = dataframe.asfreq(dataframe.index.freq or to_offset(timeframe.Timespan).freqstr)
        # print(dataframe.index)
        # make_decomposed_plot(dataframe, filename, 'east')
        # make_decomposed_plot(dataframe, filename, 'north')

def make_raw():
    for file in os.listdir('data/'):
        filename = file[:-4]
        dataframe = pd.read_csv("data/" + file, parse_dates=['date'])
        dataframe.set_index('date')
        # make_raw_plot(dataframe, filename, 'east')
        make_raw_plot(dataframe, filename, 'north')



# def make_decomposed(component):
#     for file in os.listdir('data/'):
#         filename = file[:-4]
#         dataframe = pd.read_csv("data/" + file, parse_dates=['date'])
#         x = dataframe.day
#         y = dataframe.north_value
#         stats = linregress(x, y)
#         m = stats.slope
#         b = stats.intercept
#         plt.plot(x, y)
#         plt.plot(x, m * x + b, color="red")
#         plt.savefig('decomposed_' + filename + '_' + 'north' + '.png')

# make_decomposed()
# make_decomposed('north')
make_raw()


def make_dummy():
    dummyframe = pd.read_csv('data/data.csv', header=0, index_col=0)
    decomposed = seasonal_decompose(dummyframe, model='additive', period = 365)
    decomposed.plot()
    plt.savefig("dummy.png")
# make_dummy()

def make_dummy2():
    dummyframe = pd.read_csv('data/data2.csv', header=0, index_col=0)
    decomposed = seasonal_decompose(dummyframe, model='multiplicative', period = 12)
    decomposed.plot()
    plt.savefig("dummy2.png")
# make_dummy2()