# -*- coding: utf-8 -*-
import env
import daily
import stock
import utils.common_utils as utils

def aday():
    print('hi...')
    print('-------------------------------------------------------')
    print('大盘环境：')
    env.summury_env()
    print('-------------------------------------------------------')
    print('盘面：')
    daily.say_today(utils.yesterday())
    print('-------------------------------------------------------')
    print('我的：')
    df = stock.my_stocks()
    print(df)

if __name__ == '__main__':
    aday()

