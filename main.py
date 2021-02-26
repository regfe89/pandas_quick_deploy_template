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
    y_orig = dataframe[name + '_value']
    y_mean = np.mean(y_orig)
    y = np.array(y_orig) - y_mean
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
    min_sigma = 99999999999
    min_value_shift = 0
    sinus_result = []

    for day in range(365):
        sinus_row = []
        
        for index, value in enumerate(result_row):
            sinus = math.sin(2 * math.pi / 365.25 * index + day)
            sinus_row.append(sinus)
        # print(sinus_row)
        sinus_row = np.array(sinus_row, dtype=float)
        sinus_regr = linregress(sinus_row, result_row)
        sinus_m = sinus_regr.slope
        sinus_b = sinus_regr.intercept
        sinus_regr_result = sinus_m * sinus_row + sinus_b
        sig_sum = 0
        for index, value in enumerate(result_row):
            sig_sum += (sinus_regr_result[index] - result_row[index])**2
        sigma = math.sqrt(sig_sum/len(result_row))
        if (sigma < min_sigma):
            min_sigma = sigma
            min_value_shift = day
            sinus_result = sinus_regr_result

    y_sin = np.array(y) - np.array(sinus_result)
    final_regr = linregress(x, y_sin)
    final_m = final_regr.slope
    final_b = final_regr.intercept
    speed_mm_per_year = final_m * 1000 * 365.25
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x, sinus_result, color='green')
    ax.plot(x, y)
    ax.plot(x, final_m * x + final_b, color="red")
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    # ax.xaxis.set_major_formatter(myFmt)
    ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series, speed = ' + str(speed_mm_per_year) + ' mm per year')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig('final_regr' + '_' + filename + '_' + name + ".png")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x_orig, sinus_result, color='green')
    ax.plot(x_orig, y)
    ax.plot(x_orig, final_m * x + final_b, color="red")
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    ax.xaxis.set_major_formatter(myFmt)
    ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series, speed = ' + str(speed_mm_per_year) + ' mm per year')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig('original_with_regr' + '_' + filename + '_' + name + ".png")

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x_orig, y)
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(round(float(x), 4), ',')))
    ax.xaxis.set_major_formatter(myFmt)
    ax.set(xlabel='date', ylabel='baseline length', title= filename + ' ' + name + ' baseline time series, speed = ' + str(speed_mm_per_year) + ' mm per year')
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.savefig('original' + '_' + filename + '_' + name + ".png")

    


def make_custom():
    for file in os.listdir('data/'):
        filename = file[:-4]
        dataframe = pd.read_csv("data/" + file, parse_dates=['date'])
        dataframe.set_index('date')
        make_custom_plot(dataframe, filename, 'east')
        make_custom_plot(dataframe, filename, 'north')



make_custom()

