# -*- coding: utf-8 -*
from pylab import mpl

import matplotlib.pyplot as plt

# 正常显示画图时出现的中文
# 这里使用微软雅黑字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 画图时显示负号
mpl.rcParams['axes.unicode_minus'] = False


def show_k(df, stock_info):
    stock_close = df['close']
    stock_close.plot()
    plt.title('STOCK' + stock_info)
    plt.xlabel('日期')
    plt.show()


def show_vol(df, stock_info):
    stock_vol = df['vol']
    stock_vol.plot()
    plt.title('成交量' + stock_info)
    plt.show()

    
def show_ma(df, stock_info):
    df = df.sort_values('trade_date', ascending=True)

    ma_day = [21, 89, 333]
    for ma in ma_day:
        column_name = f'{ma}日均线'
        df[column_name] = df["close"].rolling(ma).mean()
    # 画出2010年以来收盘价和均线图
    df[["close", "21日均线", "89日均线", "333日均线"]].plot()
    plt.title('均线' + stock_info)
    plt.xlabel('日期')
    plt.show()


def show_mon_k_v1(df, stock_info):
    stock_month = df['close']
    stock_month.plot()
    plt.title('月线' + stock_info)
    plt.xlabel('日期')
    plt.show()
