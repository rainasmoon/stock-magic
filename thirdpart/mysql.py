'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import tushare as ts
import TSUtils
import DBUtils

engine_ts = DBUtils.get_engine()

def read_data():
    sql = """SELECT * FROM stock_basic LIMIT 20"""
    df = pd.read_sql_query(sql, engine_ts)
    return df


def write_data(df, sql_table):
    res = df.to_sql(sql_table, engine_ts, index=False, if_exists='append', chunksize=5000)
    print(res)


def get_data():
    df = read_data()
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


if __name__ == '__main__':
    df = get_index()
    print(df.tail())
    print('end.')
