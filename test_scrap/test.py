import requests
from bs4 import BeautifulSoup as Bs


def make_request(link):
    try:
        cont = requests.get(link)
        if cont.status_code == 200:
            return cont.content
    except Exception:
        print('connection error')
        return


def parse_page(data):
    html = Bs(data, 'html.parser')
    models = [i.select('a') for i in html.select('div.category-box')]
    models = [[i[0].text.strip(), i[0].get('href')] for i in models]
    print(models)

if __name__ == '__main__':
    content = make_request('https://www.maxtondesign.co.uk/body-kits/kia-motors')
    if content:
        parse_page(content)


