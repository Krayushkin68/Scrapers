# import requests
import requests_html
import fake_useragent
from bs4 import BeautifulSoup as bs

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}
login_url = 'https://www.barchart.com/login'

login = 'angarragnar777@rambler.ru'
password = 'Gfhjkmangarragnar777'

payload = {'email': login,
           'password': password}

rs = requests_html.HTMLSession()
logging = rs.post(login_url, headers=headers, data=payload)

main_page = 'https://www.barchart.com/'
page = rs.get(main_page, headers=headers)
page.html.render(sleep=1, keep_page=True)

with open('test.html', 'wb') as f:
    f.write(page.content)

html = bs(page.content, 'html.parser')
tag1 = html.select('span.bc-glyph-user')
tag2 = html.select('a.bc-user-block__button')
print(tag1)
print(tag2)

