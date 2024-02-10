import config
from CriteriaChecker import CriteriaChecker
from DataLoader import DataLoader
from DataProcessor import DataProcessor
from IBConnectionManager import IBConnectionManager
from OrderManager import OrderManager


def provide_disclaimer():
    print(f'------------------------------\n'
          f'Current application mode: {config.MODE} \n'
          f'------------------------------')


class StrategyExecutor:
    def __init__(self):
        self.data_loader = DataLoader()
        self.data_processor = DataProcessor()
        self.criteria_checker = CriteriaChecker()
        self.order_manager = OrderManager()
        self.ib_connection_manager = IBConnectionManager()

    @staticmethod
    def execute_long_swing_strategy():
        provide_disclaimer()

        pass
        # TODO: Implementation...


if __name__ == '__main__':
    StrategyExecutor.execute_long_swing_strategy()
