import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

url = r'https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=10'
r = requests.get(url, verify=False)

soup = bs(r.content, 'html.parser')

rows = []
for el in soup.select('table')[0].select('tr'):
    tds = el.select('td')
    if tds:
        row = {'date': '', 'title': '', 'link': ''}
        row['date'] = tds[0].text
        row['title'] = tds[1].select_one('a').text
        row['link'] = tds[1].select_one('a').get('href')
        rows.append(row)

[print(i) for i in rows]

df = pd.DataFrame(rows)

needed_page = 2
payload = {'nextValue': str(needed_page),
           'next': 'n',
           'search': None,
           'fromDate': None,
           'toDate': None,
           'fromYear': None,
           'toYear': None,
           'deptId': '-1',
           'sid': '3',
           'ssid': '15',
           'smid': '10',
           'intmid': '-1',
           'sText': 'Filings',
           'ssText': 'Public Issues',
           'smText': 'Draft Offer Documents filed with SEBI',
           'doDirect': str(needed_page)}

p = requests.post(f'https://www.sebi.gov.in/sebiweb/ajax/home/getnewslistinfo.jsp', verify=False, data=payload)
