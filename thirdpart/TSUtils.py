## encoding: utf-8 ##

import tushare as ts
import Utils
import datetime

ts.set_token('5e7376feb8fd52cc3a964a5e8386799360e399b36136e52885ed3323')
pro = ts.pro_api()

def get_pro():
    print('CALL TS pro ...')
    return pro

def get_ts():
    print('CALL TS ...')
    return ts

def get_stock_canlender(startdate, enddate):
    start = startdate
    end = enddate
    if type(startdate) == datetime.datetime:
        start = Utils.format_d(startdate)
    elif(len(startdate) != 8):
        start = Utils.date2d(startdate)
    
    if type(enddate) == datetime.datetime:
        end = Utils.format_d(enddate)
    elif(len(enddate) != 8):
        end = Utils.date2d(enddate)

    df = get_pro().trade_cal(exchange_id='', is_open=1, start_date=start,
                         end_date=end)
    if df.empty:
        print('WARN: empty: %s, %s' % (startdate, enddate))
        return [startdate, enddate]

    return list(df.iloc[:,1])

def get_daily(stock_code, start_dt, end_dt):

    df = get_pro().daily(ts_code=stock_code, start_date=start_dt, end_date=end_dt)
    return df

if __name__ == '__main__':
    print('test')
    aresult = get_stock_canlender('2020-01-01', '2020-10-01')
    print(aresult)
