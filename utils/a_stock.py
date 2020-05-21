
import common_utils
import plt_utils
import ts_utils
import pandas as pd

test_ts_code_1 = '000001.SZ'


def show_a_stock(stock_code, end_date):
    print('A STOCK:', stock_code)
    astock = ts_utils.call_stock_info(stock_code)
    
    ipo_date = str(astock['list_date'])
    stock_info = '{0}-{1}-{2}'.format(astock['name'], astock['industry'], astock['symbol'])
    print('STOCKNAME:', stock_info)
    
    df = ts_utils.call_stock_qfq(stock_code, ipo_date, end_date)
    main_info = df.describe().round(2)
    
    price_max = main_info.loc['max', 'high']
    price_min = main_info.loc['min', 'low']
    vol_max = main_info.loc['max', 'vol']
    vol_min = main_info.loc['min', 'vol']
    return f'BIGPIC:[{price_max}:{price_min}:{vol_max}:{vol_min}]'
    
    plt_utils.show_k(df, stock_info)
    plt_utils.show_vol(df, stock_info)
    plt_utils.show_ma(df, stock_info)
    
    df = ts_utils.call_stock_v1(stock_code, ipo_date, end_date)
     
    print('MONTH DATA:\n', df)
     
    main_info = df.describe().round(2)
    print('MAIN INFO:\n', main_info)
     
    plt_utils.show_mon_k_v1(df, stock_info)


def a_stock(stock_code, aday):
    astock = ts_utils.call_stock_info(stock_code)
    if astock.empty :
        return 'nan, nan, nan, nan, "已退市,已退市,N"'
    ipo_date = str(astock['list_date'])
    industry = str(astock['industry'])
    
    stock_info = '{0},{1},{2}'.format(astock['name'].ljust(5, chr(12288)), industry.ljust(5, chr(12288)), astock['is_hs'])
    
    df = ts_utils.call_stock_qfq(stock_code, ipo_date, aday)
    
    main_info = df.describe().round(2)
    
    price_max = main_info.loc['max', 'high']
    price_min = main_info.loc['min', 'low']
    vol_max = main_info.loc['max', 'vol']
    vol_min = main_info.loc['min', 'vol']
    price = df.loc[aday, 'close']
    vol = df.loc[aday, 'vol']
    price_pos = (price - price_min) / (price_max - price_min)
    vol_pos = (vol - vol_min) / (vol_max - vol_min)
    price_pos = round(price_pos, 2)
    vol_pos = round(vol_pos, 2)
    return f'{price_max}, {price_min}, {vol_max}, {vol_min}, {stock_info}, {price_pos}, {vol_pos}'

if __name__ == '__main__':
    
    stock_1 = '002024.SZ'
    stock_2 = '300024.SZ'
    print(a_stock(stock_1, common_utils.yesterday()))
    print(a_stock(stock_2, common_utils.yesterday()))
