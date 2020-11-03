import datetime

year = 2020
date_start = str(year) + '-03-01'
date_end = str(year) + '-04-05'

stock_pool = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']

def to_date(afulldate):
    return datetime.datetime.strptime(afulldate, '%Y-%m-%d')

def to_d(ashortdate):
    return datetime.datetime.strptime(ashortdate, '%Y%m%d')

def format_d(adate):
    return adate.strftime('%Y%m%d')

def format_date(adate):
    return adate.strftime('%Y-%m-%d')

def date2d(str):
    return format_d(to_date(str))

def d2date(str):
    return format_date(to_d(str))

def count_F1(a, b):
    f1 = 0
    if a + b == 0:
        f1 = 0
    else:
        f1 = (2 * a * b)/(a + b)

    return f1
