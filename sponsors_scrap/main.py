import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs

link = r'https://sponsors.channelpartnersconference.com/products-and-services.php'

r = requests.get(link)
if r.status_code != 200:
    print('error')
    exit(0)

bs = Bs(r.content, 'html.parser')

bs_sponsors = bs.select('div.col-md-2.text-align')
print(len(bs_sponsors))
sponsors = []
for s in bs_sponsors:
    sponsor = {"name": '', 'description': '', 'services': [], 'products': [], 'links': []}
    if s.select('a.turnbuckle_plus'):
        sponsor['name'] = s.select('a.turnbuckle_plus')[1].text
    if s.select('div > p'):
        sponsor['description'] = s.select('div > p')[0].text
    if s.select('ul'):
        if s.select('ul')[0].select('li'):
            [sponsor['services'].append(b.text.strip()) for b in s.select('ul')[0].select('li')]
        if len(s.select('ul')) > 1:
            if s.select('ul')[1].select('li'):
                [sponsor['products'].append(b.text.strip()) for b in s.select('ul')[1].select('li')]
    [sponsor['links'].append(l.get('href')) for l in s.select('p>a')]
    sponsors.append(sponsor)

[print(s) for s in sponsors]
df = pd.DataFrame(sponsors)
df.to_excel('data/test.xlsx')
