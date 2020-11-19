#-*- coding: utf-8 -*-

import utils.ts_utils as ts_utils
import utils.ts_pro as ts_pro
import utils.utils as utils
import utils.plt_utils as plt_utils

'''
上证指数
上证成份股
上证指数处在各区间的概率：
先计算分数，
再计算分类：60分以下，80分以上。不及格，及格，优秀，卓越
个股是否在成份股里。

'''

def summury_env(aday):
    today_indexs = ts_utils.call_today_indexs()
    today_sh_index = today_indexs.loc['000001', 'close']
    today_sh_vol = today_indexs.loc['000001', 'volume']

    print('当前上证指数：%d'%(today_sh_index))
    print('current vol: %d'%(today_sh_vol))

    sh_index_history = ts_utils.call_sh_index()

    sh_index_history = sh_index_history.loc[utils.day0:]
    print('BASE day0: ' + utils.day0)

    plt_utils.show_k(sh_index_history, '上证指数')

    describe = sh_index_history.describe()

    index_high = describe.loc['max', 'high']
    index_low = describe.loc['min', 'low']
    
    vol_max = describe.loc['max', 'volume']
    vol_min = describe.loc['min', 'volume']

    today_index_position = (today_sh_index - index_low) / (index_high - index_low)
    today_vol_position = (today_sh_vol - vol_min) / (vol_max - vol_min)

    print('now index pos: %.2f;  vol pos: %.2f'%(today_index_position,
                                                 today_vol_position))
    
    gr_days = len(sh_index_history[sh_index_history['close'] > today_sh_index])
    print('higher days than now: %d'%(gr_days))
    higher_posibility = gr_days/len(sh_index_history)
    print('higher posibility: %0.2f'%(higher_posibility))

    gr_vol_days = len(sh_index_history[sh_index_history['volume'] > today_sh_vol])
    print('higher vol days than now: %d'%(gr_vol_days))
    gr_vol_posibility = gr_vol_days/len(sh_index_history)
    print('higher vol posibility: %0.2f'%(gr_vol_posibility))

if __name__ == '__main__':
    r = summury_env('20201118')
    print(r)
