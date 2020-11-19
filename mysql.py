'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import utils.ts_pro as TSUtils
import utils.DBUtils as DBUtils
import utils.utils as Utils
import utils.ts_utils_api as ts_utils_api
import utils.ts_pro_api as ts_pro_api
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
        df = ts_pro.stock_basic()
        write_data(df, 'stock_basic')
    return df

def get_index():
    print('CALL old TS...')
    df = ts_utils_api.call_sh_index()
    write_data(df, 'stock_index')
    return df

def get_calender(start, end):
    print('CALL pro ...')
    df = ts_pro_api.call_calender(start, end)
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
