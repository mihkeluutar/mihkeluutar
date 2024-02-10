from ibapi.contract import Contract
from ibapi.order import Order
import math
import time
import config  # Configuration file that holds base references for the application


class OrderManager:
    def __init__(self, client):
        self.client = client  # EClient instance
        self.def_sec_type = 'STK'
        self.def_exchange = 'SMART'
        self.def_currency = 'USD'
        self.next_order_id = 1  # Initialize a simple order ID counter

    # TODO: Always needs to be called before placing an order!
    def sync_order_id(self):
        # Request the next valid order ID from the server
        self.client.reqIds(-1)

        # Wait for the response (in a real application, consider a more robust approach)
        while self.client.next_valid_order_id is None:
            time.sleep(0.1)  # Adjust sleep time as necessary

        # Set the next order ID to the received value
        self.next_order_id = self.client.next_valid_order_id
        # print(f"Synchronized order ID: {self.next_order_id}")

    def create_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = self.def_sec_type
        contract.exchange = self.def_exchange
        contract.currency = self.def_currency
        return contract

    def place_order(self, contract, order):
        # TODO: Figure out why removing those two is necessary
        order.eTradeOnly = False
        order.firmQuoteOnly = False

        self.sync_order_id()
        self.client.placeOrder(self.next_order_id, contract, order)
        print(f"Placed order to {order.action} {order.totalQuantity} shares of {contract.symbol} at ${order.lmtPrice} each.")
        self.next_order_id += 1

    # TODO: Finish this method as well, so we know how to place orders and can later check them in IBKR
    # TODO: Kas peaks panema korraga sisse kaks orderit? Ostuks ja müügiks
    # TODO: Selle meetodi kirjeldus ka siia
    def place_buy_order(self, symbol, price, quantity=0):
        self.sync_order_id()

        contract = self.create_contract(symbol)

        if quantity < 1:
            quantity = math.floor(price / config.LOT_SIZE_USD)

        # Order information
        order = Order()
        order.action = 'BUY'
        order.orderType = 'LMT'
        order.totalQuantity = quantity
        order.lmtPrice = price
        order.tif = 'DAY'

        self.place_order(contract, order)

    # TODO 1: Mine välja kui päeva kyynal sulgub madalamal kui 10 päeva exponentsiaalne keskmine (EMA_10); anname yhe päeva ooteaega
    #  loogika on selles, et momentum võib taastuda. Aga see order on sama, mis esialgses dokumendis.
    # TODO 2: This method should check all our open orders, go over the data and see if the parameters have changed enough,
    #  so that we would wish to sell
    #  could be good to execute the method before market open every day?
    def close_open_orders(self):
        pass
        # TODO: Implementation...
