## encoding: utf-8 ##

import tushare as ts

ts.set_token('5e7376feb8fd52cc3a964a5e8386799360e399b36136e52885ed3323')
pro = ts.pro_api()

def get_pro():
    return pro

def get_ts():
    return ts

def get_stock_canlender(startdate, enddate):
    df = pro.trade_cal(exchange_id='', is_open=1, start_date=startdate,
                         end_date=enddate)
    return list(df.iloc[:,1])
