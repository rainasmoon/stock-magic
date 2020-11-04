import Deal
import Operator
import DBUtils

def filter_main(stock_new,state_dt,predict_dt,poz):

    #先更新持股天数
    DBUtils.update_hold_days()

    #先卖出
    deal = Deal.Deal(state_dt)
    stock_pool_local = deal.stock_pool
    for stock in stock_pool_local:
        
        predict = DBUtils.get_stock_predict(state_dt, stock)
        ans = Operator.sell(stock,state_dt,predict)

    #后买入
    for stock_index in range(len(stock_new)):
        deal_buy = Deal.Deal(state_dt)

        # # 如果模型f1分值低于50则不买入
        # sql_f1_check = "select * from model_ev_resu a where a.stock_code = '%s' and a.state_dt < '%s' order by a.state_dt desc limit 1"%(stock_new[stock_index],state_dt)
        # cursor.execute(sql_f1_check)
        # done_check = cursor.fetchall()
        # db.commit()
        # if len(done_check) > 0:
        #     if float(done_check[0][4]) < 0.5:
        #         print('F1 Warning !!')
        #         continue


        ans = Operator.buy(stock_new[stock_index],state_dt,poz[stock_index]*deal_buy.cur_money_rest)
        del deal_buy
    
