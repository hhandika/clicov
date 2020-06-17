import datetime as dt
import json
import os

import click
import pandas as pd
import requests
from tabulate import tabulate

from utils import search

#Get date and current working directory for saving files.
current_wd = os.getcwd()
date = dt.datetime.today().strftime("%Y-%m-%d")

#Setup group function for click commands. 
@click.group()
def main():
    """
    clicov 0.0.3

    A simple command line program to access covid-19 data.

    Usages:

    To display summary of cases:

    World cases: clicov summary -w

    Selected country: clicov summary -c [country-iso2-id]

    To download country cases from day one:

    clicov download -c [country-iso2-id/slug]

    For usa cases:

    All states current cases: clicov usa

    Per states: clicov usa -s [state-code]

    To display country isoid:

    All: clicov isoid

    For country with one word, you could just type the country name.

    If more, use underscore.
    
    clicov isoid -c [country-name]

    clicov isoid -c united_states

    Popular country  ISO2 codes:

    Australia: AU

    Brazil: BR

    China: CN

    France: FR

    Germany: DE

    India: IN

    Indonesia: ID

    Japan: JP

    United Kingdom : GB

    United States: US

    """
    pass

#Function to handle world cases and multi-country covid19 data. Docstring will be displayed in the command help.
@main.command('summary')
@click.option('--world', '-w', is_flag=True, help='Get summary of global covid19 cases' )
@click.option('--countries', '-c', default=None, help='Display a country summary cases')
@click.option('--save', '-sv', is_flag=True, help='Save per country cases in csv file')
def get_summary(world, countries, save):
    """
    Get covid-19 most recent global cases and/or by country cases. 
    
    To display a country summary cases, use a slug name or an ISO2 country code

    Example:

    clicov summary -c us

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
        top_table = search.change_number_formats(top_table)
        bottom_table = cases.filter(['TotalConfirmed', 'TotalRecovered', 'TotalDeaths'])
        bottom_table = search.change_number_formats(bottom_table)
        print(f'{country_name} cases:')
        print(tabulate(top_table, headers='keys', tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
        print(tabulate(bottom_table, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
        print(f'\nData date and time (24H): {accessed_date} UTC')

    if save:
        try:
            filename = 'result-country-cases_' + date + '.csv'
            country_cases.to_csv(filename, index=False)
            print(f'\nDone! \nThe results are saved in {current_wd} as {filename}')
        except PermissionError:
            print('\nThe program cannot save the results. A file with the same filename exists.')
    
    print('\nAPI: https://covid19api.com/')
    print('Data sources: CSSE, Johns Hopkins University\n')

#Options to download cases from day one. 
#Nothing will be displayed if this command is used.
#The function is a saved to csv only option.    
@main.command('download', help='Get country data from day one')
@click.option('--country', '-c', help='Select country name')
def download_results(country):
    """
    Download country covid-19 data from day one.
    Use slugs or id to choose the country.

    Commands:

    clicov download -c id
    """
    queries = search.clean_user_inputs(country)
    url = 'https://api.covid19api.com/total/country/' + queries
    results = search.search_cases(url)
    save_files = pd.json_normalize(results)
    try:
        filename = country.upper() + '-cases_' + date + '.csv'
        save_files.to_csv(filename, index=False)
        print(f'\nDone! \nThe results are saved in {current_wd} as {filename}')
    except PermissionError:
        print('\nThe program cannot save the results. A file with the same filename exists.')

 
@main.command('usa', help='Get selected state covid-19 cases')
@click.option('--states', '-s', default='all', help='Select state based on state code')
@click.option('--daily', '-d', is_flag=True, help='States covid19 data from dayone')
@click.option('--save', '-sv', is_flag=True, help='Save results to csv')
def get_usa_covid(states, daily, save):
    """
    Command to dig dive into the U.S covid19 cases. 
    You can display or download the data.
    Data is presented in state by state cases.
    For summary of the U.S covid19 cases, use the 'summary' command. 

    To display all states covid19 data:

    clicov usa

    If you wish to save all-state data:

    clicov usa -sv

    For daily cases, the option is only available per state. 
    Use -s or --states option to query this command.
    The resulting data will be saved in your current working directory.

    Example:

    clicov usa -s ny -d

    """
    if states != 'all':
        queries = search.clean_user_inputs(states)
        url = search.get_url_usa_cases(queries, daily)
    else:
        url = search.get_url_usa_cases(states, daily)
    results = search.search_cases(url)
    results = pd.json_normalize(results)

    if daily:
        filename = 'allstates-cases_' + date + '.csv'
        results.to_csv('results.csv', index=False)
        print(f'\nResults are save in {current_wd} as {filename}')
    else:
        if states == 'all':
            filename = 'allstates-cases_' + date + '.csv'
            if save:
                results.to_csv('results.csv', index=False)
                print(f'\nDetails results are save in {current_wd} as {filename}')
            filtered_results = results.filter(['state', 'positive', 'negative', 'hospitalizedCurrently', 'deathIncrease', 'hospitalizedIncrease' ])
            printed_results = search.clean_usa_results(filtered_results)
            print("\nAll U.S. states' cases:\n")
            print(tabulate(printed_results, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
        else:
            top_results = results.filter(['positive', 'negative'])
            top_results = search.change_number_formats(top_results)
            hospitalized_results = results.filter(['hospitalizedCurrently', 'hospitalizedCumulative'])

            #Try to change numbers format with thousand separators. Skip it, if the value cannot be converted.
            try:
                hospitalized_results = search.change_number_formats(hospitalized_results)
            except:
                pass

            icu_results = results.filter(['inIcuCurrently' , 'inIcuCumulative', 'onVentilatorCurrently' ])
            try:
                icu_results = search.change_number_formats(icu_results)
            except:
                pass
            trend_results = results.filter(['positiveIncrease', 'negativeIncrease','deathIncrease', 'hospitalizedIncrease'])
            try:
                trend_results = search.change_number_formats(trend_results)
            except:
                pass
            data_date = results['lastUpdateEt']
            data_date = results.to_string(index=False)
            print(f'\n{states.upper()} cases:\n')
            print(tabulate(top_results, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
            print(tabulate(hospitalized_results, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
            print(tabulate(icu_results, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
            print(tabulate(trend_results, headers='keys',  tablefmt='pretty', showindex=False, numalign='center', stralign='center'))
            print(f'\nData date and time (24H): {data_date} ET')

    print('\nData provider: The Covid Tracking Project at the Atlantic')
    print('Data license: CC BY-NC-4.0')
    print('Details on data usages: https://covidtracking.com/about-data')
    

@main.command('id', help='Display country ISO2 id')
@click.option('--country', '-c', default= None, help ='Select by country')
def get_isoid(country):
    """
    Get ISO2 country code. 

    To display all-country codes:

    clicov id

    To display select country:

    For single word country:

    clicov id -c indonesia

    For multi-words country name, use underscore:

    clicov id -c united_states

    """
    url = 'https://api.covid19api.com/countries'
    results = search.search_cases(url)
    tabled_results = pd.json_normalize(results)
    tabled_results = tabled_results.sort_values(by=['Country'])

    if country is not None:
        queries = search.clean_user_inputs(country)
        country_id = tabled_results.loc[tabled_results['Slug'] == queries]
        print(tabulate(country_id, headers='keys', tablefmt='pretty', showindex=False, stralign='center'))
    else:
        print(tabulate(tabled_results, headers='keys', tablefmt='pretty', showindex=False, stralign='center'))

if __name__ == '__main__':
    main()