# -*- coding: utf-8 -*-
import os

import pandas as pd
import tushare as ts
import utils as utils

COMMEN_FILE_PATH = '../datas/v1/'

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
    '''
    获取所有指数实时行情
    
    code:指数代码
    name:指数名称
    change:涨跌幅
    open:开盘点位
    preclose:昨日收盘点位
    close:收盘点位
    high:最高点位
    low:最低点位
    volume:成交量(手)
    amount:成交金额（亿元）
    
    '''
    df = ts.get_index()
    df.set_index('code', inplace=True)
    return df


def call_today_stocks():
    '''
    获取股票实时行情
    code：代码
    name:名称
    changepercent:涨跌幅
    trade:现价
    open:开盘价
    high:最高价
    low:最低价
    settlement:昨日收盘价
    volume:成交量
    turnoverratio:换手率
    amount:成交金额
    per:市盈率
    pb:市净率
    mktcap:总市值
    nmc:流通市值

    '''
    df = ts.get_today_all()
    return df


def call_reports(year, quarter):
    '''
    code,代码
    name,名称
    esp,每股收益
    eps_yoy,每股收益同比(%)
    bvps,每股净资产
    roe,净资产收益率(%)
    epcf,每股现金流量(元)
    net_profits,净利润(万元)
    profits_yoy,净利润同比(%)
    distrib,分配方案
    report_date,发布日期
    '''
    
    filePath = COMMEN_FILE_PATH + f'v1_report_{year}_{quarter}.csv'
    if not os.path.exists(filePath):
        df = ts.get_report_data(year, quarter)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    return df   


def call_stock(ts_code, start_date, end_date):
    if not ts_code.isdigit():
        ts_code = ts_code[:-3]
    filePath = COMMEN_FILE_PATH + f'v1_stock_qfq_{ts_code}_{start_date}_{end_date}.csv'
    if not os.path.exists(filePath):
        # code:股票代码，个股主要使用代码，如‘600000’
        # ktype:'D':日数据；‘m’：月数据，‘Y’:年数据
        # autype:复权选择，默认‘qfq’前复权
        # start：起始时间
        # end：默认当前时间
        df = ts.get_k_data(code=ts_code, ktype='m', autype='qfq', start=start_date, end=end_date)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    df = make(df)
    
    return df


def call_sh_index():
    '''获得上证指数的交易数据'''
    today = utils.today()
    filePath = COMMEN_FILE_PATH + f'v1_sh_index_{today}.csv'
    if not os.path.exists(filePath):
        print('CALL TUSHARE...')
        df = ts.get_k_data(code='sh', ktype='D',
          autype='qfq', start='1990-12-20')
        df.to_csv(filePath)
    else:
        df = pd.read_csv(filePath)
    df = make(df)
    return df


if __name__ == '__main__':

    r = call_sh_index()
    print(r)
