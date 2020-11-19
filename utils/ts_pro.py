# -*- coding: utf-8 -*-
import json
import os

import pandas as pd
import tushare as ts
import utils

COMMEN_FILE_PATH = '../datas/'

f = open('./config_api.json', 'r')
config_jd_api = json.load(f)
app_key = config_jd_api['app_key']

ts.set_token(app_key)
pro = ts.pro_api()

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


def call_last_tradeday(aday):
    df = pro.trade_cal(exchange='SSE', is_open='1', start_date='20150601',
                       end_date='20150630', fields='cal_date')
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
    
    filePath = COMMEN_FILE_PATH + 'all_stocks.csv'
    if not os.path.exists(filePath):
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,fullname,enname,market,exchange,curr_type,list_status,delist_date,is_hs')
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
    path = COMMEN_FILE_PATH + 'daily/'
    path = path + aday[:4] + '/' +  aday[4:6] + '/' + aday[6:8] + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    filePath = path  + f'daily_{aday}.csv'
    if not os.path.exists(filePath):
        
        df = pro.daily(trade_date=aday)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    return make_ts_code(df)


def call_stock(ts_code, start_date, end_date):
    filePath = COMMEN_FILE_PATH + f'stock_{ts_code}_{start_date}_{end_date}.csv'
    if not os.path.exists(filePath):
        
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df.empty:
            return df
        df.to_csv(filePath)
        if DEBUG: 
            print('STORE:', filePath)
    else:
        df = pd.read_csv(filePath)
    return make(df)


def call_stock_qfq_raw_ts():
    '''
    ts_code 	str 	Y 	证券代码
api 	str 	N 	pro版api对象，如果初始化了set_token，此参数可以不需要
start_date 	str 	N 	开始日期 (格式：YYYYMMDD)
end_date 	str 	N 	结束日期 (格式：YYYYMMDD)
asset 	str 	Y 	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
adj 	str 	N 	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
freq 	str 	Y 	数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D。目前有120积分的用户自动具备分钟数据试用权限（每分钟5次），正式权限请在QQ群私信群主。
ma 	list 	N 	均线，支持任意合理int数值
factors 	list 	N 	股票因子（asset='E'有效）支持 tor换手率 vr量比
adjfactor 	str 	N 	复权因子，在复权数据是，如果此参数为True，返回的数据中则带复权因子，默认为False。 该功能从1.2.33版本开始生效
    '''
    df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    return df


def call_stock_qfq_raw(ts_code, start_date, end_date):
    path = COMMEN_FILE_PATH + 'stocks/' + ts_code[:3] + '/' + ts_code + '/'
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
     
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=ipo_date,
                        end_date=yesterday)
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

def get_daily(stock_code, start_dt, end_dt):
    print('CALL TS pro...:' + stock_code)
    df = pro.daily(ts_code=stock_code, start_date=start_dt, end_date=end_dt)
    return df

if __name__ == '__main__':
    r = call_last_tradeday('20150607')
    print(r)
