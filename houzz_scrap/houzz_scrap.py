import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs


def make_request(session, headers, link):
    try:
        content = session.get(link, headers=headers, timeout=5)
        if content.status_code == 200:
            return content.content
    except Exception:
        print('connection error')
        return False


def get_links_from_main_page(content):
    html = Bs(content, 'html.parser')
    links = []
    li = html.select('#hz-page-content-wrapper > div > main > div > div.hz-card.mbl.hz-track-me > ul > li')
    for i in range(1, len(li) + 1):
        a = html.select(
            f'#hz-page-content-wrapper > div > main > div > div.hz-card.mbl.hz-track-me > ul > li:nth-child({i}) >'
            ' div.hz-pro-search-result > div.hz-pro-search-result__info > div.hz-pro-search-result__left-info.clearfix > '
            'div.hz-pro-profile-info-rating.clearfix > a')
        if a:
            links.append(a[0].attrs.get('href'))
    return links


def parse_page(content):
    html = Bs(content, 'html.parser')
    name = ''
    city = ''
    foll = ''
    name = html.select(
        '#hz-page-content-wrapper > div.sc-183mtny-0.sc-1wm9uar-0.kVLgJv.ljilJP.hui-grid > main > header > div.sc-183mtny-0.fAraQc > div.sc-183mtny-0.gamUmb > h1')
    table = html.select(
        '#hz-page-content-wrapper > div.sc-183mtny-0.sc-1wm9uar-0.kVLgJv.ljilJP.hui-grid > div.sc-183mtny-0.sc-1uw6j8i-0.bRDPne.ecpWHO.hui-cell > div > div.sc-183mtny-0.sc-15uvirn-0.bLnFJI.eForze > div')
    for i in table:
        search = i.select('span.mwxddt-0.IconRow___StyledText-sc-1f6s35j-1.hgfkgN.bkjkrD > span')
        if search:
            if search[0].select('a'):
                foll = search[0].select('a')
            else:
                city = search
    if name:
        name = name[0].contents[0]
    if city:
        city = city[0].contents[0]
    if foll:
        foll = foll[0].contents[0]
    if not city and not foll:
        print('reload')
        return 'reload'
    info = {'name': name, 'city': city, 'url': '', 'foll': foll}
    return info


def get_info_from_main_page(content):
    html = Bs(content, 'html.parser')
    script = html.select('script#hz-ctx')
    if script:
        script = json.loads(script[0].text)
        shops = script['data']['stores']['data']['ProfessionalStore']['data']
        users = script['data']['stores']['data']['UserStore']['data']
        users = [(str(i['userId']), i['displayName']) for i in users.values()]

        shops_data = []
        for k in users:
            if shops.get(k[0]):
                shop = {'name': '', 'phone': '', 'address': ''}
                shop['name'] = k[1]
                if shops[k[0]].get('formattedPhone'):
                    shop['phone'] = shops[k[0]].get('formattedPhone')
                if shops[k[0]].get('location') or shops[k[0]].get('address'):
                    if shops[k[0]].get('location') and shops[k[0]].get('address'):
                        shop['address'] = shops[k[0]].get('address') + ', ' + shops[k[0]].get('location')
                    elif shops[k[0]].get('location'):
                        shop['address'] = shops[k[0]].get('location')
                    elif shops[k[0]].get('address'):
                        shop['address'] = shops[k[0]].get('address')
                shops_data.append(shop)

    [print(i) for i in shops_data]
    return shops_data


def parse_page_new(content):
    html = Bs(content, 'html.parser')
    script = html.find('script', attrs={'type': 'application/ld+json'})
    script = json.loads(script.text)

    if len(script) > 0:
        shop = {'name': '', 'phone': '', 'url': '', 'address': ''}
        shop['name'] = script[0].get('name')
        shop['phone'] = script[0].get('telephone')
        shop['url'] = script[0].get('url')
        address = script[0].get('address')
        if address:
            address = [address[i] for i in address.keys() if not i.startswith('@') and isinstance(address[i], str)]
            address = [i for i in address if i != '']
            address = ', '.join(address)
            shop['address'] = address
        return shop
    else:
        return 'reload'


def process_links_from_main_page(main_page_content):
    links = get_links_from_main_page(main_page_content)

    all_info = []
    for i in links:
        count = 0
        while True:
            count += 1
            cont = make_request(session, headers, i)
            if cont:
                info = parse_page_new(cont)
                if info != 'reload':
                    info['platform_url'] = i
                    all_info.append(info)
                    # print('page done')
                    break
                if count == 5:
                    print('page dropped')
                    break
    return all_info


if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    url = r'https://www.houzz.com/professionals/cabinets/c/New-York--NY'
    cont = make_request(session, headers, url)
    info = process_links_from_main_page(cont)

    for i in range(1, 4):
        print(f'Start processing page {i}')
        url = url + f'/p/{i * 15}'
        cont = make_request(session, headers, url)
        if cont:
            print(f'Received page {i}')
            info.extend(process_links_from_main_page(cont))
            print(f'Scraped page {i}')

    df = pd.DataFrame(info)
    df.to_excel('test.xlsx')
