# -*- coding: utf-8 -*-
import tushare as ts
from . import common_utils as utils

ts.set_token(utils.read_config('tushare', 'app_key'))
pro = ts.pro_api()

test_ts_code_1 = '000001.SZ'
test_ts_code_2 = '002018.SZ'

DEBUG = True

def call_last_tradeday(aday):

    if aday == '':
        aday = utils.new_trade_day()

    df = pro.trade_cal(exchange='SSE', start_date=aday,
                       end_date=aday, fields='cal_date, is_open, pretrade_date')

    if df.iloc[0]['is_open']==0 :
        return df.iloc[0]['pretrade_date']
    else:
        return df.iloc[0]['cal_date']

def call_calender(start_date, end_date):
    df = pro.trade_cal(exchange='SSE', is_open='1', start_date=start_date,
                       end_date=end_date, fields='cal_date')
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
    
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,fullname,enname,market,exchange,curr_type,list_status,delist_date,is_hs')
    return data

def call_daily(aday):
    df = pro.daily(trade_date=aday)
    return df


def call_stock(ts_code, start_date, end_date):
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df

def call_stock_qfq_raw(ts_code, start_date, end_date):
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
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start_date,
                    end_date=end_date)
    
    return df 

def get_daily(stock_code, start_dt, end_dt):
    df = pro.daily(ts_code=stock_code, start_date=start_dt, end_date=end_dt)

    return df

