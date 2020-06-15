import json
import os
import datetime as dt

import requests
import click
import pandas as pd
from tabulate import tabulate

from utils import search

@click.group()
def main():
    pass

@main.command('summary')
@click.option('--world', '-w', is_flag=True, help='Get summary of global cases' )
@click.option('--countries', '-c', default=None, help='Use ISO2 country code to display a country summary cases')
@click.option('--save', '-sv', is_flag=True, help='Save per country cases in csv file')
def summary(world, countries, save):
    """Get covid-19 most recent global cases and/or by country cases. 

    Args:
        summary (text): print global most recent cases
        countries (text): print user selected country most recent cases
        save (bool): If flagged, the results will be saved in the current user working directory.
    """
    url = 'https://api.covid19api.com/summary'
    results = search.search_cases(url)
    country_cases = pd.json_normalize(results['Countries'])

    if world:
        global_cases = results['Global']
        new_confirmed = global_cases['NewConfirmed']
        new_deaths = global_cases['NewDeaths']
        new_recovered = global_cases['NewRecovered']
        total_cases = global_cases['TotalConfirmed']
        total_recovered = global_cases['TotalRecovered']
        total_death = global_cases['TotalDeaths']
        global_cases = results['Global']
        print('\nGlobal Cases:\n')
        print(f'New confirmed: {new_confirmed:,}')
        print(f'New recovered: {new_recovered:,}')
        print(f'New deaths: {new_deaths:,}')
        print(f'Total confirmed: {total_cases:,}')
        print(f'Total recovered: {total_recovered:,}')
        print(f'Total deaths: {total_death:,}\n')

    if countries:
        country_id = countries.upper()
        cases = country_cases.loc[country_cases['CountryCode'] == country_id]
        country_name = country_cases.loc[country_cases['CountryCode'] == country_id, 'Country']
        country_name = country_name.to_string(index=False)
        accessed_date = cases['Date'].to_string(index=False)
        accessed_date = accessed_date.replace('T', ' ').replace('Z','')
        top_table = cases.filter(['NewConfirmed','NewRecovered' , 'NewDeaths'])
        for column in top_table.columns:
            top_table[column] = top_table[column].apply(lambda x: f'{x:,}')
        bottom_table = cases.filter(['TotalConfirmed', 'TotalRecovered', 'TotalDeaths'])
        for column in bottom_table.columns:
            bottom_table[column] = bottom_table[column].apply(lambda x: f'{x:,}')
        print(f'{country_name} cases:')
        print(f'\nData date and time (24H): {accessed_date}')
        print(tabulate(top_table, headers='keys', tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
        print(tabulate(bottom_table, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))

    if save:
        try:
            current_wd = os.getcwd()
            date = dt.datetime.today().strftime("%Y-%m-%d")
            filename = 'result-country-cases_' + date + '.csv'
            country_cases.to_csv(filename, index=False)
            print(f'\nDone! \nThe results are saved in {current_wd} as {filename}')
        except PermissionError:
            print('\nThe program cannot save the results. A file with the same filename exists.')
    
    print('\nAPI: https://covid19api.com/')
    print('Data source: the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University\n')
    
@main.command('country', help='Get country data from day one')
@click.option('--select', '-c', help='Select country name')
def country(select):
    pass

@main.command('usa', help='Get selected state covid-19 cases')
@click.option('--state', '-s', help='Select state based on state code')
def usa(state):
    pass
