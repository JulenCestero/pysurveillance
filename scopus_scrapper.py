import csv
import json
import re
import time

import pandas as pd
import progressbar
import requests
import streamlit as st
from bs4 import BeautifulSoup

with open('config.json', 'r') as f:
    API_KEY = json.load(f)
url = 'https://api.elsevier.com/content/search/scopus'
q = '"inverse reinforcement learning"  AND  ( "system"  OR  "e-learning"  OR  "stochastic"  OR  "smart grids"  OR  "control"  OR  "system controller"  OR  "control tuning"  OR  "optimization")'
scimago_url = 'https://www.scimagojr.com/journalrank.php'


class scopus_df:
    def __init__(self):
        self.columns = ['Authors', 'Title', 'Year', 'Cited by', 'Affiliations', 'Author Keywords', 'Source title']
        self.csv = pd.DataFrame(columns=self.columns)

    def get_authors(self, publication: dict) -> list:
        return [author['authname'] for author in publication['author']]

    def get_affiliations(self, publication: dict) -> list:
        return [aff['affilname'].replace(',', ';') for aff in publication['affiliation']]

    def append(self, publication: dict) -> None:
        try:
            authors = ','.join(self.get_authors(publication))
            title = publication['dc:title']
            year = re.findall(r'([\d]{4})', publication['prism:coverDisplayDate'])[0]
        except Exception as e:
            return None
        try:
            source_title = publication['prism:publicationName']
        except KeyError as e:
            source_title = ''
        try:
            cites = publication['citedby-count']
        except KeyError as e:
            cites = 0
        try:
            affiliations = ','.join(self.get_affiliations(publication))
        except KeyError as e:
            affiliations = ''
        try:
            author_kw = ','.join([ii.lstrip().strip() for ii in publication['authkeywords'].split('|')])
        except KeyError as e:
            author_kw = ''
        self.csv = self.csv.append(
            pd.DataFrame([[authors, title, year, cites, affiliations, author_kw, source_title]], columns=self.columns),
            ignore_index=True)


def query_to_scopus(url: str, query: str, api: str, start_item: int = 0) -> list:
    return requests.get(url,
                        headers={'Accept': 'application/json', 'X-ELS-APIKey': api},
                        params={'query': query, 'view': 'COMPLETE', 'start': start_item}).json()


def get_years_scimago():
    years = []
    r = requests.get(scimago_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    test = soup.find_all('div', class_='dropdown').__getitem__(4)
    for li in test.contents.__getitem__(3).findAll('li'):
        years.append(li.text)
    return years


def download_scimago_data(years: list):
    ##for year in years:
    year = 2018
    scimago_url = 'https://www.scimagojr.com/journalrank.php?year=%s&out=xls' % year
    response = requests.get(scimago_url).content
    open('scimago/%s.csv' % year, 'wb').write(response)
    print(year)


def process_scimago_file(file: str, journal: str):
    try:
        with open('scimago/%s.csv' % file) as f:
            r = csv.reader(f, delimiter=';')
            for row in r:
                if journal in row[2]:
                    return row[18]
    except:
        return None


def create_df_from_scopus(url: str, query: str, api: str, num_items: int) -> pd.DataFrame():
    assert num_items > 0
    start_item = 0
    publications = scopus_df()
    with progressbar.ProgressBar(max_value=num_items) as bar:
        while start_item < num_items:
            response = query_to_scopus(url, query, api, start_item)
            try:
                batch = response['search-results']['entry']
            except KeyError as e:
                break
            for item in batch:
                publications.append(item)
                start_item += 1
                bar.update(start_item)
    return publications.csv


@st.cache
def check_query(query: str = q) -> int:
    query_parsed = f'{query}'  # TODO: Save a history of all the querys with the number of results
    api = API_KEY['api-key']
    return int(query_to_scopus(url, query_parsed, api)['search-results']['opensearch:totalResults'])


@st.cache
def get_csv(num_items: int, query: str = q) -> pd.DataFrame():
    query_parsed = f'{query}'
    api = API_KEY['api-key']
    return create_df_from_scopus(url, query_parsed, api, num_items)


def main():
    query = input('Introduce query: ')
    num_items = check_query(query)
    action = input(f'The query returned {num_items} results. Do you want to continue? [y/n] ')
    if 'y' in action or 'Y' in action:
        csv = get_csv(num_items, query)
        ts = int(time.time())
        csv.to_csv(f'sample_data/{ts}.csv')
        print(f'Data saved to {ts}.csv')
    else:
        print('Aborting...')


if __name__ == '__main__':
    main()
