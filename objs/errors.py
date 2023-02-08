class InvalidTransaction(Exception):
    pass


class InsufficientFunds(InvalidTransaction):
    pass


class DuplicateAlias(Exception):
    pass


class UserNotFound(Exception):
    pass
