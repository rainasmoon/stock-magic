# -*- coding: utf-8 -*-

'''
600:主板
603:
000:深市
002:中小板
300:创业板
688:科创板
ST:
*ST:
'''
'''
1 选出每日涨副在4.5 -5.5之间的
2 去除ST
3 去除价格为30%之上的
4 

TODO:
5 大盘
6 资金管理
7 模拟复盘
6 板块

7 已经退市的股票

NOW:
一定时间之前的股票于今天的对比。

sharp率： （收益-无风险利率）/波动率
胜率是指出手赚钱次数与总出手次数之比；
赔率是指平均每次出手赚到的钱除以平均每次出手赔的钱，也叫做盈亏比。
最大回撤
'''

import a_stock
import common_utils
import ts_utils
from functools import lru_cache
import matplotlib.pyplot as plt

DEBUG = False

def make_position(df, aday):
    today_focus = df.copy()
    today_focus['ts_code_orginal'] = today_focus.index.to_numpy()
    ext_info = today_focus.loc[:, 'ts_code_orginal'].apply(a_stock.a_stock, args=(aday,))
    # 把返回的结果扩展拆分成列
    df_ext = ext_info.str.split(',', expand=True)
    today_focus[['price_max', 'price_min', 'vol_max', 'vol_min', 'stock_name',
                 'stock_industry', 'stock_hs', 'p_pos', 'v_pos']] = df_ext
    today_focus[['price_max', 'price_min', 'vol_max', 'vol_min']] = today_focus[['price_max', 'price_min', 'vol_max', 'vol_min']].applymap(float)
    
    # 计算价格和成交量的位置
    t = today_focus
    t['P_position'] = round((t['close'] - t['price_min']) / (t['price_max'] - t['price_min']) * 100, 2)
    t['V_position'] = round((t['vol'] - t['vol_min']) / (t['vol_max'] - t['vol_min']) * 100, 2)
    
    if DEBUG:
        print('价格和成交量的位置:\n', t)
    return t

@lru_cache()
def select_stocks(aday):
    df = ts_utils.call_daily(aday)
    if df.empty:
        print('NO TRADE')
        return
    # ##
    # 1 选出每日涨副在4.5 -5.5之间的
    # ##
    today_focus = df[(df.pct_chg > 4.5) & (df.pct_chg < 5.5)].copy()
    if DEBUG:
        print('MGAIC STOCKS:\n', today_focus)
    # 根据ts_code查询股票信息
    t = make_position(today_focus, aday)
    # 去掉ST
    t = t[~(t.stock_name.str.contains(r'ST'))].copy()
    
    # 去掉P_position在30%以上的
    t = t[t.P_position < 40].copy()
    
    r = t[[ 'close', 'P_position', 'V_position', 'stock_name', 'stock_industry', 'stock_hs']]
    
    if r.empty:
        print('无合适股票')
        return
    
    if DEBUG:
        print('去掉ST，位置在40以下:\n', t)
        
    return r 

def sell_stocks_now(r):    
    yesterday = ts_utils.call_last_tradeday_before(common_utils.yesterday())
    
    yesterday_df = ts_utils.call_daily(yesterday)
    
    r = r.join(yesterday_df, lsuffix="_L", rsuffix="_R")
    r['RESULT'] = round((r['close_R'] - r['close_L']) / r['close_L'] * 100, 2)
    
    r = r[[ 'close_L', 'close_R', 'P_position', 'V_position', 'stock_name', 'stock_industry', 'RESULT']]
    return r

def sell_stocks(r, aday):
    r['close_L']=r['close']
    r['close_R']=ai_sell(r, aday)
    r['RESULT'] = round((r['close_R'] - r['close_L']) / r['close_L'] * 100, 2)
    r = r[[ 'close_L', 'close_R', 'P_position', 'V_position', 'stock_name', 'stock_industry', 'RESULT']]
    return r

