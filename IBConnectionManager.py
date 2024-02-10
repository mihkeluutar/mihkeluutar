from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread
import time


class IBConnectionManager(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.next_valid_order_id = None
        self.order_responses = {}  # Initialize the dictionary to store order responses

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.next_valid_order_id = orderId
        print(f"Received next valid order ID: {orderId}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):

        # This method is called to report the status of an order
        self.order_responses[orderId] = status
        print(f"Order Status - ID: {orderId}, Status: {status}, Filled: {filled}")

    def connect(self, host="127.0.0.1", port=7497, clientId=0):
        """ Connect to the Interactive Brokers API """
        super().connect(host, port, clientId)

        # Start a separate thread to run the communication loop
        thread = Thread(target=self.run)
        thread.start()

        # Wait for the connection to be established
        print('Waiting for the connection to be established...')
        time.sleep(1)
        print(f'Successfully connected to Interactive Brokers API')

    def disconnect(self):
        """ Disconnect from the Interactive Brokers API """
        super().disconnect()
        print(f'Disconnected from Interactive Brokers API')


if __name__ == "__main__":
    ib_manager = IBConnectionManager()
