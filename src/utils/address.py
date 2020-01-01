from urllib import parse

import requests

from src.utils import GENERIC_ERROR_MSG


def get_address(postcode):
    postcode = postcode.upper()

    res = requests.get(f"https://postcodes.io/postcodes/{parse.quote(postcode)}")

    if res.status_code == 200:
        return res.json()["result"]
    else:
        if res.status_code == 404:
            error_msg = f'Postcode "{postcode}" cannot be found. Please try another postcode.'
        else:
            error_msg = GENERIC_ERROR_MSG
        return {"error_message": error_msg}
