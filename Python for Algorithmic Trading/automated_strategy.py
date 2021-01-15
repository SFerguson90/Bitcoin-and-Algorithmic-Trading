#
# Automated ML-Based Trading Strategy for Oanda
# Online Algorithm, Logging, Monitoring
#

from dotenv import load_dotenv
import zmq
from tpqoa import tpqoa2
import pickle
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date

today = date.today()
log_file = f'automated_strategy {today}.log'

# loads the persisted algorithm object
algorithm = pickle.load(open('algorithm.pkl', 'rb'))

# sets up the socket communication via ZeroMQ (here: "publisher")
context = zmq.Context()
socket = context.socket(zmq.PUB)

# this binds the socket communication to all IP addresses of the machine
socket.bind('tcp://127.0.0.1:5555')

# recreating the log file
with open(log_file, 'w') as f:
    f.write('*** NEW LOG FILE ***\n')
    f.write(str(dt.datetime.now()) + '\n\n\n')


def logger_monitor(message, time=True, sep=True):

    '''
    Custom logger and monitor function.
    '''

    with open(log_file, 'a') as f:
        t = str(dt.datetime.now())
        msg = ''
        if time:
            msg += '\n' + t + '\n'
        if sep:
            msg += 80 * '=' + '\n'
        msg += message + '\n\n'
        # sends the message via the socket
        socket.send_string(msg)
        # writes the message to the log file
        f.write(msg)


class MLTrader(tpqoa2.tpqoa2):
    def __init__(self, algorithm, conf_file=None, env_file=None):
        super(MLTrader, self).__init__(conf_file, env_file)
        self.model = algorithm['model']
        self.mu = algorithm['mu']
        self.std = algorithm['std']
        self.units = 100000
        self.position = 0
        self.bar = '15M'
        self.window = 2
        self.lags = 32 #Must be inline with algorithm
        self.min_length = self.lags + self.window + 1
        self.features = ['return', 'vol', 'mom', 'sma', 'ema', 'min', 'max']
        self.raw_data = pd.DataFrame()

    def prepare_features(self):
        self.data['return'] = np.log(
            self.data['mid'] / self.data['mid'].shift(1))
        self.data['vol'] = self.data['return'].rolling(self.window).std()
        self.data['mom'] = np.sign(
            self.data['return'].rolling(self.window).mean())
        self.data['sma'] = self.data['mid'].rolling(self.window).mean()
        self.data['ema'] = self.data['mid'].ewm(span=self.window).mean()
        self.data['min'] = self.data['mid'].rolling(self.window).min()
        self.data['max'] = self.data['mid'].rolling(self.window).max()
        self.data.dropna(how='any',inplace=True)
        self.data[self.features] -= self.mu
        self.data[self.features] /= self.std
        self.cols = []
        for f in self.features:
            for lag in range(1, self.lags + 1):
                col = f'{f}_lag_{lag}'
                self.data[col] = self.data[f].shift(lag)
                self.cols.append(col)

    def report_trade(self, pos, order):
        
        '''
        Prints, logs and sends trade data.
        '''

        out = '\n\n' + 80 * '=' + '\n'
        out += '*** GOING {} *** \n'.format(pos) + '\n'
        out += str(order) + '\n'
        out += 80 * '=' + '\n'
        logger_monitor(out)
        print(out)

    def on_success(self, time, bid, ask):
        print(self.ticks, 20 * ' ', end='\r')
        df = pd.DataFrame({'bid': float(bid), 'ask': float(ask)},
                          index=[pd.Timestamp(time).tz_localize(None)])
        self.raw_data = self.raw_data.append(df)
        self.data = self.raw_data.resample(
            self.bar, label='right').last().ffill()
        self.data = self.data.iloc[:-1]
        if len(self.data) > self.min_length:
            logger_monitor('NUMBER OF TICKS: {} | '.format(self.ticks) +
                           'NUMBER OF BARS: {}'.format(self.min_length))
            self.min_length += 1
            self.data['mid'] = (self.data['bid'] + self.data['ask']) / 2
            self.prepare_features()
            features = self.data[self.cols].iloc[-1].values.reshape(1, -1)
            signal = self.model.predict(features)[0]
            #print(self.model.predict(features))
            # logs and sends major financial information
            logger_monitor('MOST RECENT DATA\n' +
                           str(self.data[self.cols].tail()),
                           False)
            logger_monitor('features:\n' + str(features) + '\n' +
                           'position: ' + str(self.position) + '\n' +
                           'signal:   ' + str(signal), False)
            if self.position in [0, -1] and signal == 1:  # going long?
                order = self.create_order(self.stream_instrument,
                                          units=(1 - self.position) *
                                          self.units,
                                          suppress=True, ret=True)
                self.report_trade('LONG', order)
                self.position = 1
            elif self.position in [0, 1] and signal == -1:  # going short?
                order = self.create_order(self.stream_instrument,
                                          units=-(1 + self.position) *
                                          self.units,
                                          suppress=True, ret=True)
                self.report_trade('SHORT', order)
                self.position = -1
            else:  # no trade
                logger_monitor('*** NO TRADE PLACED ***')

            logger_monitor('*** END OF CYCLE ***\n\n', False, False)


if __name__ == '__main__':
    mlt = MLTrader(algorithm, env_file='../.env')
    mlt.stream_data('EUR_USD')
    order = mlt.create_order(mlt.stream_instrument,
                             units=-mlt.position * mlt.units,
                             suppress=True, ret=True)
    mlt.position = 0
    mlt.report_trade('NEUTRAL', order)
