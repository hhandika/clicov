import json
import os

import requests
import pandas as pd
import click
from tabulate import tabulate

from utils import search

@click.command()
@click.option('--world', '-w', is_flag=True, help='Get summary of global cases' )
@click.option('--countries', '-c', default=None, help='Select based on the country code')
@click.option('--save', '-s', is_flag=True, help='Save per country cases in csv file')
def main(world, countries, save):
    """Get covid-19 most recent data and convert it to pandas dataframe. 

    Args:
        summary (text): print global most recent cases
        countries (text): print user selected country most recent cases
        save (bool): option to save the search results
    """
    url = 'https://api.covid19api.com/summary'
    results = search.search_cases(url)
    global_cases = results['Global']
    country_cases = pd.json_normalize(results['Countries'])

    if world:
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
        country_code = countries.upper()
        cases = country_cases.loc[country_cases['CountryCode'] == country_code]
        country_name = country_cases.loc[country_cases['CountryCode'] == country_code, 'Country']
        country_name = country_name.to_string(index=False)
        country_name = country_name.replace(' ','')
        accessed_date = cases['Date'].to_string(index=False)
        accessed_date = accessed_date.replace('T', ' ').replace('Z','')
        df1 = cases.filter(['NewConfirmed', 'TotalConfirmed', 'NewDeaths'])
        for i in df1.columns:
            df1[i] = df1[i].apply(lambda x: f'{x:,}')
        df2 = cases.filter(['TotalDeaths', 'NewRecovered', 'TotalRecovered'])
        for i in df2.columns:
            df2[i] = df2[i].apply(lambda x: f'{x:,}')
        print(f'{country_name} cases:\n')
        print(f'Date: {accessed_date}')
        print(tabulate(df1, headers='keys', tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
        print(tabulate(df2, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
    if save:
        try:
            country_cases.to_csv('country_cases.csv', index=False)
            print('\nDone! saved')
        except PermissionError:
            print('\nThe same file exist. Permission to overwrite the file is denied.')

