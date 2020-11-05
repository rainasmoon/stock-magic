## encoding: utf-8 ##

import tushare as ts
import Utils
import datetime

ts.set_token('5e7376feb8fd52cc3a964a5e8386799360e399b36136e52885ed3323')
pro = ts.pro_api()

def get_pro():
    print('CALL pro ...')
    return pro

def get_ts():
    print('CALL TS ...')
    return ts


def get_daily(stock_code, start_dt, end_dt):
    print('CALL TS pro...:' + stock_code)
    df = pro.daily(ts_code=stock_code, start_date=start_dt, end_date=end_dt)
    return df

if __name__ == '__main__':
    print('test')
    aresult = get_stock_calender('2020-01-01', '2020-10-01')
    print(aresult)
