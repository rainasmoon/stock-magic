import Deal
import utils.DBUtils as  DBUtils
import utils.utils as Utils

def buy(stock_code,opdate,buy_money):
    deal_buy = Deal.Deal(opdate)
    
    #后买入
    if deal_buy.cur_money_rest+1 >= buy_money:
        
        stock2buy = DBUtils.select_stock_info(opdate, stock_code)
        if len(stock2buy) == 0:
            print('WARN: no stock to buy... -' + stock_code)
            return -1
        
        buy_price = float(stock2buy[0][3])
        
        if buy_price >= 195:
            print('INFO: price over 195... -' + stock_code)
            return 0
        
        vol, rest = divmod(min(deal_buy.cur_money_rest, buy_money), buy_price * 100)
        vol = vol * 100
        
        if vol == 0:
            print('INFO: vol is 0, money is not enough... -' + stock_code)
            return 0
        
        new_capital = deal_buy.cur_capital - vol * buy_price * 0.0005
        new_money_lock = deal_buy.cur_money_lock + vol * buy_price
        new_money_rest = deal_buy.cur_money_rest - vol * buy_price * 1.0005
        
        DBUtils.insert_my_capital(new_capital, new_money_lock,new_money_rest,
                                  'BUY', stock_code, vol, 0.0, 0.0, 'init', opdate, buy_price) 
        if stock_code in deal_buy.stock_all:
            new_buy_price = (deal_buy.stocks_buy_price[stock_code] * deal_buy.stocks_hold_vol[stock_code] + vol * buy_price) / (deal_buy.stocks_hold_vol[stock_code] + vol)
            new_vol = deal_buy.stocks_hold_vol[stock_code] + vol

            DBUtils.update_my_stock_poll(stock_code, new_buy_price, new_vol)
        else:
            DBUtils.insert_my_stock_poll(stock_code, buy_price, vol)

        return 1
    return 0

def record_sell(deal, opdate, stock_code, init_price, sell_price, hold_vol, act, desc):

        new_money_lock = deal.cur_money_lock - sell_price*hold_vol
        new_money_rest = deal.cur_money_rest + sell_price*hold_vol
        new_capital = deal.cur_capital + (sell_price-init_price)*hold_vol
        new_profit = (sell_price-init_price)*hold_vol
        new_profit_rate = sell_price/init_price
    
        DBUtils.insert_my_capital(new_capital,new_money_lock,new_money_rest,act,stock_code,hold_vol,new_profit,new_profit_rate,desc,opdate,sell_price)

        DBUtils.delete_my_stock_poll(stock_code)


def sell(stock_code, opdate, predict):

    deal = Deal.Deal(opdate)
    init_price = deal.stocks_buy_price[stock_code]
    hold_vol = deal.stocks_hold_vol[stock_code]
    hold_days = deal.stocks_hold_days[stock_code]
    
    stock_2_sell = DBUtils.select_stock_info(opdate, stock_code)
    
    if len(stock_2_sell) == 0:
        print('WARN: no stock info. wired. return. pls check')
        return -1
    
    sell_price = float(stock_2_sell[0][3])

    if sell_price > init_price*Utils.GOOD_THREADHOLD and hold_vol > 0:
        record_sell(deal, opdate, stock_code, init_price, sell_price, hold_vol, 'SELL', 'GOODSELL')
        return 1

    elif sell_price < init_price*Utils.BAD_THREADHOLD and hold_vol > 0:
        record_sell(deal, opdate, stock_code, init_price, sell_price, hold_vol, 'SELL', 'BADSELL')
        return 1

    elif hold_days >= Utils.OVER_DUE_DAYS and hold_vol > 0:
        record_sell(deal, opdate, stock_code, init_price, sell_price, hold_vol, 'OVERTIME',
                    'OVERTIMESELL')
        return 1

    elif predict == -1:
        record_sell(deal, opdate, stock_code, init_price, sell_price, hold_vol, 'Predict',
                    'PredictSell')
        return 1
    
    return 0

