import json
from datetime import datetime
from constants import Constants
from. errors import *


class Transaction:
    def __init__(self, sender, recipent, amount):
        """
        A placeholder for a transaction between two users. Does not include authentication.

        :param sender:
        :param recipent:
        :param amount:
        """

        with open(Constants.TRANSACTIONS_JSON, 'r') as f:
            transactions = json.load(f)

        self.id = len(transactions)

        self.sender = sender
        self.recipent = recipent
        self.amount = amount
        self.request_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    def valid(self):
        if self.sender.balance < self.amount:
            return False
        else:
            return True

    def serialize(self, output=None):
        serial = {
            "id": self.id,
            "sender": self.sender.serialize(),
            "recipent": self.recipent.serialize(),
            "amount": self.amount,
            "request_timestamp": self.request_timestamp
        }

        if output:
            with open(Constants.TRANSACTIONS_JSON) as f:
                data = json.load(f)
                data.append(serial)

        return serial

    def execute(self, *, force=False, log=True):
        """
        Executes the transaction.
        :param force: bool: Whether to not check Transaction.validate() before running the transaction.
        :param log: bool: Whether to log the transaction
        :raises: objs.errors.InsufficientFunds: When force = False, this is raised when the sender doesn't have enough
        MemeCoin.
        :return:
        """

        if not force:
            if not self.valid():
                raise InsufficientFunds("Insufficient funds.")

        if log:
            self.serialize(Constants.TRANSACTIONS_JSON)

        self.sender.deduct(self.amount)
        self.recipent.increase(self.amount)

        # TODO: When User.notify is implemented, should be added here.
