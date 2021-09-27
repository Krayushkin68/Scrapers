import requests
from bs4 import BeautifulSoup as bs

headers = {'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         r'Chrome/93.0.4577.82 Safari/537.36'}

url1 = r'https://www.funda.nl/en/koop/heel-nederland/'
url2 = r'https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=1&orderBy=relevance'
r = requests.get(url2, headers=headers)

with open('test2.html', 'wb') as f:
    f.write(r.content)

html = bs(r.content, 'html.parser')
print(html)
