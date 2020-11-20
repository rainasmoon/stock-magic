## encoding: utf-8
import utils.ts_utils as ts_utils
import utils.ts_pro as ts_pro
import utils.utils as utils

import matplotlib.pyplot as plt
import pandas as pd

from pylab import mpl
import seaborn as sns

# 正常显示画图时出现的中文
# 这里使用微软雅黑字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 画图时显示负号
mpl.rcParams['axes.unicode_minus'] = False

PATH = './datas/pic/'

def draw_pic(aday):
    print('RUN on day:' + aday)
    df = ts_pro.call_daily(aday)

    prices = df['close']
    prices = prices.sort_values(ascending = True)
    prices = prices.reset_index(drop=True)
    fig = plt.figure()
    prices.plot()
    plt.title('今日收盘排序价分布')
    plt.grid(True)
    plt.savefig(PATH + 'close_prices_test'+aday+'.png', bbox_inches='tight')
    plt.close()

    plt.figure()
    prices.hist(bins=100)
    plt.title('收盘价价格分布 ')
    plt.savefig(PATH + 'close_prices'+aday+'.png', bbox_inches='tight')

    plt.close()

    price_l = df[df['close'] <= 50]['close']
    price_l = price_l.sort_values(ascending = True)
    price_l = price_l.reset_index(drop=True)
    plt.figure()
    price_l.plot()
    plt.title('<= 50 stocks')
    plt.savefig(PATH + 'class1_stocks'+aday+'.png', bbox_inches='tight')
    plt.close()

    price_h = df[(df['close'] > 50) & (df['close'] <= 400)]['close']
    price_h = price_h.sort_values(ascending = True)
    price_h = price_h.reset_index(drop = True)
    plt.figure()
    if not price_h.empty:
        price_h.plot()
    plt.title('50-400 stocks')
    plt.savefig(PATH + 'class2_stocks'+aday+'.png', bbox_inches='tight')
    plt.close()

    price_50 = df[df['close'] > 50]
    print('the number over 50 is:' + str(len(price_50)))

    price_100 = df[df['close'] > 100]
    print('the number over 100 is:' + str(len(price_100)))

    price_exception = df[df['close'] > 400]
    print('the number over 400 is:' + str(len(price_exception)))

    p_up = df[df['pct_chg'] > 9]

    print('up is:' + str(len(p_up)))

    p_down = df[df['pct_chg'] < -9 ]
    print('down is:' + str(len(p_down)))

    p_ratio = df['pct_chg']

    plt.figure()
    p_ratio.hist(bins=40)
    plt.title('回报率分布')
    plt.savefig(PATH + 'return_ratio_1'+aday+'.png', bbox_inches='tight')
    plt.close()

    plt.figure()
    sns.kdeplot(p_ratio)
    plt.title('回报率')
    plt.savefig(PATH + 'return_ratio_0'+aday+'.png', bbox_inches='tight')
    plt.close()

    p_ratio = p_ratio.sort_values(ascending = True)
    p_ratio = p_ratio.reset_index(drop = True)
    plt.figure()
    p_ratio.plot()
    plt.title('回报率')
    plt.savefig(PATH + 'return_ratio'+aday+'.png', bbox_inches='tight')
    plt.close()

    vols = df['vol']
    plt.figure()
    vols.hist(bins=50)
    plt.title('成交量')
    plt.savefig(PATH + 'vol'+aday+'.png', bbox_inches='tight')
    plt.close()

    amounts = df['amount']
    plt.figure()
    amounts.hist(bins=100)
    plt.title('成交额')
    plt.savefig(PATH + 'amount'+aday+'.png', bbox_inches='tight')
    plt.close()
    
if __name__ == '__main__':
    print('hello...')
    draw_pic(utils.new_trade_day())

#    for aday in days:
#        draw_pic(aday)
