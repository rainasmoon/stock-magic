import Model_Evaluate as ev
import Filter
import Portfolio as pf
import Cap_Update_daily as cap_update
import DBUtils
import TSUtils
import Utils
import PltUtils

import datetime

if __name__ == '__main__':

    DBUtils.clear_db()
    DBUtils.init_stock_pool()

    date_seq_start = Utils.date_start
    date_seq_end = Utils.date_end
 
    # 建回测时间序列
    back_test_date_start = (datetime.datetime.strptime(date_seq_start, '%Y-%m-%d')).strftime('%Y%m%d')
    back_test_date_end = (datetime.datetime.strptime(date_seq_end, "%Y-%m-%d")).strftime('%Y%m%d')
    date_temp = TSUtils.get_stock_canlender(back_test_date_start, back_test_date_end)
    date_seq = [(datetime.datetime.strptime(x, "%Y%m%d")).strftime('%Y-%m-%d') for x in date_temp]
    print(date_seq)

    #开始模拟交易
    index = 1
    day_index = 0
    for i in range(1,len(date_seq)):
        day_index += 1
        # 每日推进式建模，并获取对下一个交易日的预测结果
        for stock in Utils.stock_pool:
            try:
                ans2 = ev.model_eva(stock,date_seq[i],90,365)
                # print('Date : ' + str(date_seq[i]) + ' Update : ' + str(stock))
            except Exception as ex:
                print('ERROR:' + ex)
                continue
        # 每5个交易日更新一次配仓比例
        if divmod(day_index+4,5)[1] == 0:
            portfolio_pool = Utils.stock_pool
            if len(portfolio_pool) < 5:
                print('Less than 5 stocks for portfolio!! state_dt : ' + str(date_seq[i]))
                continue
            pf_src = pf.get_portfolio(portfolio_pool, date_seq[i-1], Utils.year)
            # 取最佳收益方向的资产组合
            risk = pf_src[1][0]
            weight = pf_src[1][1]
            Filter.filter_main(portfolio_pool,date_seq[i],date_seq[i-1],weight)
        else:
            Filter.filter_main([],date_seq[i],date_seq[i - 1], [])
            cap_update_ans = cap_update.cap_update_daily(date_seq[i])
        print('Runnig to Date :  ' + str(date_seq[i]))
    print('ALL FINISHED!!')

    sharp,c_std = DBUtils.get_sharp_rate()
    print('Sharp Rate : ' + str(sharp))
    print('Risk Factor : ' + str(c_std))
    
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
