import requests
import pandas as pd
import datetime
from requests import HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class CoingeckoAPI(object):
    def __init__(self, dump_url, f=None, wanted={'binance', 'binance_us', 'bitfinex', 'kraken', 'bitstamp', 'gdax', 'bitflyer', 'gemini', 'itbit', 'bittrex', 'poloniex', 'okex', 'huobi'}):
        if f:
            self.f = f
        else:
            now = datetime.datetime.now().date()
            self.f = open(f'{now}_status.txt', 'w')
        self.BASE = 'https://api.coingecko.com/api/v3'
        self.dump_url = dump_url
        self.request_timeout = 120
        self._spawnsession()
        self._ping()
        self.wanted, _ = self.check_exchanges(wanted)

    def _spawnsession(self):
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[ 502, 503, 504 ])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _print(self, statement):
        if self.f.closed:
            print(statement)
        print(statement, file=self.f)

    def _collect(self, exchange, days):
        exchange = exchange.lower()
        ENDPOINT = '/exchanges/' + exchange + '/volume_chart'
        response = self.session.get(self.BASE + ENDPOINT, params={'days':days})
        response.raise_for_status()
        data = response.json()
        print(' len data ' + str(len(data)))
        self._print('Collected ' + exchange)
        return data
    
    def _transform(self, data):
        df = pd.DataFrame(data, columns=['time', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['volume'] = df['volume'].astype(float)
        df = df.set_index('time').resample('D').last().reset_index()
        return df

    def _ping(self):
        response = self.session.get(self.BASE + '/ping')
        response.raise_for_status()
        if response.status_code == 200:
            self._print('Server Awake.')

    def _stats(self, df):
        time = df['time'].diff().mean()
        days = time.days*df.shape[0]
        self._print(' -- Stats: ')
        self._print('    Average Time Delta ' + str(time) + f' - ({days} days)')
        self._print('    Shape ' + str(df.shape))
        self._print('    Mean Volume ' + str(df['volume'].mean()))

    def _collects(self, save, days):
        temp = pd.DataFrame(columns=['exchange', 'time', 'volume'])
        exchanges = sorted(list(self.wanted))
        for exchange in exchanges:
            data = self._collect(exchange, days)
            df = self._transform(data)
            if df.empty:
                raise ValueError('No Data from response!')
            if save:
                if self.dump_url[-1] == '/':
                    url = self.dump_url
                else:
                    url = self.dump_url + '/'
                df.to_csv(url + exchange + '.csv', index=False)
                self._print('Saved ' + exchange)
            else:
                df['exchange'] = exchange
                temp = pd.concat((temp, df), ignore_index=True, sort=False)
                self._stats(df)
        if not save:
            return temp

    def check_exchanges(self, wanted, available=False, details=False):
        ENDPOINT = '/exchanges/list'
        if not available:
            wanted = {item.lower() for item in wanted}
        try:
            response = self.session.get(self.BASE + ENDPOINT)
            response.raise_for_status()
            if details:
                return response.json()
            exchanges = {item['id'] for item in response.json()}
            if available:
                return exchanges
            self._print('Not Available: ' + str(wanted.difference(exchanges)))
            self._print('Contains: ' + str(wanted.intersection(exchanges)))
            return wanted.intersection(exchanges), wanted.difference(exchanges)
        except HTTPError as e:
            self._print('Error: ' + str(e))
            raise e

    def run(self, save=True, days=5):
        if save:
            self._collects(save, days)
        else:
            return self._collects(save, days)



    