import requests as requests
import pandas as pd
import time
import ta
from datetime import datetime, timedelta

import config
import data_models


def map_json_to_ticker_df(json_row):
    # print(f"Mapping json to ticker: {json_row}")
    new_row = {
        'symbol': json_row.get('symbol'),
        'name': json_row.get('companyName'),
        'market_cap': json_row.get('marketCap'),
        'volume': json_row.get('volume'),
        'exchange': json_row.get('exchange')
    }

    return new_row


def map_json_to_daily_quote_df(ticker, json_row):
    new_row = {
        'symbol': ticker,
        'date': datetime.strptime(json_row.get('date'), '%Y-%m-%d %H:%M:%S'),
        'open': json_row.get('open'),
        'close': json_row.get('close'),
        'low': json_row.get('low'),
        'high': json_row.get('high')
    }

    return new_row


def fetch_daily_quote_data(ticker, days_of_data=config.DAILY_QUOTE_DAYS):
    # TODO: viimane päev peaks olema tegelt viimane CLOSETUD päev; vähemalt vaikimisi
    last_date = datetime.now()
    from_date = last_date - timedelta(days=days_of_data)

    # Dates need to be in a string format for the request
    last_date_str = last_date.strftime('%Y-%m-%d')
    from_date_str = from_date.strftime('%Y-%m-%d')

    request_url = config.DAILY_QUOTE_API_URL + ticker

    query_params = {
        'apikey': config.FINANCIAL_MODELING_PREP_API_KEY,
        'type': 'rsi',  # needs to be here to get some quote data
        'period': 10,
        'from': from_date_str,
        'to': last_date_str
    }

    response = requests.get(request_url, params=query_params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data for ticker [{ticker}]: {response.status_code}")


# If testing=True, then only the requests for the first x tickers will be made to minimize API usage
def enrich_daily_quotes_with_price_info(tickers_df, days_of_data=config.DAILY_QUOTE_DAYS):
    daily_quotes_df = data_models.empty_daily_quote_dataframe()

    total_count = len(tickers_df)

    for index, row in tickers_df.iterrows():
        ticker = row['symbol']
        print(f"Fetching data for ticker: {ticker} - {index + 1}/{total_count}")

        try:
            daily_data = fetch_daily_quote_data(ticker, days_of_data)
            for data_row in daily_data:
                daily_quotes_df = daily_quotes_df._append(map_json_to_daily_quote_df(ticker, data_row),
                                                          ignore_index=True)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            break

        # Sleep to avoid hitting API rate limits
        # TODO: Make it more dynamic and without time.sleep; we should instead retry request after some time if we get a timeout
        time.sleep(0.040)  # At most 240 requests per sec (limit is 300); for 1000 tickers we waste 40 seconds.

    return daily_quotes_df


def calculate_rsi(df, window=14):
    df['rsi_14'] = ta.momentum.RSIIndicator(close=df['close'], window=window).rsi()
    return df


# TODO: siin võib olla jama sellega, et andmeid ei ole piisavalt; kas siis viskame lihtsalt minema asja?
def calculate_adx(df, window=14):
    adx_indicator = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=window)
    df['adx'] = adx_indicator.adx()
    df['ad_plus'] = adx_indicator.adx_pos()
    df['ad_minus'] = adx_indicator.adx_neg()
    return df


def ema(series, window):
    return series.ewm(span=window, adjust=False).mean()


# If needed the periods can be altered
# TODO: maybe we should have MACD stuff in config as well?
def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['ema_fast_12'] = ema(df['close'], fast_period)
    df['ema_slow_26'] = ema(df['close'], slow_period)
    df['macd'] = df['ema_fast_12'] - df['ema_slow_26']
    df['macd_signal'] = ema(df['macd'], signal_period)
    df['macd_diff'] = df['macd'] - df['macd_signal']

    return df


# TODO: EMA_10 ka
# TODO: ATR (14 päeva oma) ka
# Function that adds indicators to the daily_quote dataframe
def enrich_daily_quotes_with_indicators(df):
    unique_symbols = df['symbol'].unique()
    result_df = pd.DataFrame()

    # For every symbol, a sub-dataframe "stock_df" is created and later added to the main dataframe.
    for symbol in unique_symbols:
        stock_df = df[df['symbol'] == symbol].copy()
        stock_df = stock_df.sort_values(by='date')
        stock_df = calculate_rsi(stock_df)
        # stock_df = calculate_adx(stock_df)
        stock_df = calculate_macd(stock_df)
        result_df = pd.concat([result_df, stock_df])

    return result_df
