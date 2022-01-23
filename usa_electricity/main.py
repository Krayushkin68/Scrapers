import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs


def make_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    content = requests.get(url, headers=headers)
    if content.status_code == 200:
        print('HTML page received')
        return content.content


if __name__ == '__main__':
    j = json.load(open('states.json', 'rt'))
    states = j['states']
    cities = j['Alabama']
    info = []
    for c in cities:
        url = f'https://www.electricitylocal.com/states/alabama/{c.lower()}/'
        content = make_request(url)
        if content:
            bs = Bs(content, 'html.parser')
            res = {'city': c, 'state': 'Alabama', 'commercial': '', 'residential': '', 'industrial': ''}
            res['commercial'] = bs.select('ul.no2 > li')[0].select('strong')[0].text[:-6]
            res['residential'] = bs.select('ul.no2 > li')[3].select('strong')[0].text[:-6]
            res['industrial'] = bs.select('ul.no2 > li')[6].select('strong')[0].text[:-6]
            info.append(res)
    df = pd.DataFrame(info)
    df.to_csv('data/info.csv')
