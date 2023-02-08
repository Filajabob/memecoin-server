import json
from constants import Constants
import objs


def user_lookup(alias):
    """
    Find a User's id that has a certain alias
    :param alias: The alias to search
    :return: str or None: The user's id that was found, if not found, then None
    """

    with open(Constants.USERS_JSON, 'r') as f:
        data = json.load(f)

    for user in data.values():
        if alias in user.values():
            return user["id"]
    else:
        return None
