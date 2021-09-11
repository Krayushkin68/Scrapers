from bs4 import BeautifulSoup as Bs
import requests
import re

link = r'https://trackapkg.com/a.duiepyle-tracking-number#couriers'

r = requests.get(link)
if r.status_code != 200:
    print('error')
    exit(0)

bs = Bs(r.content, 'html.parser')

links_carrier = []
for i in bs.select('div.bottom-links.container > div.col-xs-12.col-md-3'):
    for j in i.select('a'):
        links_carrier.append('https://trackapkg.com/' + j.get('href'))
        print('https://trackapkg.com/' + j.get('href'))


carriers = []
for num, link in enumerate(links_carrier):
    r = requests.get(link)
    if r.status_code != 200:
        print(f'error srap page {num+1}')
        exit(0)

    bs = Bs(r.content, 'html.parser')
    carrier = {'name': '', 'link': ''}
    if bs.select_one('h1.newtitle'):
        carrier['name'] = bs.select_one('h1.newtitle').text
    if bs.select_one('form.form-buscar'):
        if bs.select_one('form.form-buscar').has_attr('action'):
            carrier['link'] = bs.select_one('form.form-buscar').get('action')
        elif bs.select_one('input#run'):
            onclick = bs.select_one('input#run').get('onclick')
            carrier['link'] = re.match("window.open\('(.*)',.*", onclick).group(1)

    print(carrier)
    carriers.append(carrier)

