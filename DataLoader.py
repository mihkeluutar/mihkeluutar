import os
import pandas as pd
import requests
import config
import data_models
import utils

from datetime import datetime


# Returns a filename that matches the format xyz_YYYY-MM-DD.xlsx
def get_todays_filename(prefix, directory_name):
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(directory_name, f"{prefix}_{today}.xlsx")

# TL;DR - returns a dataframe of tickers matching screening criteria
'''
Fetches a list of tickers from Financial Modeling Prep API based on configuration (config.py) for
list of exchanges, minimum volume and minimum market cap. It should be possible to easily add more
constraints for the API request. Be aware, that this method just returns a list of EQUITY SYMBOLS with
some basic data. 
'''
def generate_initial_tickers_list_as_dataframe(exchanges=config.EXCHANGES_LIST,
                                               min_volume=config.MIN_VOLUME_FOR_SCREENING,
                                               min_mkt_cap=config.MIN_MKT_CAP_FOR_SCREENING):
    print(f'Creating an initial list of tickers matching criteria \n'
          f'-> min_volume= {min_volume}\n'
          f'-> min_mkt_cap= {min_mkt_cap}')

    tickers_df = data_models.empty_ticker_dataframe()
    print(f"Initialized empty dataframe: \n {tickers_df}")
    request_url = config.SCREENER_API_URL

    # TODO: Viia see request eraldi meetodisse; vbla teha mingi abiklass selle fmp api jaoks?
    #  nagu on fetch_daily_quote_data
    # Needs a separate request for each exchange
    for exchange in exchanges:
        request_params = {
            'apikey': config.FINANCIAL_MODELING_PREP_API_KEY,
            'marketCapMoreThan': min_mkt_cap,
            'volumeMoreThan': min_volume,
            'exchange': exchange,
            'isActivelyTrading': True
        }

        response = requests.get(request_url, params=request_params)

        if response.status_code == 200:
            for row in response.json():
                row_df = utils.map_json_to_ticker_df(row)
                tickers_df = tickers_df._append(row_df, ignore_index=True)
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    return tickers_df


# Handles collecting initial data to work with
class DataLoader:

    # Returns a dataframe object based on an existing excel file, if one exists;
    #  or request necessary data from API-s
    # TODO: move enriching daily_quotes away from this method so that in case of errors, the loading takes less time.
    @staticmethod
    def get_daily_dataframe(prefix, tickers_df=None, directory_name=config.HISTORIC_DATA_FOLDER):
        filename = get_todays_filename(prefix, directory_name)
        if os.path.exists(filename):
            print(f"Loading {prefix} from {filename}")
            df = pd.read_excel(filename, header=0, index_col=0)
        else:
            print(f"[{prefix}] dataframe does not exist for today yet - fetching it from API")
            if prefix == 'tickers':
                df = generate_initial_tickers_list_as_dataframe()
            if prefix == 'daily_quotes':
                df = utils.enrich_daily_quotes_with_price_info(tickers_df)
                # daily_quotes_df = utils.enrich_daily_quotes_for_tickers(tickers_df)
                # df = utils.enrich_daily_quotes_with_indicators(daily_quotes_df)
            df.to_excel(filename, index=False)

        return df

    # Creates a new root folder if necessary
    @staticmethod
    def create_folder(folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Created folder: {folder_name}")
        else:
            print(f"Folder already exists: {folder_name}")
