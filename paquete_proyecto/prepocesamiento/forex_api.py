import os
from dotenv import load_dotenv  # remember: pip install python-dotenv
import requests

load_dotenv()

TOKEN = os.environ["TOKEN_AV"]


def alpha_vantage_fx_api(function, from_symbol, to_symbol, api_key):
    """API SERVICE OF ALPHA VANTAGE

    Keyword arguments:
    function = FX_DAILY, FX_WEEKLY, FX_MONTHLY
    from_symbol: first asset
    to_symbol: second asset
    api_key: personal TOKEN
    Return: JSON
    """
    function = function
    from_symbol = from_symbol
    to_symbol = to_symbol
    api_key = api_key

    URL_BASE = "https://www.alphavantage.co/"

    URL = URL_BASE + "query?function=" + function
    URL += "&from_symbol=" + from_symbol
    URL += "&to_symbol=" + to_symbol
    URL += "&apikey=" + api_key

    r = requests.get(URL)
    return r.json()


if __name__ == "__main__":
    from pprint import pprint

    data = alpha_vantage_fx_api("FX_MONTHLY", "COP", "USD", TOKEN)
    pprint(data)
