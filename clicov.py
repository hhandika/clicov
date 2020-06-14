import json

import requests
import pandas as pd
import click
from tabulate import tabulate

from utils import search

@click.command()
@click.option('--summary', '-s', is_flag=True, help='Get summary of new cases' )
@click.option('--countries', '-c', default=None, help='Select country new cases')
def main(summary, countries):
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
        print('\nGlobal Cases:\n')
        print(f'New confirmed: {confirmed_cases:,}')
        print(f'Total confirmed: {total_cases:,}')
        print(f'New deaths: {new_deaths:,}')
        print(f'New recovered: {new_recovered:,}')
        print(f'Total recovered: {total_recovered:,}\n')
    if countries:
        countries = countries.title()
        country_cases = pd.json_normalize(results['Countries'])
        cases = country_cases.loc[country_cases['Country'] == countries]
        df1 = cases.filter(['NewConfirmed', 'TotalConfirmed', 'NewDeaths'])
        df2 = cases.filter(['TotalDeaths', 'NewRecovered', 'TotalRecovered'])
        print(countries.title())
        print(tabulate(df1, headers='keys', tablefmt='psql'))
        print(tabulate(df2, headers='keys',  tablefmt='psql'))
