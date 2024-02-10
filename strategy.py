import config
import utils
import pandas as pd
import math

from ibapi.contract import Contract
from ibapi.order import Order

from ib_insync import IB

from DataLoader import DataLoader
from CriteriaChecker import CriteriaChecker

# Set option to display all rows (or a large number of rows)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 400)
pd.set_option('expand_frame_repr', False)

# Calculates the "rise" of RSI_14 over the last 5 days
# Rise is defined as the sum of differences for a pairs of days
def rsi_14_rise(stock_df):
    return stock_df['rsi_14'].diff().tail(5).sum()


# TODO: Excelisse lugemisel peab daily_quote puhul enne ikkagi need rsi jms andmed sisse lööma, muidu jälle topelt töö...
# TODO: Make logging/print statements better for all of the rows
# Elapsed time for a certain block would be cool.
# Something like x out of y done as well...
# Meetodi sisu:
# 1.   Kontrollib, mis režiimis rakendus on (PROD = "tee kõike", TEST = "tee natuke")
# 2.   Leiab sobivad aktsiad kõikide* aktsiate seast   *kõikide = valitud turgudel olevad sobiva market capiga aktsiad
# 3.   Tõmbab API abil iga aktsia jaoks alla selle 90 päeva hinnainfo (close, open, high, low)
# 3.1.   "Fetching data for ticker... x/y"
# 4.   Arvutab vastavalt hinnainfole finantsnäitajad (ADX, AD+, AD-, MACD, etc)
# 5.   Finantsnäitaje pealt kontrollib iga aktsia jaoks kriteeriumid (CriteriaChecker.py)
# 5.1.   Kui aktsia vastab kriteeriumitele lisame selle potentsiaalsete aktsiate nimekirja
# 5.2.   Sorteerime nimekirja vastavalt parmaeetrile (EMA tõus)
def execute_strategy():
    # Sets up necessary classes
    criteria_checker = CriteriaChecker()
    DataLoader.create_folder(config.HISTORIC_DATA_FOLDER)

    # DataLoader.get_daily_dataframe returns a table (dataframe) of today's selected tickers
    # This selection is based on criteria defined in
    tickers = DataLoader.get_daily_dataframe('tickers')
    print("Found", len(tickers), "tickers matching screening criteria\n")

    # This part creates a large table (100K+ rows) that contains data about daily prices for each ticker over
    # the last 90 days (config.DAILY_QUOTE_DAYS)
    daily_quotes = DataLoader.get_daily_dataframe('daily_quotes', tickers_df=tickers)
    print("daily_quotes dataframe has", len(daily_quotes), "elements.")

    # This calculates all necessary indicators for the list of tickers and their dataframe
    # Think RSI, MACD, EMA, AD+ etc - they all are added by this method
    daily_quotes = utils.enrich_daily_quotes_with_indicators(daily_quotes)

    # Commented out, but can be used for debugging
    # print('\n--- DAILY QUOTES AFTER TA INDICATOR UPDATES ---')
    # print(daily_quotes.head(10))
    # print(daily_quotes.tail(10))

    # From here, the filtering based on our criteria (CriteriaChecker.py) begins
    print("\n--- STARTING TO FILTER STOCKS --- \n")
    filtered_stocks = []  # Keeps a list of tickers to later use for in-depth analysis or trading
    for symbol in daily_quotes['symbol'].unique():
        stock_df = daily_quotes[daily_quotes['symbol'] == symbol]
        if criteria_checker.check_criteria(stock_df):
            # print(f"Ticker {symbol} added to the potential stocks list (filtered_stocks)")
            filtered_stocks.append(symbol)

    # Calculate RSI_14 rise for each stock and sort
    sorted_stocks = sorted(filtered_stocks, key=lambda x: rsi_14_rise(daily_quotes[daily_quotes['symbol'] == x]),
                           reverse=True)

    print(f"Found {len(sorted_stocks)} tickers that we want to buy");
    print(f"-- TO BUY -- \n"
          f"{sorted_stocks}")

    # IB specific stuff - commented out right now
    '''
    print("--- MAKING ORDERS ---")
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=0)

    # Kontrolli ostujõudu ja olemasolevaid ordereid
    # Define the stock and the order (buying 10 of each :D)
    for symbol in sorted_stocks:
        symbol_df = daily_quotes[daily_quotes['symbol'] == symbol]
        symbol_df = symbol_df.sort_values(by='date')
        # Get the last closing price
        last_closing_price = symbol_df['close'].iloc[-1]

        # place_buy_order(symbol, last_closing_price, ib_instance)

    ib.disconnect()
    '''


execute_strategy()
