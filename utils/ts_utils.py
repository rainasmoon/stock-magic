# -*- coding: utf-8 -*-
from functools import lru_cache
import json
import os

import pandas as pd
import tushare as ts
import common_utils

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


def to_date_v1(date):
    return pd.to_datetime(date)


def make(df):    
    # pandas有个专门把字符串转为时间格式的函数，to_datetime。第一个参数是原始数据，第二个参数是原始数据的格式
    df['trade_date'] = to_date(df['trade_date'])
    # 把trade_date设置为索引
    df.set_index('trade_date', inplace=True)
    return df


def make_v1(df):
    df['date'] = to_date_v1(df.date)
    df.set_index('date', inplace=True)
    return df


def make_ts_code(df):
    df.set_index('ts_code', inplace=True)
    return df


def call_last_tradeday_before(aday):
# don't have permitions
#     df = pro.trade_cal(exchange='', start_date=aday, end_date=aday)

    return '20191122'


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
    yesterday = common_utils.yesterday()
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


@lru_cache()
def call_index_v1():
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


@lru_cache()
def call_today_all_v1():
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


@lru_cache() 
def call_report_v1(year, quarter):
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


@lru_cache()   
def call_stock_v1(ts_code, start_date, end_date):
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
    df = make_v1(df)
    
    return df


def call_sh_index_v1():
    '''获得上证指数的交易数据'''
    today = common_utils.today()
    filePath = COMMEN_FILE_PATH + f'v1_sh_index_{today}.csv'
    if not os.path.exists(filePath):
        print('CALL TUSHARE...')
        df = ts.get_k_data(code='sh', ktype='D',
          autype='qfq', start='1990-12-20')
        df.to_csv(filePath)
    else:
        df = pd.read_csv(filePath)
    df = make_v1(df)
    return df


@lru_cache()
def call_deposit_rate_v1():
    df = ts.get_deposit_rate()
    df = df [(df.date == df.date.max()) & (df.deposit_type == '定期存款整存整取(一年)')]
    return df['rate'].max()


@lru_cache()
def call_money_supply():
    '''
    返回值说明：

    month :统计时间
    m2 :货币和准货币（广义货币M2）(亿元)
    m2_yoy:货币和准货币（广义货币M2）同比增长(%)
    m1:货币(狭义货币M1)(亿元)
    m1_yoy:货币(狭义货币M1)同比增长(%)
    m0:流通中现金(M0)(亿元)
    m0_yoy:流通中现金(M0)同比增长(%)
    cd:活期存款(亿元)
    cd_yoy:活期存款同比增长(%)
    qm:准货币(亿元)
    qm_yoy:准货币同比增长(%)
    ftd:定期存款(亿元)
    ftd_yoy:定期存款同比增长(%)
    sd:储蓄存款(亿元)
    sd_yoy:储蓄存款同比增长(%)
    rests:其他存款(亿元)
    rests_yoy:其他存款同比增长(%)

    '''
    df = ts.get_money_supply()
     
    return [df.loc[0, 'm0'], df.loc[0, 'm1'], df.loc[0, 'm2']]


@lru_cache()
def call_gdp():
    df = ts.get_gdp_quarter()
    return df


@lru_cache()
def call_cpi():
    df = ts.get_cpi()
    return df.loc[0, 'cpi']


@lru_cache()
def call_ppi():
    df = ts.get_ppi()
    return df 


@lru_cache()
def call_shibor():
    '''
    获取银行间同业拆放利率数据，目前只提供2006年以来的数据。

参数说明：

    year:年份(YYYY),默认为当前年份

返回值说明：

    date:日期
    ON:隔夜拆放利率
    1W:1周拆放利率
    2W:2周拆放利率
    1M:1个月拆放利率
    3M:3个月拆放利率
    6M:6个月拆放利率
    9M:9个月拆放利率
    1Y:1年拆放利率

    '''
    df = ts.shibor_data() 
    return df


if __name__ == '__main__':
    r = call_daily('20191202')
    print(r)
    r = call_stock_qfq('000001.SZ', '20191001', '20191101')
    print(r)
