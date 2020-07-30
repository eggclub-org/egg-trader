#!/usr/bin/env python

"""
Author: www.backtest-rookies.com

MIT License

Copyright (c) 2018 backtest-rookies.com
"""
import time

import ccxt
import click

import ccxt_utils as utils


@click.command()
@click.argument('symbol')
@click.argument('exchange')
@click.option('--timeframe', '-t',
              default='1d',
              type=click.Choice(['1m', '5m', '15m', '30m', '1h', '2h', '3h', '4h', '6h', '12h', '1d', '1M', '1y']),
              help='The timeframe to download', show_default=True)
@click.option('--since', type=int, default=None,
              help='From timestamp (in miliseconds). Ex: 946684800000 (2000-01-01 00:00:00)')
@click.option('--limit', type=int, default=None, help='Limit records')
@click.option('--n-last-record', type=int, default=None, help='Last records')
@click.option('--debug', default=False, help='Print sizer debugs')
def ccxt_downloader(symbol, exchange, timeframe, since, limit, n_last_record, debug):
    """Download Crypto Trades Data

    - symbol: symbol to download

    - exchange: the exchange to download from
    """
    if since:
        since = utils.round_up_timeframe(timeframe, since=since)
    elif n_last_record:
        since = utils.round_up_timeframe(timeframe, n_last_record=n_last_record)

    # Get our Exchange
    try:
        exchange = getattr(ccxt, exchange)()
    except AttributeError:
        print('-' * 36, ' ERROR ', '-' * 35)
        print('Exchange "{}" not found. Please check the exchange is supported.'.format(exchange))
        print('-' * 80)
        quit()

    # Check if fetching of OHLC Data is supported
    if not exchange.has["fetchOHLCV"]:
        print('-' * 36, ' ERROR ', '-' * 35)
        print('{} does not support fetching OHLC data. Please use another exchange'.format(exchange))
        print('-' * 80)
        quit()

    # Check requested timeframe is available. If not return a helpful error.
    if (not hasattr(exchange, 'timeframes')) or (timeframe not in exchange.timeframes):
        print('-' * 36, ' ERROR ', '-' * 35)
        print('The requested timeframe ({}) is not available from {}\n'.format(timeframe, exchange))
        print('Available timeframes are:')
        for key in exchange.timeframes.keys():
            print('  - ' + key)
        print('-' * 80)
        quit()

    # Check if the symbol is available on the Exchange
    exchange.load_markets()
    if symbol not in exchange.symbols:
        print('-' * 36, ' ERROR ', '-' * 35)
        print('The requested symbol ({}) is not available from {}\n'.format(symbol, exchange))
        print('Available symbols are:')
        for key in exchange.symbols:
            print('  - ' + key)
        print('-' * 80)
        quit()

    # Get data
    data = list()

    if limit:
        now = time.time() * 1000

        total_records = 0

        while total_records < limit:

            current_data = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since)
            data.extend(current_data)
            total_records += len(current_data)

            if len(data) > 0:
                last_timestamp = data[-1][0] + 1
                since = utils.round_up_timeframe(timeframe, since=last_timestamp)
            else:
                break

            if since > now:
                break

        data = data[:limit]
    else:
        data = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since)

    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

    # Save it
    symbol_out = symbol.replace("/", "")
    filename = '{}-{}-{}.csv'.format(exchange, symbol_out, timeframe)

    # # Save with Pandas
    # import pandas as pd
    # df = pd.DataFrame(data, columns=header).set_index('Timestamp')
    # df.to_csv(filename)

    # Save with csv
    with open(filename, 'w') as f:
        f.write(','.join(header) + '\n')

        f.writelines([(','.join([str(t) for t in row]) + '\n') for row in data])


if __name__ == '__main__':
    ccxt_downloader()
