import requests
import pandas as pd
import sys
from requests import HTTPError

class CoingeckoAPI(object):
    def __init__(self, dump_url, f=None, wanted={'binance', 'binance_us', 'bitfinex', 'kraken', 'bitstamp', 'gdax', 'bitflyer', 'gemini', 'itbit', 'bittrex', 'poloniex', 'okex', 'huobi'}):
        if f:
            self.stdout = f
        else:
            self.stdout = sys.stdout
        self.BASE = 'https://api.coingecko.com/api/v3'
        self.wanted = self.check_exchanges(wanted)
        self.dump_url = dump_url

    def _print(self, statement):
        if self.stdout.closed:
            self.stdout = sys.stdout
        print(statement, file=self.stdout)

    def _collect(self, exchange, days=365):
        exchange = exchange.lower()
        ENDPOINT = '/exchanges/' + exchange + '/volume_chart'
        try:
            response = requests.get(self.BASE + ENDPOINT, params={'days':days})
            if response.status_code == 200:
                self._print('Collected ' + exchange)
                return response.json()
            else:
                self._print('Missed Collection of ' + exchange)
        except HTTPError as e:
            self._print('Missed ' + exchange)
            self._print('Error: ' + e)
    
    def _transform(self, data):
        df = pd.DataFrame(data, columns=['time', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df.set_index('time').resample('D').sum()
        df['volume'] = df['volume'].astype(float)
        return df

    def _collects(self, save=True, days=365):
        from time import sleep
        temp = pd.DataFrame(columns=['exchange', 'time', 'volume'])
        for exchange in self.wanted:
            sleep(2)
            data = self._collect(exchange, days)
            df = self._transform(data)
            if save:
                try:
                    if self.dump_url[-1] == '/':
                        url = self.dump_url
                    else:
                        url = self.dump_url + '/'
                    df.to_csv(url + exchange + '.csv', index=False)
                    self._print('Saved ' + exchange)
                except Exception as e:
                    self._print('Missed in `_collects`: ' + exchange)
                    self._print(str(e))
            else:
                df['exchange'] = exchange
                temp = pd.concat((temp, df), ignore_index=True, sort=False)
            time = df['time'].diff().mean()
            days = time.seconds*df.shape[0]/86400
            self._print(' -- Stats: ')
            self._print('    Average Time Delta ' + str(time) + f' - ({days} days)')
            self._print('    Shape ' + str(df.shape))
            self._print('    Mean Volume ' + str(df['volume'].mean()))
        if not save:
            return temp

    def check_exchanges(self, wanted):
        ENDPOINT = '/exchanges'
        wanted = {item.lower() for item in wanted}
        try:
            response = requests.get(self.BASE + ENDPOINT)
            exchanges = {item['id'] for item in response.json()}
            self._print('Not Available: ' + str(wanted.difference(exchanges)))
            self._print('Contains: ' + str(wanted.intersection(exchanges)))
            return wanted.intersection(exchanges)
        except HTTPError as e:
            self._print('Error: ' + str(e))
            raise e

    def run(self, save=True):
        if save:
            self._collects(save)
        else:
            return self._collects(save)



    