from collect import CoingeckoAPI
import pandas as pd
cg_exchange_ids = set(pd.read_csv('exchange_list.csv', index_col=0)['id'].values)

f = open('status.txt', 'a')

filepath = 'testing'
filepath_futures = 'testing_futures'
wanted = {
    'binance', 
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
    'huobi'
}

wanted_futures = {
    'bitmex',
    'bitfinex_futures',
    'bitflyer_futures',
    'deribit',
    'binance_futures',
    'cme_futures',
    'kraken_futures',
    'okex_swap'
}

# --- Note ---
# Save=False, f=None is CLI Printing DF Generation
# Save=True, f=None is CLI Printing File Generation
# Save=False, f=FileObj is Headless DF Generation
# Save=True, f-FileObj is Headless File Generation
f.write('\n\n ----- TEST ----- \n\n')
cg = CoingeckoAPI(filepath, wanted=wanted, f=f)
_, w = cg.check_exchanges(wanted)
_, wf = cg.check_exchanges(wanted)
if not w and not wf:
    f.write('All markets available.')
else:
    f.write('Missing spot ' + str(w) + ' futures ' + str(wf))
f.write('\n\n ----- SPOT ----- \n\n')
cg = CoingeckoAPI(filepath, wanted=wanted, f=f)
cg.run(save=True, days=7000)
f.write('\n\n ----- FUTURES ----- \n\n')
cg = CoingeckoAPI(filepath_futures, wanted=wanted_futures, f=f)
cg.run(save=True, days=7000)
f.close()


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