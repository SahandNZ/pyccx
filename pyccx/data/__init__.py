import itertools
from typing import Dict, List, Tuple

import pandas as pd
from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local import LocalData
from pyccx.defaults import BASE_TIME_FRAME
from pyccx.interface.exchange import Exchange
from pyccx.model.candle import Candle
from pyccx.utils import resample_time_frame
from rich.progress import Progress

__EXCHANGE: Exchange = None
__LOCAL_DATA: LocalData = None


def load_dataframe(exchange: str, symbol: str, time_frame: TimeFrame, update: bool = False,
                   proxies: Dict[str, str] = None) -> pd.DataFrame:
    global __EXCHANGE
    global __LOCAL_DATA
    if __EXCHANGE is None or __EXCHANGE.exchange != exchange:
        __EXCHANGE = Exchange(exchange=exchange, proxies=proxies)
        __LOCAL_DATA = LocalData(exchange=__EXCHANGE)

    if update:
        candles = __LOCAL_DATA.download_candles(symbol=symbol, time_frame=BASE_TIME_FRAME)
        sdf = Candle.to_dataframe(candles=candles)
    else:
        sdf = __LOCAL_DATA.load_dataframe(symbol=symbol, time_frame=BASE_TIME_FRAME)

    df = resample_time_frame(tohlcv=sdf, source_timeframe=BASE_TIME_FRAME, destination_timeframe=time_frame)

    return df


def load_dataframes_dict(
        exchange: str,
        symbols: List[str],
        time_frames: List[TimeFrame],
        update: bool = False,
        proxies: Dict[str, str] = None,
        progress: Progress = None,
) -> Dict[Tuple[str, int], pd.DataFrame]:
    items = list(itertools.product(symbols, time_frames))

    if progress is not None:
        task = progress.add_task(description="Loading DataFrames", total=len(items))

    dfs_dict = {}
    for symbol, time_frame in items:
        df = load_dataframe(exchange=exchange, symbol=symbol, time_frame=time_frame, update=update, proxies=proxies)
        dfs_dict[symbol, time_frame] = df

        if progress is not None:
            progress.update(task, advance=1)

    return dfs_dict
