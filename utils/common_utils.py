# -*- coding: utf-8 -*

import datetime


def today():
    today = datetime.date.today()
    return today.strftime('%Y%m%d')


def last_tradeday():
    '''
    正确的作法是返回上一个交易日的日期
    '''
    return yesterday()


def yesterday():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return yesterday.strftime("%Y%m%d")


if __name__ == '__main__':
    print(today())
    print(yesterday())
