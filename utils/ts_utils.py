# -*- coding: utf-8 -*-
import os

import pandas as pd
from . import ts_utils_api as ts
from . import common_utils as utils

COMMEN_FILE_PATH = utils.read_config('datas', 'path') + '/v1'

test_ts_code_1 = '000001.SZ'
test_ts_code_2 = '002018.SZ'

DEBUG = True

def to_date(date):
    return pd.to_datetime(date)

def make(df):
    df['date'] = to_date(df.date)
    df.set_index('date', inplace=True)
    return df

def call_today_indexs():
    df = ts.call_today_indexs()
    df.set_index('code', inplace=True)
    return df


def call_today_stocks():
    df = ts.call_today_stocks()
    return df

def call_stock(ts_code, start_date, end_date):
    if not ts_code.isdigit():
        ts_code = ts_code[:-3]
    df = ts.call_stock(ts_code, start_date, end_date)

    df = make(df)
    
    return df


def call_sh_index():
    '''获得上证指数的交易数据'''
    df = ts.call_sh_index()
    df = make(df)
    return df


