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
