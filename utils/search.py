import pandas as pd, requests, json


def clean_user_inputs(queries):
    """

    Args:
        params ([type]): [description]
    """
    queries = queries.lower()
    queries = queries.replace('_', '-')
    return queries

def search_cases(url):
    """[summary]

    Args:
        url ([type]): [description]

    Returns:
        [type]: [description]
    """
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return data

def save_results(filename):
    """

    Args:
        filename ([type]): [description]
    """
