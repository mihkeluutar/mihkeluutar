from fmp_python import fmp

import config
import requests
from datetime import datetime, timedelta


# Data from API looks a little like this
'''
[
  {
    "date": "2024-10-31",
    "symbol": "AAPL",
    "eps": null,
    "epsEstimated": null,
    "time": "amc",
    "revenue": null,
    "revenueEstimated": null,
    "updatedFromDate": "2024-01-31",
    "fiscalDateEnding": "2024-09-30"
  },
  ...
]
'''
def fetch_earnings_data(ticker, timeframe_plus_minus):
    # print("Fetching earnings data...")
    today = datetime.now()
    date_from = (today - timedelta(days=timeframe_plus_minus)).strftime('%Y-%m-%d')
    date_to = (today + timedelta(days=timeframe_plus_minus)).strftime('%Y-%m-%d')

    request_url = f"https://financialmodelingprep.com/api/v3/historical/earning_calendar/{ticker}"

    query_params = {
        'apikey': config.FINANCIAL_MODELING_PREP_API_KEY,
        'from': date_from,
        'to': date_to,
    }

    response = requests.get(request_url, params=query_params)
    if response.status_code == 200:
        # print("Received response for request!")
        return response.json()
    else:
        raise Exception(f"Error fetching earnings data for ticker {ticker}. Response status: {response.status_code}")


def check_earnings_in_n_days(symbol, today=datetime.now(), timeframe=10):
    earnings_data = fetch_earnings_data(symbol, timeframe)

    for data_object in earnings_data:
        try:
            earnings_date = datetime.strptime(data_object['date'], '%Y-%m-%d')
            # Ensuring both comparisons are explicitly with datetime objects
            if (earnings_date + timedelta(days=timeframe)) >= today >= (earnings_date - timedelta(days=timeframe)):
                print(f"Earnings is within {timeframe} days for {symbol}, thus discarding it as a candidate.")
                return True
        except Exception as e:
            print(f"Error comparing dates: {e}")
    return False


class CriteriaChecker:

    def __init__(self):
        self.fmp_api = fmp.FMP(config.FINANCIAL_MODELING_PREP_API_KEY)

    @staticmethod
    # Increase logging
    def check_criteria(stock_df):
        # Ensure the DataFrame is sorted by date
        stock_df = stock_df.sort_values(by='date')

        # Criteria 1: ADX rising trend over the last 5 days
        crit_1 = stock_df['adx'].diff().tail(5).sum() > 0

        # Criteria 2: AD+ higher than AD- on the last day
        crit_2 = stock_df['ad_plus'].iloc[-1] > stock_df['ad_minus'].iloc[-1]

        # Criteria 3: RSI_14 rising trend over the last 5 days
        crit_3 = stock_df['rsi_14'].diff().tail(5).sum() > 0

        # Criteria 4: MACD histogram positive over last x days / modify by setting .tail(x)
        crit_4 = (stock_df['macd_diff'].tail(1) > 0).all()

        # Criteria 5: RSI_14 on last day should be under 70
        crit_5 = stock_df['rsi_14'].iloc[-1] < 60

        # crit_6 = check_earnings_in_n_days(stock_df[0]['symbol'], timeframe=10)

        # TODO: Valideerida, kas on relevantne
        #  Criteria x: ADX tuleb kõige alt ja pöörab üles... (momentum) (CNH 25.10.2022 näide)
        #  ADX peab olema teinud liikumise 10 pealt 15 peale
        #  Selle liikumise ajal peaksid ka roheline ja punane olema sellest kõrgemal
        #  Sel juhul saab välja visata crit_1

        # TODO: Kontrollida ka earninguid, et poleks 10 päeva sees

        # TODO: Kontrollida potentsiaali mineviku tippude pealt

        # Logging
        # print(f"CriteriaChecker results for [{stock_df['symbol'][0]}] are: C1={crit_1}, C2={crit_2}, C3={crit_3}, C4={crit_4}, C5={crit_5}.")

        # Using this, since adx calculation is broken right now
        return crit_3 and crit_4 and crit_5
        # return crit_1 and crit_2 and crit_3 and crit_4 and crit_5


# for testing
# check_earnings_in_n_days('AAPL', timeframe=10)
