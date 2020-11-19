# -*- encoding: utf-8 -*-
import utils
import plt_utils
import ts_utils
import ts_pro

test_ts_code_1 = '000001.SZ'


def show_a_stock(stock_code, end_date):
    print('A STOCK:', stock_code)
    astock = ts_pro.call_stock_info(stock_code)
    
    ipo_date = str(astock['list_date'])
    stock_info = '{0}-{1}'.format(astock['name'], astock['industry'])    

    df = ts_pro.call_stock_qfq(stock_code, ipo_date, end_date)
    main_info = df.describe().round(2)
    
    price_max = main_info.loc['max', 'high']
    price_min = main_info.loc['min', 'low']
    vol_max = main_info.loc['max', 'vol']
    vol_min = main_info.loc['min', 'vol']
    
    plt_utils.show_k(df, stock_info)
    plt_utils.show_vol(df, stock_info)
    plt_utils.show_ma(df, stock_info)
    
    df = ts_utils.call_stock(stock_code, ipo_date, end_date)
    plt_utils.show_mon_k(df, stock_info)


def a_stock(stock_code, aday):
    astock = ts_pro.call_stock_info(stock_code)
    if astock.empty :
        return 'nan', 0, 0, 0, 0

    ipo_date = str(astock['list_date'])
    df = ts_pro.call_stock_qfq(stock_code, ipo_date, aday)
    
    main_info = df.describe()
    
    price_max = main_info.loc['max', 'high']
    price_min = main_info.loc['min', 'low']
    
    vol_max = main_info.loc['max', 'vol']
    vol_min = main_info.loc['min', 'vol']
    
    price = df.loc[aday, 'close']
    vol = df.loc[aday, 'vol']
    
    price_pos = (price - price_min) / (price_max - price_min)
    vol_pos = (vol - vol_min) / (vol_max - vol_min)

    gr_price_days = len(df[df['close'] > price])
    gr_price_posibility = gr_price_days/ len(df)

    gr_vol_days = len(df[df['vol'] > vol])
    gr_vol_posibility = gr_vol_days/ len(df)

    return astock, price_pos, vol_pos, gr_price_posibility, gr_vol_posibility

if __name__ == '__main__':
    
    stock_1 = '002024.SZ'
    stock_2 = '300024.SZ'
    print(a_stock(stock_1, utils.yesterday()))
    print(a_stock(stock_2, utils.yesterday()))

    show_a_stock(stock_1, utils.yesterday())
