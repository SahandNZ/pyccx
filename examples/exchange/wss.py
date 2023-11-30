import argparse
import json
import sys

from pyccx.interface.exchange import Exchange
from pyccx.model.candle import Candle


def on_message(candle: Candle):
    print(candle.datetime, candle.close)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=60)
    parser.add_argument('--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)

    exchange = Exchange.from_dict(config_data['pyccx'])
    exchange.future.market.subscribe_candles(symbol='BTC-USDT', time_frame=args.time_frame, on_message=on_message)
    exchange.future.market.subscribe_candles(symbol='ETH-USDT', time_frame=args.time_frame, on_message=on_message)
    exchange.future.market.join_wss()


if __name__ == '__main__':
    sys.path.append('../..')
    main()