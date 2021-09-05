# https://slco.org/assessor/new/valuationInfoExpanded.cfm?parcel_id=16292010070000
import requests
from bs4 import BeautifulSoup as Bs
from lxml import etree
import json
import re
import pandas as pd


def make_request(session, headers):
    content = session.get(r'https://slco.org/assessor/new/valuationInfoExpanded.cfm?parcel_id=16292010070000', headers=headers)
    if content.status_code == 200:
        print('HTML page received')
        with open('test2.html', 'wb') as f:
            f.write(content.content)
    return content.content


def parse_salt(content):
    html = Bs(content, 'html.parser')
    name = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(1) > td')[0].contents[0]
    address = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(2) > td')[0].contents[0]
    total_acreage = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(3) > td > a')[0].contents[0]
    above_grade = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(4) > td > a')[0].contents[0]
    type1 = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(5) > td')[0].contents[0]
    type2 = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(5) > td > a')[0].contents[0]
    tax = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(6) > td > a')[0].contents[0]
    land_val = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(7) > td')[0].contents[0]
    build_val = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(8) > td')[0].contents[0]
    market_val = html.select('#parcelFieldNames > div.valueSummBox > div > table > tbody > tr:nth-child(9) > td')[0].contents[0]
    print(f'name: {name}')
    print(f'address: {address}')
    print(f'total_acreage: {total_acreage}')
    print(f'above_grade: {above_grade}')
    print(f'type: {type1+type2}')
    print(f'tax: {tax}')
    print(f'land_val: {land_val}')
    print(f'build_val: {build_val}')
    print(f'market_val: {market_val}')

if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    content = make_request(session, headers)
    parse_salt(content)