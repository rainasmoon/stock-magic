import ts_utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def Strategy(pdatas, win_long, win_short, lossratio=999):
    """
    pma：计算均线的价格序列
    win:窗宽
    lossratio：止损率,默认为0
    """

    pdatas = pdatas.copy()

    pdatas['lma'] = pdatas.close.rolling(win_long, min_periods=0).mean()
    pdatas['sma'] = pdatas.close.rolling(win_short, min_periods=0).mean()

    pdatas['position'] = 0  # 记录持仓
    pdatas['flag'] = 0  # 记录买卖

    pricein = []
    priceout = []
    price_in = 1
    for i in range(max(1, win_long), pdatas.shape[0] - 1):

        # 当前无仓位，短均线上穿长均线，做多
        if (pdatas.sma[i - 1] < pdatas.lma[i - 1]) & (pdatas.sma[i] > pdatas.lma[i]) & (pdatas.position[i] == 0):
            pdatas.loc[i, 'flag'] = 1
            pdatas.loc[i + 1, 'position'] = 1

            date_in = pdatas.trade_date[i]
            price_in = pdatas.loc[i, 'close']
            pricein.append([date_in, price_in])

        # 当前持仓，下跌超出止损率，止损
        elif (pdatas.position[i] == 1) & (pdatas.close[i] / price_in - 1 < -lossratio):
            pdatas.loc[i, 'flag'] = -1
            pdatas.loc[i + 1, 'position'] = 0

            priceout.append([pdatas.trade_date[i], pdatas.loc[i, 'close']])

        # 当前持仓，死叉，平仓
        elif (pdatas.sma[i - 1] > pdatas.lma[i - 1]) & (pdatas.sma[i] < pdatas.lma[i]) & (pdatas.position[i] == 1):
            pdatas.loc[i, 'flag'] = -1
            pdatas.loc[i + 1, 'position'] = 0

            priceout.append([pdatas.trade_date[i], pdatas.loc[i, 'close']])

        # 其他情况，保持之前仓位不变
        else:
            pdatas.loc[i + 1, 'position'] = pdatas.loc[i, 'position']

    p1 = pd.DataFrame(pricein, columns=['datebuy', 'pricebuy'])
    p2 = pd.DataFrame(priceout, columns=['datesell', 'pricesell'])

    transactions = pd.concat([p1, p2], axis=1)

    pdatas = pdatas.loc[max(0, win_long):, :].reset_index(drop=True)
    pdatas['ret'] = pdatas.close.pct_change(1).fillna(0)
    pdatas['nav'] = (1 + pdatas.ret * pdatas.position).cumprod()
    pdatas['benchmark'] = pdatas.close / pdatas.close[0]

    stats, result_peryear = performace(transactions, pdatas)

    return stats, result_peryear, transactions, pdatas


def performace(transactions, strategy):
    N = 250

    # 年化收益率
    rety = strategy.nav[strategy.shape[0] - 1] ** (N / strategy.shape[0]) - 1

    # 夏普比
    Sharp = (strategy.ret * strategy.position).mean() / (strategy.ret * strategy.position).std() * np.sqrt(N)

    # 胜率
    VictoryRatio = ((transactions.pricesell - transactions.pricebuy) > 0).mean()

    DD = 1 - strategy.nav / strategy.nav.cummax()
    MDD = max(DD)

    # 策略逐年表现

    strategy['year'] = strategy.trade_date.apply(lambda x: str(x)[:4])
    nav_peryear = strategy.nav.groupby(strategy.year).last() / strategy.nav.groupby(strategy.year).first() - 1
    benchmark_peryear = strategy.benchmark.groupby(strategy.year).last() / strategy.benchmark.groupby(
        strategy.year).first() - 1

    excess_ret = nav_peryear - benchmark_peryear
    result_peryear = pd.concat([nav_peryear, benchmark_peryear, excess_ret], axis=1)
    result_peryear.columns = ['strategy_ret', 'bench_ret', 'excess_ret']
    result_peryear = result_peryear.T

    # 作图
    xtick = np.round(np.linspace(0, strategy.shape[0] - 1, 7), 0)
    xticklabel = strategy.trade_date[xtick]

    plt.figure(figsize=(9, 4))
    ax1 = plt.axes()
    plt.plot(np.arange(strategy.shape[0]), strategy.benchmark, 'black', label='benchmark', linewidth=2)
    plt.plot(np.arange(strategy.shape[0]), strategy.nav, 'red', label='nav', linewidth=2)
    plt.plot(np.arange(strategy.shape[0]), strategy.nav / strategy.benchmark, 'orange', label='RS', linewidth=2)

    plt.legend()
    ax1.set_xticks(xtick)
    ax1.set_xticklabels(xticklabel)

    maxloss = min(transactions.pricesell / transactions.pricebuy - 1)
    print('------------------------------')
    print('夏普比为:', round(Sharp, 2))
    print('年化收益率为:{}%'.format(round(rety * 100, 2)))
    print('胜率为：{}%'.format(round(VictoryRatio * 100, 2)))
    print('最大回撤率为：{}%'.format(round(MDD * 100, 2)))
    print('单次最大亏损为:{}%'.format(round(-maxloss * 100, 2)))
    print('月均交易次数为：{}(买卖合计)'.format(round(strategy.flag.abs().sum() / strategy.shape[0] * 20, 2)))

    result = {'Sharp': Sharp,
              'RetYearly': rety,
              'WinRate': VictoryRatio,
              'MDD': MDD,
              'maxlossOnce': -maxloss,
              'num': round(strategy.flag.abs().sum() / strategy.shape[0], 1)}

    result = pd.DataFrame.from_dict(result, orient='index').T
    print('result:\n', result)
    print('result_peryear\n', result_peryear)
    return result, result_peryear


def test():
    stock_code = '000001.SZ'
    ipo_date = '20190101'
    aday = '20191001'
    df = ts_utils.call_stock_qfq_raw(stock_code, ipo_date, aday)
    df = df.sort_values(by='trade_date')
    df = df.reset_index(drop=True)
    r = Strategy(pdatas=df, win_long=89, win_short=21, lossratio=999)


if __name__ == '__main__':
    test()
