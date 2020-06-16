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

def get_url_usa_cases(queries, current, allstates):
    """

    Args:
        url ([type]): [description]
    """
    extension = '.json'
    link = 'https://covidtracking.com/api/v1/states/'
    if queries is not None:
        if current:
            url =  link + queries + current + extension
            return url
        else:
            url = url =  link + queries + 'daily' + extension
            return url
    if allstates:
        url = link + current + extension
        return url
