#-*- coding: utf-8 -*-

import ts_utils
import matplotlib.pyplot as plt
import pandas as pd

'''
上证指数
上证成份股
上证指数处在各区间的概率：
先计算分数，
再计算分类：60分以下，80分以上。不及格，及格，优秀，卓越
个股是否在成份股里。

'''


def summury_env(aday):
    y_roi = ts_utils.call_deposit_rate_v1()
    df_sh_index = ts_utils.call_index_v1()
    sh_index = round(df_sh_index.loc['000001', 'close'])
    sh_vol = df_sh_index.loc['000001', 'volume']
    cpi = ts_utils.call_cpi()
    m = ts_utils.call_money_supply()
    df = ts_utils.call_sh_index_v1()
    df = df.describe().round(2)
    low = df.loc['min', 'low']
    high = df.loc['max', 'high']
    vol_max = df.loc['max', 'volume']
    vol_min = df.loc['min', 'volume']
    index_position = round((sh_index - low) / (high - low) * 100, 2)
    sh_vol_position = round((sh_vol - vol_min) / (vol_max - vol_min) * 100, 2)
    rint(f'一年存款利率：{y_roi},\n 上证指数：{sh_index},\n 位置：{index_position}%,\n 成交量：{sh_vol},\n 位置：{sh_vol_position}%,\n CPI: {cpi},\n M: {m}\n')
    return [y_roi]

def show_index_position():
    '''
    统计上证指数的所有所在点位的天数。计算这一点数出现的概率
    :return:
    '''
    df = ts_utils.call_sh_index_v1()
    df['crazy_pos'] = df['close'].apply(posibility_day, args=(df,))
    all_num = len(df)
    df['crazy_pos'] = round(df['crazy_pos']/all_num, 2)
    # 以0.48 为基准重新计算概率
    df['crazy_pos'] = round(df['crazy_pos']/0.27,2)*100
    df['crazy_vol'] = df['volume'].apply(posibility_vol, args=(df,))
    df['crazy_vol'] = round(df['crazy_vol']/all_num, 2)*100

    print('pos & trust')
    final_df = pd.DataFrame()
    final_df['close'] = df['close']
    final_df['vol'] = df['volume']
    final_df['pos'] = df['crazy_pos']
    final_df['trust'] = df['crazy_vol']
    print(final_df.tail())
    print('HISTORY must be remembered.')
    print(final_df.loc[pd.to_datetime(['19940728', '20050606', '20081028', '20130625', '20160127']),:])

def posibility_vol(index, df):
    great_df = df[df.volume > index]
    return len(great_df)

def posibility_day(index, df):
    great_df = df[df.close > index]
    return len(great_df)

if __name__ == '__main__':
    show_index_position()
