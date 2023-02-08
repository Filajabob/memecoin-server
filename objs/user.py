import json
import random
from constants import Constants
import utils
from .errors import *


class User:
    def __init__(self, id, firstname, lastname, alias, email, password, balance):
        """
        A User, which can hold MemeCoins, transact them, or otherwise interact with MemeCoin.

        :param id: int: An identifying number, unique from other Users.
        :param firstname: str: First name of the user
        :param lastname: str: Last name of the user
        :param alias: str: A unique alias for the user
        :param email: str: The email of the user
        :param password: str: The password for the user.
        :param balance: int: The amount of MemeCoins in the user's account
        """

        self.id = str(id)
        self.firstname = firstname
        self.lastname = lastname
        self.alias = alias
        self.email = email
        self.password = password
        self.balance = balance

    def serialize(self, output: str = None):
        """
        Convert User to a JSON format which can be saved and later reloaded into the User object.

        :param output: str: A filepath to a JSON file, where the serialized results should be outputted. If None, the
        results will not be saved anywhere.

        :returns: dict: The final serialized data
        """

        serialized_data = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "alias": self.alias,
            "email": self.email,
            "password": self.password,
            "balance": self.balance
        }

        if output:
            with open(output, 'r+') as f:
                data = json.load(f)
                data[str(self.id)] = serialized_data

                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

        return serialized_data

    def deduct(self, amount: int, *, local_save: bool = False):
        """
        A barebones method to deduct MemeCoins. For fines, taxes, etc. a Transaction should be made, sent to a
        placeholder Bank.
        :param amount: int: The amount to deduct
        :param local_save: Whether to skip serializing/saving and to perform a deduction to the User object only.
        :return:
        """

        self.balance -= amount

        if not local_save:
            self.serialize()

    def increase(self, amount: int, *, local_save: bool = False):
        """
        Similar to deduct, except increasing balance instead of deducting
        :param amount: int: The amount to deduct
        :param local_save: Whether to skip serializing/saving and to perform an increase to the User object only.
        :return:
        """

        self.balance += amount

        if not local_save:
            self.serialize()

    def notify(self, subject, content):
        raise NotImplementedError()

    def alias_is_unique(self):
        """
        Checks if the User's alias is unique, compared to all other serialized users
        :return: bool: Whether the alias is unique
        """

        with open(Constants.USERS_JSON, 'r') as f:
            data = json.load(f)

        aliases = []

        for id, user in data.items():
            print(user)
            aliases.append(user["alias"])

        if self.alias in aliases:
            return False
        else:
            return True

    @staticmethod
    def new(firstname, lastname, alias, email, password):
        """
        Automated process to create and log a new User
        :param email:
        :param alias:
        :param firstname:
        :param lastname:
        :param password:
        :return: User
        """

        with open(Constants.USERS_JSON, 'r+') as f:
            raw_users = json.load(f)

        id = random.randint(100000, 999999)

        while id in raw_users.keys():
            id = random.randint(100000, 999999)

        user = User(id, firstname, lastname, alias, email, password, 0)

        if not user.alias_is_unique():
            raise DuplicateAlias("Alias is not unique.")

        user.serialize(Constants.USERS_JSON)

        return user

    @staticmethod
    def load_from_id(id):
        with open(Constants.USERS_JSON, 'r') as f:
            data = json.load(f)

        try:
            raw_user = data[str(id)]
        except KeyError:
            raise UserNotFound("User was not found.")

        return User(**raw_user)

    @staticmethod
    def load_from_alias(alias):
        return User.load_from_id(utils.user_lookup())
