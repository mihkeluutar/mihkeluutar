# Indigo autoTrader

Indigo autoTrader is a simple python program that creates stock buy/sell orders in Interactive Brokers using
a set of predefined strategies and parameters

To set up your environment:
1. Copy `config_template.py` to `config.py`:


## Running the application

TODO...

## 2. How it works

### CriteriaChecker

### 2.2. DataLoader
The DataLoader class in Indigo autoTrader is responsible for handling the initial data collection and processing.
It ensures the program operates with the most current data for stock trading analysis and decision-making.

**2.2.1. Key Functions:**

```load_or_fetch_dataframe(prefix)```: Checks for an existing Excel file with the day's data.
If not found, it fetches the data from APIs based on the prefix parameter (either "tickers" or "daily_quotes").
The retrieved data is then saved to an Excel file so we wouldn't need to make multiple expensive API queries per day.

```create_folder(folder_name)```: Ensures the required directory for storing data files exists,
creates a new one if it doesn't.

```get_todays_filename(prefix, directory_name)```: Utility function used internally to generate filenames for storing data,
following the format prefix_YYYY-MM-DD.xlsx.

```generate_initial_tickers_list_as_dataframe(exchanges, min_volume, min_mkt_cap)```: Creates an initial list of tickers
meeting specific criteria such as minimum volume and market cap, fetched from a specified API for each exchange in the
exchanges list.

### DataProcessor

### IBConnectionManager

### OrderManager

### StrategyExecutor

### UserActionHandler

### config.py


## List of used API-s

## TODO

1. Teha veebiliides, kust saab käivitada esimest ja teist protsessi
2. Veebiliideselt võimaldada exceli alla laadimised
3. Teha korda suhtlemine IBKR-ga
4. Teha korda ostmise loogika
5. Teha korda müümise loogika
6. Panna rakendus jooksma iga päev vastu IBKR-i testi
7. Teha valmis backtestimise raamistik
8. Alustada backtestimisega

