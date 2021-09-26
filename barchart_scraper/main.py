import requests
import requests_html
import fake_useragent
from bs4 import BeautifulSoup as bs

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}
login_url = 'https://www.barchart.com/login'

login = 'angarragnar777@rambler.ru'
password = 'Gfhjkmangarragnar777'

# rs = requests.Session()
rs = requests_html.HTMLSession()
login_page = rs.get(login_url, headers=headers)
print('Login page code ', login_page.status_code)

login_html = bs(login_page.content, 'html.parser')
token = login_html.select('input[name="_token"]')[0].get('value')
print('Token: ', token)

payload = {'_token': token,
           'email': login,
           'password': password,
           'remember': 'on'}

logging = rs.post(login_url, headers=headers, data=payload)
print('Logging code ', logging.status_code)
# rs.get(login_url, headers=headers)

page_url = 'https://www.barchart.com/options/most-active/stocks?orderBy=optionsTotalVolume&orderDir=desc'
page = rs.get(page_url, headers=headers)
print('Main page code ', page.status_code)

# page.html.render(sleep=1, keep_page=True)

html = bs(page.content, 'html.parser')
print(html)

# request_url = 'https://www.barchart.com/proxies/core-api/v1/quotes/get?list=options.mostActive.us&fields=symbol%2CsymbolType%2CsymbolName%2ChasOptions%2ClastPrice%2CpriceChange%2CpercentChange%2CoptionsImpliedVolatilityRank1y%2CoptionsTotalVolume%2CoptionsPutVolumePercent%2CoptionsCallVolumePercent%2CoptionsPutCallVolumeRatio%2CtradeTime%2CsymbolCode&orderBy=optionsTotalVolume&orderDir=desc&between(lastPrice%2C.10%2C)=&between(tradeTime%2C2021-09-24%2C2021-09-27)=&meta=field.shortName%2Cfield.type%2Cfield.description&hasOptions=true&page=1&limit=100&raw=1'
# request = rs.get(request_url, headers=headers)


