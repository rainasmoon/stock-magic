import datetime

year = 2020
date_start = str(year) + '-03-01'
date_end = str(year) + '-04-01'

stock_pool = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']

def to_date(adate):
    return datetime.datetime.strptime(adate, '%Y-%m-%d')

def to_d(afulldate):
    return datetime.datetime.strptime(adate, '%Y%m%d')

def count_F1(a, b):
    f1 = 0
    if a + b == 0:
        f1 = 0
    else:
        f1 = (2 * a * b)/(a + b)

    return f1
