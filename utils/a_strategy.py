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

import utils
import ts_pro

DEBUG = False

def select_stocks(aday):
    
    df = ts_pro.call_daily(aday)
    if df.empty:
        print('NO TRADE')
        return
    # ##
    # 1 选出每日涨副在4.5 -5.5之间的
    # ##
    today_focus = df[(df.pct_chg > 4.5) & (df.pct_chg < 5.5)].copy()
    if DEBUG:
        print('MGAIC STOCKS:\n', today_focus)
        
    return today_focus

def show_my_stock():
    aday = utils.yesterday()
    df = ts_pro.call_daily(aday)
    df = df.loc[['002024.SZ', '300024.SZ', '601633.SH']]
    print(df)


if __name__ == '__main__':
    show_my_stock()
    r = select_stocks('20200402')
    print(r)
