import requests
import json
import os
from bs4 import BeautifulSoup as Bs
import pandas as pd


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
url = r'https://api.masterhelp.se/api/mh?page=1&pageSize=150&position=32&region=15&siteFilter=1'

try:
    print('Start scraping...')
    r = requests.get(url, verify=False)
    if not r.status_code == 200:
        print('Error receiving information.')
        exit(0)
except Exception as e:
    print('Request error: ', e)
    exit(0)

data = json.loads(r.content.decode())
print(f'Received {len(data)} job posts, start loading descriptions...')
for num, el in enumerate(data):
    job_url_part = el['friendlyUrl']
    job_descr_url = fr'https://api.masterhelp.se/api/mh/{job_url_part}?showInactive=true'
    try:
        r = requests.get(job_descr_url)
        if not r.status_code == 200:
            print('Error receiving description information at job № ', num)
            continue
        description = json.loads(r.content.decode()).get('description')
        if description:
            data[num]['fullDescription_html'] = description.strip()
            data[num]['fullDescription_text'] = Bs(description, 'html.parser').text.strip()
            print(f'Description for job № {num+1} received.')
    except Exception as e:
        print('Request error: ', e)
        continue

if not os.path.exists('Output'):
    os.mkdir('Output')
# JSON
with open(r'Output\Jobs_info.json', 'wt', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

df = pd.DataFrame(data)
# EXCEL
df.to_excel(r'Output\Jobs_info.xlsx')
# CSV
df.to_csv(r'Output\Jobs_info.csv')

print('Scraping completed.')
input('Print ENTER to exit...')
