import json

import pandas as pd
import requests

def clean_user_inputs(queries):
    """
    Convert user inputs to match the api inputs.

    """
    queries = queries.lower()
    queries = queries.replace('_', '-')
    return queries

def search_cases(url):
    """
    Send queries to api and store json return. 
    The function will check for request status during the process.

    Args:
        url (string): full api query url.

    Returns:
        json: results from api.
    """
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return data
