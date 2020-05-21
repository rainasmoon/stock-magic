import datetime 
import random

import numpy as np
import pandas as pd


def test_lot():
    print(datetime.date(2019, 1, 1))
    print(datetime.datetime.strptime(str(20191111), '%Y%m%d'))
    
    ts_code = '300000.sz'
    print(ts_code)
    print(ts_code.isdigit())
    print(ts_code[:-3])

    
def test_df():
    df = pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C'],
                 index=pd.date_range('1/1/2000', periods=10))
    
    print(df.empty)
    df = pd.DataFrame()
    print(df.empty)


def test_df_setvalues():
    df = pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C'],
                 index=pd.date_range('1/1/2000', periods=10))
#     print(df)
    df['D1'] = [i * 10 for i in range(10)]
    df['D2'], df['D3'] = (10, 100)
    df['D4'] = df['D1'] / (df['D3'] - df['D2']) * 100
    print(df[['D1', 'D2', 'D3', 'D4']])


def test_df_setvalues_1():
    x = []
    x.append([1, 2])
    x.append([4, 5, 6])
    df = pd.DataFrame(x, columns=['a', 'b', 'c'])
    print(df)


def test_str():
    print(int('10'))
    print('ST' in '*ST小宝')
    print('ST' in '*SAT小宝')
    print('ST' in '小宝')
    print('ST' not in 'ST小宝')

    
def test_str_format():
    
    print('A:', '    B')
    print('A:', '{0:10}'.format('B'), 'C')
    print('{0:10},{1},{2}'.format('大中国', '我爱我家', '秦香莲'))
    print('{0:10},{1},{2}'.format('大中国家', '我爱家', '秦香莲'))
    print('{0:10},{1},{2}'.format('mad', '我爱我家', '秦香莲'))
    print('{0:10},{1},{2}'.format('best', '我爱家', '秦香莲'))


def test_nan():
    print(np.NaN)
    s = 's'
    print(s.ljust(5))
    s = np.NaN
    print(str(s).ljust(5))

    
def test_date():
    
    begin = datetime.date(2010, 1, 1)
    end = datetime.date(2019, 11, 1)
    days = []
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        if day.weekday() in [5, 6]:
            continue
        days.append(day)
        
    print('counts:', len(days))
#     sample = random.sample(days, 100)
    print('step:', int(len(days) / 100))
    sample = [days[i] for i in range(0, len(days), int(len(days) / 100))] 
    print(sample)
    print(len(sample))


def test_str():
    print('abcd.1234'.replace('.', ''))
    print('000001.sz'[7:9])
    print('000001.sz'[:6])
    

# test_str_format()
test_str()
#test_date()
