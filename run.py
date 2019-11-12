from collect import CoingeckoAPI

filepath = '~/Downloads/testing'
wanted={'binance', 
        'binance_us', 
        'bitfinex', 
        'kraken', 
        'bitstamp', 
        'gdax', 
        'bitflyer', 
        'gemini', 
        'itbit', 
        'bittrex', 
        'poloniex', 
        'okex', 
        'huobi', 'TEST'}

with open('test3.txt', 'a') as f:
    cg = CoingeckoAPI(filepath, f=f, wanted=wanted)
    cg.run()

'''
Testing:
Data seems only available back to Sept. 9th or 22nd 2019 most times
Binance_US drops to 2 volume at Sept. 23 2019
Short dates: Binance, 
             Bitfinex, 
             Binance, 
             bitstamp, 
             bittrex, 
             gdax (22nd), 
             gemini (28th), 
             huobi (27th), 
             itbit, 
             okex, 
             poloniex
Long Dates: Bitflyer 11-12-2018 to present, 
            Kraken 11-13-2018
'''