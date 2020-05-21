# -*- coding: utf-8 -*-

import datetime
import random

import pandas as pd
import a_strategy


def backward_test():
    begin = datetime.date(2019, 1, 1)
    end = datetime.date(2019, 1, 10)

    for i in range((end - begin).days + 1):
            day = begin + datetime.timedelta(days=i)
            aday = day.strftime("%Y%m%d")
            a_strategy.trick(aday)


def backward_test_permonth():

    begin = datetime.date(2010, 1, 1)

    r_final_report = []

    for i in range(10):
        day = begin + datetime.timedelta(days=i * 30)
        aday = day.strftime("%Y%m%d")
        r_final_report.append(a_strategy.trick(aday))
    df = pd.DataFrame(r_final_report, columns=['aday', 'rounds', 'win_ratio', 'win_lose_ratio', 'max_lose', 'sharpe_ratio'])
    print('FINAL SUMMURY:\n', df.dropna())
    print(df.describe())
    print('END.')


def build_sample_day():
    begin = datetime.date(2010, 1, 1)
    end = datetime.date(2019, 11, 1)
    days = []
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        if day.weekday() in [5, 6]:
            continue
        days.append(day)
    sample = [days[i] for i in range(0, len(days), int(len(days) / 100))]
#     sample = random.sample(days, 100)
    print('SAMPLE DATE:\n', len(sample))
    print(sample)


def backward_test_sampledate():
    begin = datetime.date(2010, 1, 1)
    end = datetime.date(2019, 11, 24)
    days = []
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        if day.weekday() in [5, 6]:
            continue
        days.append(day)
    sample = [days[i] for i in range(0, len(days), int(len(days) / 100))]
    r_final_report = []
    for day in sample:
        aday = day.strftime("%Y%m%d")
        r_final_report.append(a_strategy.trick(aday))
    df = pd.DataFrame(r_final_report, columns=['aday', 'rounds', 'win_ratio', 'win_lose_ratio', 'max_lose', 'sharpe_ratio', 'max_win'])
    print('FINAL SUMMURY:\n', df.dropna())
    print(df.describe())
    print('END.')



backward_test()

