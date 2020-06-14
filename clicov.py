import json

import requests
import pandas as pd
import click

from utils import search

@click.command()
@click.option('--summary', '-s', is_flag=True, help='Get summary of new cases' )
def main(summary):
    """
    """
    url = 'https://api.covid19api.com/summary'
    results = search.search_cases(url)
    global_cases = results['Global']
    if summary:
        confirmed_cases = global_cases['NewConfirmed']
        total_cases = global_cases['TotalConfirmed']
        new_deaths = global_cases['NewDeaths']
        new_recovered = global_cases['NewRecovered']
        total_recovered = global_cases['TotalRecovered']
        global_cases = results['Global']
        print('\nGlobal cases:')
        print(f'New Confirmed: {confirmed_cases}')
        print(f'Total Confirmed: {total_cases}')
        print(f'New Deaths: {new_deaths}')
        print(f'NewRecovered: {new_recovered}')
        print(f'TotalRecovered: {total_recovered}\n')