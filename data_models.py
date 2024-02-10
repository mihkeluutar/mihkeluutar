import pandas as pd


def empty_ticker_dataframe():
    df = pd.DataFrame({
        'symbol': pd.Series([], dtype='str'),
        'name': pd.Series([], dtype='str'),
        'market_cap': pd.Series([], dtype='float'),
        'volume': pd.Series([], dtype='float'),
        'exchange': pd.Series([], dtype='str')
    })
    df.set_index('symbol', inplace=True)

    return df


# TODO: Every stock should have a rsi_gain_last5_days field as well, so we can see it right away
def empty_daily_quote_dataframe():
    daily_quote_df = pd.DataFrame({
        'symbol': pd.Series([], dtype='str'),
        'date': pd.Series([], dtype='datetime64[ns]'),
        'open': pd.Series([], dtype='float'),
        'close': pd.Series([], dtype='float'),
        'low': pd.Series([], dtype='float'),
        'high': pd.Series([], dtype='float'),
        'daily_volume': pd.Series([], dtype='float'),  # TODO: not utilized yet
        'rsi_14': pd.Series([], dtype='float'),
        'ema_10': pd.Series([], dtype='float'),  # TODO: not utilized yet
        'atr_14': pd.Series([], dtype='float'),  # TODO: not utilized yet
        'adx': pd.Series([], dtype='float'),
        'ad_plus': pd.Series([], dtype='float'),
        'ad_minus': pd.Series([], dtype='float'),
        'macd': pd.Series([], dtype='float'),
        'macd_signal': pd.Series([], dtype='float'),
        'macd_diff': pd.Series([], dtype='float'),
        'ema_fast_12': pd.Series([], dtype='float'),
        'ema_slow_26': pd.Series([], dtype='float'),
        'rsi_gain_last_5_days': pd.Series([], dtype='float')  # TODO: not utilized yet
    })

    daily_quote_df.set_index('symbol', inplace=True)

    return daily_quote_df

