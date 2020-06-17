import json

import pandas as pd
import requests

def clean_user_inputs(queries):
    """
    Convert user inputs to match the api inputs.

    Args:
        queries (string): country/us state codes

    Returns:
        string: lowercase codes and replace underscore to dash
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
    Build full url to send request to the covid tracking api.

    Args:
        states (string): states code
        daily (string): show current data or daily data from first cases

    Returns:
        string: a full url
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
    Change number format to thousand separators.

    Args:
        tables (int/float): a pandas table.

    Returns:
        a thousand  separated pandas table.
    """
    for column in tables.columns:
        tables[column] = tables[column].apply(lambda x: f'{x:,}')
    return tables

def clean_usa_results(results):
    """Function to clean pandas results and add thousand separator.

    Args:
        results : pass pandas table
    """
    state = results['state']
    number_results = results.drop(['state'], axis=1)
    #The api provided some data in float that display .0 in the value.
    #Change nan to 0 will allow the method to convert the data to integer. 
    #But, we can't tell the different between 0 cases vs no value provided.
    #Retain the value as it is to prevent misinterpretation.
    # number_results = number_results.fillna(0).astype('Int64')
    try:
        number_results = change_number_formats(number_results)
    except:
        pass
    final_results = pd.concat([state, number_results], axis=1)
    return final_results
