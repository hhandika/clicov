<h3 align='center'>clicov</h3>
<p align='center'>A cli application to quickly view and download covid-19 data.</p>
<hr/>
You can quickly view and/or download covid-19 cases from your Terminal. The data are available for global cases and per country cases. The U.S cases are available in per state basis and include positive and negative testing results.

## Installation

Installation from github:

```
git clone https://github.com/hhandika/clicov.git
cd clicov/
pip install --editable .
```

## Global Cases

To view summary of global cases:

```
clicov -w
```

To view summary of user selected country cases, use the command -c and add the country two-letter <a href='https://www.iban.com/country-codes'>iso2 code</a>. You can also use the country name, but iso2 codes will yield more consistent results, particularly for multi-word country names.

```
clicov -c [country-iso2-code]

#For example, US cases:
clicov -c us

#You can chain it with global cases:
clicov -w -c us
```

To download a summary of all countries' current cases:

```
clicov summary -sv
```

Per country cases from day one is also available for download:

```
clicov download -c [country-iso2-code]
```
All files will be saved in a comma-separated values (.csv) format.

## The U.S Cases

This option is available to dig dive into the U.S states' cases. You can view a summary of all states' cases in the U.S or in per state basis. The data are available for current cases and historical data for each state. For the U.S. cases in a country basis use the 'clicov summary' command instead.

To view all states' current  cases:

```
clicov usa
```

To view current cases per state:

```
clicov usa -s [state-code]

#For New York
clicov usa -s ny
```

To download all states' current cases:

```
clicov usa -sv
```

To download per state cases from day one:

```
clicov usa -s [state-code] -sv
```

## Data Providers

### Global cases

Data aggregation: https://covid19api.com/

Data source: <a href='https://github.com/CSSEGISandData/COVID-19'>the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University</a>

Term of use: https://covidtracking.com/license

### U.S. States cases

Data aggregation and providers: <a href='https://covidtracking.com/api'>the COVID Tracking Project at the Atlantic</a>

Learn more about the data here: https://covidtracking.com/data

Term of use: https://covidtracking.com/license

## License:
The app is under MIT license, meaning you are free to do however you want to the app. For the data usages, please refers to the term of use provided by the data providers.