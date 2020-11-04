import datetime
from pylab import np

year = 2020
date_start = str(year) + '-03-01'
date_end = str(year) + '-03-05'

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

def get_sharp_rate(done_exp):
    cap_list = [float(x[0]) for x in done_exp]
    return_list = []
    
    base_cap = float(done_exp[0][0])
    
    for i in range(len(cap_list)):
        if i == 0:
            return_list.append(float(1.00))
        else:
            ri = (float(done_exp[i][0]) - float(done_exp[0][0]))/float(done_exp[0][0])
            return_list.append(ri)
    
    std = float(np.array(return_list).std())
    
    exp_portfolio = (float(done_exp[-1][0]) - float(done_exp[0][0]))/float(done_exp[0][0])
    
    exp_norisk = 0.04*(5.0/12.0)
    
    sharp_rate = (exp_portfolio - exp_norisk)/(std)

    return sharp_rate, std
