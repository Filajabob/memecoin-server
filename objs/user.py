import json
import random
from constants import Constants


class User:
    def __init__(self, id, firstname, lastname, password, balance):
        """
        A User, which can hold MemeCoins, transact them, or otherwise interact with MemeCoin.

        :param id: int: An identifying number, unique from other Users.
        :param firstname: str: First name of the user
        :param lastname: str: Last name of the user
        :param password: str: The password for the user.
        :param balance: int: The amount of MemeCoins in the user's account
        """

        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.balance = balance

    def serialize(self, output: str = None):
        """
        Convert User to a JSON format which can be saved and later reloaded into the User object.

        :param output: str: A filepath to a JSON file, where the serialized results should be outputted. If None, the results will not be saved
        anywhere.

        :returns: dict: The final serialized data
        """

        serialized_data = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
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

    @staticmethod
    def new(firstname, lastname, password):
        """
        Automated process to create and log a new User
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

        user = User(id, firstname, lastname, password, 0)
        user.serialize(Constants.USERS_JSON)

        return user
