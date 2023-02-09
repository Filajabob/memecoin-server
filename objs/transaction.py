import json
from datetime import datetime
from constants import Constants
from. errors import *


class Transaction:
    def __init__(self, sender, recipient, amount):
        """
        A placeholder for a transaction between two users. Does not include authentication.

        :param sender:
        :param recipient:
        :param amount:
        """

        with open(Constants.TRANSACTIONS_JSON, 'r') as f:
            transactions = json.load(f)

        self.id = len(transactions)

        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.request_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.execution_timestamp = None

    def valid(self):
        if self.sender.balance < self.amount:
            return False
        else:
            return True

    def serialize(self, output=None):
        serial = {
            "id": self.id,
            "sender": str(self.sender.id),
            "recipient": str(self.recipient.id),
            "amount": self.amount,
            "request_timestamp": self.request_timestamp,
            "execution_timestamp": self.execution_timestamp
        }

        if output:
            with open(output, 'r+') as f:
                data = json.load(f)
                data[str(self.id)] = serial

                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

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

        self.sender.deduct(self.amount)
        self.recipient.increase(self.amount)

        self.execution_timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        if log:
            self.serialize(Constants.TRANSACTIONS_JSON)

        # TODO: When User.notify is implemented, should be added here.
