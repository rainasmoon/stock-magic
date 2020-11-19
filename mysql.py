'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import utils.ts_pro as TSUtils
import utils.DBUtils as DBUtils
import utils.utils as Utils

engine_ts = DBUtils.get_engine()

def read_data(table_name):
    sql = "SELECT * FROM " + table_name +  " LIMIT 20"
    df = pd.read_sql_query(sql, engine_ts)
    return df


def write_data(df, sql_table):
    res = df.to_sql(sql_table, engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)


def get_data():
    df = read_data('stock_basic')
    if df.empty:
        pro = TSUtils.get_pro()
        print('CALL Tushare...')
        df = pro.stock_basic()
        write_data(df, 'stock_basic')
    return df

def get_index():
    print('CALL old TS...')
    df = ts.get_k_data(code='sh', ktype='D', autype='qfq', start='1990-12-20')
    write_data(df, 'stock_index')
    return df

def get_calender(start, end):
    print('CALL pro ...')
    df = TSUtils.get_pro().trade_cal(exchange_id='SSE', is_open=1, start_date=start, end_date=end)
    write_data(df, 'calender')
    return df


if __name__ == '__main__':
    print('clear stock_index...')
    DBUtils.truncate('stock_index')
    
    print('set stock_index...')
    df = get_index()

    print('clear calender...')
    DBUtils.truncate('calender')

    print('set calender...')
    df = get_calender(Utils.day0, Utils.get_today())

    print('SAMPLE:')
    df = read_data('calender')
    print(df.tail())
