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

def get_url_usa_cases(states, daily):
    """

    Args:
        url ([type]): [description]
    """
    link = 'https://covidtracking.com/api/v1/states/'
    if daily:
        extension = '/daily.json'
    else:
        extension = '/current.json'
    if states != 'all':
        url = link + states + extension
        return url
    else:
        url = link + extension
        return url

def change_number_formats(tables):
    """

    Args:
        tables ([type]): [description]
    """
    for column in tables.columns:
        tables[column] = tables[column].apply(lambda x: f'{x:,}')