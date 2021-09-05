import requests
from bs4 import BeautifulSoup as Bs
import json


def get_price(coin):
    r = requests.get(f'https://coinmarketcap.com/currencies/{coin}/')
    html = Bs(r.content, 'html.parser')
    coin_json = json.loads(html.find('script', attrs={'type': 'application/ld+json'}).contents[0])
    name = coin_json['name']
    price = coin_json['currentExchangeRate']['price']
    return name, price


if __name__ == '__main__':
    btc_name, btc_price = get_price('bitcoin')
    print(f'{btc_name}: {btc_price}')
    ltc_name, ltc_price = get_price('litecoin')
    print(f'{ltc_name}: {ltc_price}')
    input("\nPress enter to close program")
