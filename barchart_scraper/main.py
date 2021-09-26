import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
login_url = 'https://www.barchart.com/login'

login = 'angarragnar777@rambler.ru'
password = 'Gfhjkmangarragnar777'

payload = {'refcode': None,
           'remember': True,
           'email': login,
           'password': password}

rs = requests.Session()
login_resp = rs.get(login_url, headers=headers)

loged_page = rs.post(login_url, headers=headers, data=payload)

needed_url = 'https://www.barchart.com/options/most-active/stocks?orderBy=optionsTotalVolume&orderDir=desc'
needed_page = rs.get(needed_url, headers=headers)


download_url = 'https://www.barchart.com/my/download'
download_url = rs.post(download_url, headers=headers)




