# High level important stuff
MODE = 'PROD'  # Use 'TEST' or 'PROD'

# API keys and endpoints
FINANCIAL_MODELING_PREP_API_KEY = "your_key_here"

# Financial Modeling Prep V3 Stock Screener
SCREENER_API_URL = "https://financialmodelingprep.com/api/v3/stock-screener"
DAILY_QUOTE_API_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/1day/"  # Should always add the ticker symbol to the end
HISTORICAL_EARNINGS_API_URL = "https://financialmodelingprep.com/api/v3/earning_calendar"

# Other variables, such as markets, max order sizes, etc
MIN_VOLUME_FOR_SCREENING = 500000  # 500k daily volume
MIN_MKT_CAP_FOR_SCREENING = 2000000000  # 2bln usd
EXCHANGES_LIST = ["nyse", "nasdaq"]  # You can add exchanges as you wish :)
DAILY_QUOTE_DAYS = 90  # A decrease in performance, but increases accuracy
TESTING_API_CAP = 20
OVERALL_API_CAP = -1

# FILE SYSTEM
HISTORIC_DATA_FOLDER = '01_daily_data'

# Order information
LOT_SIZE_USD = 1000


