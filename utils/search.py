import pandas as pd, requests, json


def set_queries(queries):
    """

    Args:
        params ([type]): [description]
    """
    link = 'https://api.covid19api.com/'
    params = queries
    search_link = link + params
    return search_link

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