import Model_Evaluate as ev
import Filter
import Portfolio as pf
import Cap_Update_daily as cap_update
import DBUtils
import TSUtils
import Utils
import PltUtils

import datetime

def update_ratio(aday, pre_day):
    portfolio_pool = Utils.stock_pool
    if len(portfolio_pool) < 5:
        print('Less than 5 stocks for portfolio!! state_dt : ' + str(aday))
    pf_src = pf.get_portfolio(portfolio_pool, pre_day, Utils.year)
    # 取最佳收益方向的资产组合
    risk = pf_src[1][0]
    weight = pf_src[1][1]
    Filter.filter_main(portfolio_pool, aday, pre_day, weight)

def update_only(aday, pre_day):
    Filter.filter_main([], aday, pre_day, [])
    cap_update_ans = cap_update.cap_update_daily(aday)


def daily_trade(trade_date):
    for stock in Utils.stock_pool:
        try:
            ans2 = ev.model_eva(stock, trade_date, 90, 365)
        except Exception as ex:
            print('ERROR:', ex)
            
def show_pic(date_seq_start, date_seq_end):

    done_set_show_btc = DBUtils.select_index(date_seq_start, date_seq_end)
    btc_x = list(range(len(done_set_show_btc)))
    btc_y = [x[3] / done_set_show_btc[0][3] for x in done_set_show_btc]
    dict_anti_x = {}
    dict_x = {}
    for a in range(len(btc_x)):
        dict_anti_x[btc_x[a]] = done_set_show_btc[a][0]
        dict_x[done_set_show_btc[a][0]] = btc_x[a]

    done_set_show_profit = DBUtils.select_profit()
    profit_x = [dict_x[x[1]] for x in done_set_show_profit]
    profit_y = [x[0] / done_set_show_profit[0][0] for x in done_set_show_profit]
    # 绘制收益率曲线（含大盘基准收益曲线）

    PltUtils.show_pic(btc_x, btc_y, profit_x, profit_y, dict_anti_x)

def trade(date_seq_start, date_seq_end):

    DBUtils.clear_db()
    DBUtils.init_stock_pool()

    # 建回测时间序列
    date_temp = TSUtils.get_stock_canlender(date_seq_start, date_seq_end)
    date_seq = [(Utils.d2date(x)) for x in date_temp]

    #开始模拟交易
    index = 1
    day_index = 0
    print('begin trade...')
    for i in range(1,len(date_seq)):
        print('To Date:' + date_seq[i])
        day_index += 1
        # 每日推进式建模，并获取对下一个交易日的预测结果
        daily_trade(date_seq[i])
        if divmod(day_index+4,5)[1] == 0:
            print('update ratio...')
            update_ratio(date_seq[i], date_seq[i-1])
        else:
            update_only(date_seq[i], date_seq[i-1])

    print('ALL FINISHED!!')

    sharp,c_std = Utils.get_sharp_rate(DBUtils.select_my_capital())
    print('Sharp Rate : ' + str(sharp))
    print('Risk Factor : ' + str(c_std))
    

if __name__ == '__main__':

    date_seq_start = Utils.date_start
    date_seq_end = Utils.date_end

    show_pic(date_seq_start, date_seq_end)
 
