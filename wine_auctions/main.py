import re

import requests
from bs4 import BeautifulSoup as Bs


def get_bottle_sizes(url):
    r = requests.get(url)
    bs = Bs(r.content, 'html.parser')
    rows = bs.select('tr')
    regex = re.compile(r"\d+ x ([a-z\d. ]+?) (Mc|d')?[A-Z\d.' ]{2,}.*")
    sizes = set()
    for row in rows:
        if row.select('p.category.barial') and row.select('p.category.barial')[0].text == 'PRODUCTS/ACCESSORIES':
            break
        if row.get('class') in [['valign', 'bggrey'], ['valign']]:
            item = row.select('td')[1].text.strip()
            if item:
                match = regex.match(item)
                if match:
                    sizes.add(match.group(1))
    return sizes


def start_scraper(base_url):
    try:
        r = requests.get(base_url)
        if r.status_code != 200:
            print('Error recieving main auctions page')
            return False
    except requests.ConnectionError as e:
        print(f'Connection error: {e}')
        return False
    bs = Bs(r.content, 'html.parser')
    links = [r'https://www.oddbins.com.au' + a.get('href') for a in bs.select('a.downlistclass') if a.get('href')]
    print(f'Found {len(links)} auctions')
    sizes = set()
    for num, link in enumerate(links):
        print(f'Scraping auction {num + 1}/{len(links)}')
        try:
            sizes.update(get_bottle_sizes(link))
        except Exception:
            print(f'Error scraping auction {num + 1}/{len(links)}')
            continue
    return sizes


if __name__ == '__main__':
    bottle_sizes = start_scraper(base_url='https://www.oddbins.com.au/home/auctions')
    if bottle_sizes:
        with open('bottle_sizes.txt', 'wt') as f:
            f.write('\n'.join(bottle_sizes))
        print('Bottle sizes are loaded in the "bottle_sizes.txt"')
    input('Press Enter to exit...')
