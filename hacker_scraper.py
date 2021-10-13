import csv
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import sqlite3
from pprint import pprint
"""
run interactively with python3 -i new_scraper.py to 
play around with the code
"""
URL = 'https://news.ycombinator.com/'
page_counter = 1
PAGE_MAX = 1
NA = 'N/A'


def get_page_html(URL):
    """
    get page from URL
    """
    res = requests.get(URL)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup


def extract_data(page_html):
    [tr for tr in page_html.find_all('tr')]


def extract_data(html):
    """ 
    extract html from data 
    """
    data = {
        'titles': [],
        'authors': [],
        'scores': [],
        'timestamps': []
    }

    for post in html.find_all('tr', {'class': 'athing'}):

        title = post.find('a', {'class': 'storylink'})
        if title:
            data['titles'].append(title.get_text())

    for post in html.findAll('td', {'class': 'subtext'}):
        author = post.find('a', {'class': 'hnuser'})
        if author:
            data['authors'].append(author.get_text())
        else:
            data['authors'].append(NA)

        score = post.find('span', {'class': 'score'})
        if score:
            data['scores'].append(score.get_text().split()[0].strip())
        else:
            data['scores'].append(NA)

        timestamp = post.find('span', {'class': 'age'}).get(
            'title', 'no timestamp')
        if timestamp:
            data['timestamps'].append(timestamp)

    data = list(
        zip(data['titles'],
            data['authors'],
            data['scores'],
            data['timestamps']))
    return data


def populate_db(data, output_file='quote_list.csv', db='hn_articles.db'):
    """ 
    populate DB
    """

    df = pd.DataFrame(data, columns=['title', 'author', 'score', 'timestamp'])
    df.to_csv(output_file)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    df.to_sql('hacker_news_posts', conn, if_exists='append', index=True)

    print(c.execute('select * from hacker_news_posts').fetchall())

    c.close()
    conn.close()


def main():
    data = extract_data(get_page_html(URL))
    populate_db(data)


if __name__ == '__main__':
    main()
