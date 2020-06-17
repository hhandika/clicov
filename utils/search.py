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
    return tables

def clean_usa_results(results):
    """Function to clean pandas results

    Args:
        results ([type]): [description]
    """
    state = results['state']
    number_results = results.drop(['state'], axis=1).astype('Int64')
    # for column in number_results.columns:
    #     number_results[column] = number_results[column].apply(lambda x: f'{x:,}')
    #skip thousands separator. Only display as it is.
    final_results = pd.concat([state, number_results], axis=1)
    return final_results
