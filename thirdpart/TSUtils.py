## encoding: utf-8 ##

import tushare as ts
import Utils

ts.set_token('5e7376feb8fd52cc3a964a5e8386799360e399b36136e52885ed3323')
pro = ts.pro_api()

def get_pro():
    return pro

def get_ts():
    return ts

def get_stock_canlender(startdate, enddate):
    start = startdate
    end = enddate
    if(len(startdate) != 8):
        start = Utils.date2d(startdate)
    if(len(enddate) != 8):
        end = Utils.date2d(enddate)
    print('CALL TS...')
    df = pro.trade_cal(exchange_id='', is_open=1, start_date=start,
                         end_date=end)
    print(df.head())
    if df.empty:
        print('WARN: empty: %s, %s' % (startdate, enddate))
        return [startdate, enddate]
    return list(df.iloc[:,1])

if __name__ == '__main__':
    print('test')
    aresult = get_stock_canlender('2020-01-01', '2020-10-01')
    print(aresult)
