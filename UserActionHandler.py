import config
import utils
from DataLoader import DataLoader


# Logic to display ranking
def display_ranking(args):
    print(f'display_ranking() w/ args {args}')


# Logic to submit orders
def submit_todays_orders(args):
    # TODO: Implement this method
    #  Logic:
    #  1. Validate, that tickers_df and daily_quotes_df are already created (as an .xlsx file)
    #  2. Confirm, that a ranking of all stocks we would like to purchase has been created
    #  3. Validate connection to IBKR
    #  4. Submit orders based on our order presets. (stated in OrderManager.py)
    #  5? Close the IBKR connection.
    print(f'submit_orders() w/ args {args}')


# Welcome message logic
def display_welcome_message():
    print('''
     _           _ _           
    (_)_ __   __| (_) __ _  ___  
    | | '_ \ / _` | |/ _` |/ _ \ 
    | | | | | (_| | | (_| | (_) |
    |_|_| |_|\__,_|_|\__, |\___/ 
                      |___/
    ''')


def display_graph_for_ticker(args):
    print(f'display_graph_for_ticker() w/ args {args}')


# Information display logic
def display_info():
    print(f'-> [E] exit the application')
    print(f'-> [P] populate database')
    print(f'-> [S] submit waiting orders')
    print(f'-> [D] display the ranking of today\'s best stock picks')
    print(f'-> [G] generate graph for a specific ticker')
    print(f'-> [I] information about the application')


class UserActionHandler:
    def __init__(self):
        self.is_testing_bool = config.MODE == 'TEST'
        self.data_loader = DataLoader()

    # Logic to populate the database
    # TODO: Anda kasutajale ka informatsiooni selle kohta, mis hetkel "andmebaasis" olemas on ja kuidas läheb
    def populate_database(self, args):
        print(f'DEBUG: populate_database() w/ args {args}')
        tickers_df = self.data_loader.get_daily_dataframe('tickers', utils.generate_initial_tickers_list_as_dataframe)
        daily_quotes_df = self.data_loader.get_daily_dataframe('daily_quotes', lambda: utils.enrich_daily_quotes_with_price_info(tickers_df, testing=self.is_testing_bool))

    def handle_user_action(self):
        display_welcome_message()
        display_info()

        while True:
            user_input = input('Please choose the next action: ').upper().strip()
            user_input_parts = user_input.split(' ')
            user_command = user_input_parts[0]
            user_args = user_input_parts[1:] if len(user_input_parts) > 1 else []

            if user_command == 'E':
                break
            elif user_command == 'I':
                display_info()
            elif user_command == 'P':
                self.populate_database(user_args)
            elif user_command == 'S':
                submit_todays_orders(user_args)
            elif user_command == 'D':
                display_ranking(user_args)
            elif user_command == 'G':
                display_graph_for_ticker(user_args)
            else:
                print('Invalid input - please try again')
