class Transaction:
    def __init__(self, sender, recipent, amount):
        """
        A placeholder for a transaction between two users. Does not include authentication.

        :param sender:
        :param recipent:
        :param amount:
        """

        self.sender = sender
        self.recipent = recipent
        self.amount = amount

    def validate(self):
        pass