import Deal
import DBUtils

def buy(stock_code,opdate,buy_money):
    deal_buy = Deal.Deal(opdate)
    
    #后买入
    if deal_buy.cur_money_rest+1 >= buy_money:
        
        done_set_buy = DBUtils.select_stock_info(opdate, stock_code)
        if len(done_set_buy) == 0:
            return -1
        
        buy_price = float(done_set_buy[0][3])
        
        if buy_price >= 195:
            return 0
        
        vol, rest = divmod(min(deal_buy.cur_money_rest, buy_money), buy_price * 100)
        vol = vol * 100
        
        if vol == 0:
            return 0
        
        new_capital = deal_buy.cur_capital - vol * buy_price * 0.0005
        new_money_lock = deal_buy.cur_money_lock + vol * buy_price
        new_money_rest = deal_buy.cur_money_rest - vol * buy_price * 1.0005
        
        DBUtils.insert_my_capital(new_capital, new_money_lock,new_money_rest,
                                  'buy', stock_code, vol, 0.0, 0.0, 'init', opdate, buy_price) 
        if stock_code in deal_buy.stock_all:
            new_buy_price = (deal_buy.stock_map1[stock_code] * deal_buy.stock_map2[stock_code] + vol * buy_price) / (deal_buy.stock_map2[stock_code] + vol)
            new_vol = deal_buy.stock_map2[stock_code] + vol
            DBUtils.update_my_stock_poll(stock_code, new_buy_price, new_vol)
        else:
            DBUtils.insert_my_stock_poll(stock_code, buy_price, vol)

        return 1
    return 0

def sell(stock_code,opdate,predict):

    deal = Deal.Deal(opdate)
    init_price = deal.stock_map1[stock_code]
    hold_vol = deal.stock_map2[stock_code]
    hold_days = deal.stock_map3[stock_code]
    
    done_set_sell_select = DBUtils.select_stock_info(opdate, stock_code)
    
    if len(done_set_sell_select) == 0:
        return -1
    
    sell_price = float(done_set_sell_select[0][3])

    if sell_price > init_price*1.03 and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price*hold_vol
        new_money_rest = deal.cur_money_rest + sell_price*hold_vol
        new_capital = deal.cur_capital + (sell_price-init_price)*hold_vol
        new_profit = (sell_price-init_price)*hold_vol
        new_profit_rate = sell_price/init_price
    
        DBUtils.insert_my_capital(new_capital,new_money_lock,new_money_rest,'SELL',stock_code,hold_vol,new_profit,new_profit_rate,'GOODSELL',opdate,sell_price)
        DBUtils.delete_my_stock_poll(stock_code)

        return 1

    elif sell_price < init_price*0.97 and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price*hold_vol
        new_money_rest = deal.cur_money_rest + sell_price*hold_vol
        new_capital = deal.cur_capital + (sell_price-init_price)*hold_vol
        new_profit = (sell_price-init_price)*hold_vol
        new_profit_rate = sell_price/init_price

        DBUtils.insert_my_capital(new_capital,new_money_lock,new_money_rest,'SELL',stock_code,hold_vol,new_profit,new_profit_rate,'BADSELL',opdate,sell_price)
        DBUtils.delete_my_stock_poll(stock_code)
        
        return 1

    elif hold_days >= 4 and hold_vol > 0:
        new_money_lock = deal.cur_money_lock - sell_price * hold_vol
        new_money_rest = deal.cur_money_rest + sell_price * hold_vol
        new_capital = deal.cur_capital + (sell_price - init_price) * hold_vol
        new_profit = (sell_price - init_price) * hold_vol
        new_profit_rate = sell_price / init_price
        
        DBUtils.insert_my_capital(new_capital, new_money_lock, new_money_rest, 'OVERTIME', stock_code, hold_vol, new_profit, new_profit_rate,'OVERTIMESELL', opdate,sell_price)
        DBUtils.delete_my_stock_poll(stock_code)

        return 1

    elif predict == -1:
        new_money_lock = deal.cur_money_lock - sell_price * hold_vol
        new_money_rest = deal.cur_money_rest + sell_price * hold_vol
        new_capital = deal.cur_capital + (sell_price - init_price) * hold_vol
        new_profit = (sell_price - init_price) * hold_vol
        new_profit_rate = sell_price / init_price
        
        DBUtils.insert_my_capital( new_capital, new_money_lock, new_money_rest, 'Predict', stock_code, hold_vol, new_profit, new_profit_rate, 'PredictSell', opdate, sell_price)
        DBUtils.delete_my_stock_poll(stock_code)
        return 1
    
    return 0

