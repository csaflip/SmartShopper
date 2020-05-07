from selenium import webdriver
import bs4 as bs
import re
from re import sub
import time
from decimal import Decimal
import json


def load_config():
    with open('config.json', 'r') as infile:
        data = json.load(infile)
    return data


def get_page_source(url):
    browser = webdriver.Firefox()

    browser.get(url)

    time.sleep(1)

    html = browser.page_source

    browser.close()

    return html


def find_matches(patterns, names):
    matched_names = []
    for name in names:
        for pattern in patterns:
            if re.search(pattern, name.text, re.IGNORECASE) is not None:
                matched_names.append(name.text + " " + name['href'])
    return matched_names


def find_ebay_matches(patterns, names):
    matched_names = []

    for name in names:
        price = name.parent.parent.find('span', {'class': 's-item__price'})
        price = Decimal(sub(r'[^\d.]', '', price.text))

        for pattern in patterns:
            if re.search(pattern, name.text, re.IGNORECASE) is not None:
                matched_names.append((price, name.text + " " + name.parent['href']))

    matched_names = sorted(matched_names, key=lambda x: x[0])  # sort by key (price)
    return matched_names


def search_craigslist(config_data):
    for url in config_data['cl_urls']:
        soup = bs.BeautifulSoup(get_page_source(url), features='html5lib')

        cl_names = soup.findAll('a', {'class': "result-title hdrlnk"})

        cl_patterns = config_data['cl_patterns']

        craigslist_matches = find_matches(cl_patterns, cl_names)
        for match in craigslist_matches:
            print(match)
        print('------------------------------------------------')


def search_ebay(config_data):
    for url in config_data['ebay_urls']:
        soup = bs.BeautifulSoup(get_page_source(url), features='html5lib')

        ebay_names = soup.findAll('h3', {'class': "s-item__title"})

        ebay_patterns = config_data['ebay_patterns']

        ebay_matches = find_ebay_matches(ebay_patterns, ebay_names)

        for match in ebay_matches:
            print("$" + str(match[0]) + ": " + match[1])
        print('----------------------------------------------------')