def ai_sell(r, buy_date):
    yesterday = ts_utils.call_last_tradeday_before(common_utils.yesterday())
    r = r.reset_index()
    sell_price = []
    for i in range(len(r)):
        atscode = r.loc[i, 'ts_code']
        eyes_on_date = cool_down_day(buy_date)
        astock_df = ts_utils.call_stock_qfq(atscode, eyes_on_date, yesterday)
        print(astock_df)
        #astock_df['close'].plot()
        #plt.show()
        astock_df = astock_df.reset_index()
        astock_df['pre_max'] = r.loc[i, 'close']
        for j in range(len(astock_df) - 1):
            astock_df.loc[j+1, 'pre_max'] = max(astock_df.loc[j,'close'],
                                                astock_df.loc[j, 'pre_max'])
            if astock_df.loc[j, 'close'] < astock_df.loc[j, 'pre_max']:
                adrop = (astock_df.loc[j, 'pre_max'] - astock_df.loc[j,
                                                                 'close'])/astock_df.loc[j,
                                                                                         'pre_max']
                if adrop > 0.2:
                    sell_price.append(astock_df.loc[j, 'close'])
                    break
        else:
            print('*****************************************************')
            print('*****************************************************')
            print(astock_df)
            print('*****************************************************')
            print('*****************************************************')
            
            if not astock_df.empty:
                sell_price.append(astock_df.loc[len(astock_df)-1, 'close'])
                plot_df = astock_df.copy()
                plot_df.set_index('trade_date', inplace=True)
                plot_df['close'].plot()
                plt.show()
            else:
                sell_price.append(0)

    return sell_price

def cool_down_day(aday):
    return aday

def summary(r):    
    r_desc = r.describe()
    v_std = r_desc.loc['std', 'RESULT']
    if DEBUG:
       print('统计：\n', r_desc)
    
    rounds = len(r)
    win_df = r[r.RESULT > 0]
    lose_df = r[r.RESULT < 0]
    wins = len(win_df)
    # 胜率是指出手赚钱次数与总出手次数之比；
    win_ratio = round(wins / rounds * 100, 2)
    # 赔率是指平均每次出手赚到的钱除以平均每次出手赔的钱，也叫做盈亏比。
    if wins != 0:
        win_lose_ratio = (win_df['RESULT'].sum() / wins) / (lose_df['RESULT'].sum() / len(lose_df)) 
        win_lose_ratio = round(abs(win_lose_ratio), 2)
    else:
        win_lose_ratio = 0
    # 每日報酬(%)=(今天資產淨值-昨天資產淨值)/昨天資產淨值
    # 夏普率= [(每日報酬率平均值- 無風險利率) / (每日報酬的標準差)]x (252平方根)
    # 其中252平方根是因為一年大約有252天交易日，意思是將波動數值從每日調整成年
    # 當然如果資料上無法取得日資料，那用週資料或月資料也是可以。
    # 年化報酬率(%) = (總報酬率+1)^(1/年數) -1
    y_roi = 3
    sharpe_ratio = round((r_desc.loc['mean', 'RESULT'] - y_roi) / r_desc.loc['std', 'RESULT'], 2)
    max_lose = r.loc[r['RESULT'].idxmin(), 'RESULT']
    max_win = r.loc[r['RESULT'].idxmax(), 'RESULT']
    print('胜率：', win_ratio)
    print('赔率：', win_lose_ratio)
    print('最大回撤：', max_lose)
    print('夏普率：', sharpe_ratio)
    return [rounds, win_ratio, win_lose_ratio, max_lose, sharpe_ratio, max_win]



def trick(aday):
    
    print('\n\n')
    print('A DAY:', aday)
    print('******************************************')
    r = select_stocks(aday)

    if type(r).__name__ == 'NoneType':
        return [aday, 'NO TRADE.']
    r = sell_stocks(r, aday)
    summary_info = summary(r)
    return [aday] + summary_info

def show_my_stock():
    aday = common_utils.last_tradeday()
    df = ts_utils.call_daily(aday)
    df = df.loc[['002024.SZ', '300024.SZ', '601633.SH']]
    df = make_position(df, aday)
    print(df.dtypes)
    r = df[['trade_date', 'stock_name', 'P_position', 'V_position']]
    print(r)


if __name__ == '__main__':
    show_my_stock()
    r = select_stocks('20200402')
    print(r)
