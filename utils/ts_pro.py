# -*- coding: utf-8 -*-
import os

import pandas as pd
from . import ts_pro_api as pro
from . import utils as utils

COMMEN_FILE_PATH = utils.read_config('datas','path')

test_ts_code_1 = '000001.SZ'
test_ts_code_2 = '002018.SZ'

DEBUG = True

def to_date(date):
    return pd.to_datetime(date, format='%Y%m%d')

def make(df):    
    # pandas有个专门把字符串转为时间格式的函数，to_datetime。第一个参数是原始数据，第二个参数是原始数据的格式
    df['trade_date'] = to_date(df['trade_date'])
    # 把trade_date设置为索引
    df.set_index('trade_date', inplace=True)
    return df

def make_ts_code(df):
    df.set_index('ts_code', inplace=True)
    return df

def call_all_stocks():
    '''
    ts_code     str     TS代码
    symbol     str     股票代码
    name     str     股票名称
    area     str     所在地域
    industry     str     所属行业
    fullname     str     股票全称
    enname     str     英文全称
    market     str     市场类型 （主板/中小板/创业板/科创板）
    exchange     str     交易所代码
    curr_type     str     交易货币
    list_status     str     上市状态： L上市 D退市 P暂停上市
    list_date     str     上市日期
    delist_date     str     退市日期
    is_hs     str     是否沪深港通标的，N否 H沪股通 S深股通
    '''
    
    filePath = COMMEN_FILE_PATH + '/all_stocks.csv'
    if not os.path.exists(filePath):
        data = pro.call_all_stocks()
        if data.empty:
            return data
        data.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        data = pd.read_csv(filePath)
    return make_ts_code(data)


def call_stock_info(ts_code):
    data = call_all_stocks()
    if ts_code in data.index:
        return data.loc[ts_code]
    else:
        return pd.Series()   


def call_daily(aday):
    path = COMMEN_FILE_PATH + '/daily/'
    path = path + aday[:4] + '/' +  aday[4:6] + '/' + aday[6:8] + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    filePath = path  + f'daily_{aday}.csv'
    if not os.path.exists(filePath):
        
        df = pro.call_daily(aday)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    return make_ts_code(df)


def call_stock(ts_code, start_date, end_date):
    filePath = COMMEN_FILE_PATH + f'/stock_{ts_code}_{start_date}_{end_date}.csv'
    if not os.path.exists(filePath):
        
        df = pro.call_stock(ts_code, start_date, end_date)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    return make(df)

def call_stock_qfq_raw(ts_code, start_date, end_date):
    path = COMMEN_FILE_PATH + '/stocks/' + ts_code[:3] + '/' + ts_code + '/'
    yesterday = utils.yesterday()
    oldFile = None
    filePath = None
    if not os.path.exists(path):
        os.makedirs(path)
        filePath = path + f'stock_qfq_{ts_code}_{yesterday}.csv'
    else:
        files = os.scandir(path)
        for file in files:
            fileName = file.name
            dataday =fileName[-12:-4]
            if end_date > dataday:
                filePath = path + f'stock_qfq_{ts_code}_{yesterday}.csv'
                oldFile = path + fileName
            else:
                filePath = path + fileName 
            break
        else:
            filePath = path + f'stock_qfq_{ts_code}_{yesterday}.csv'
    if not os.path.exists(filePath):
        astock = call_stock_info(ts_code)
        ipo_date = str(astock['list_date'])
     
        df = pro.call_stock_qfq_raw(ts_code, ipo_date, yesterday)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG:
            print('STORE:', filePath)
        if oldFile:
            os.remove(oldFile)
    else:
        df = pd.read_csv(filePath)
    
    return df 


def call_stock_qfq(ts_code, start_date, end_date):
    df = make(call_stock_qfq_raw(ts_code, start_date, end_date))
    df = df.sort_index()
    return df.loc[start_date:end_date]

if __name__ == '__main__':
    r = call_all_stocks()
    print(r)
