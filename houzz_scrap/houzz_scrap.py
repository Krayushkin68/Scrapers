import requests
from bs4 import BeautifulSoup as Bs


def make_request(session, headers, link):
    try:
        content = session.get(link, headers=headers, timeout=5)
        if content.status_code == 200:
            pass
            # print('HTML page received')
            # with open('test.html', 'wb') as f:
            #     f.write(content.content)
        return content.content
    except Exception:
        print('connection error')
        return


def get_links_from_page(content):
    html = Bs(content, 'html.parser')
    links = []
    li = html.select('#hz-page-content-wrapper > div > main > div > div.hz-card.mbl.hz-track-me > ul > li')
    for i in range(1, len(li)+1):
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
    name = html.select('#hz-page-content-wrapper > div.sc-183mtny-0.sc-1wm9uar-0.kVLgJv.ljilJP.hui-grid > main > header > div.sc-183mtny-0.fAraQc > div.sc-183mtny-0.gamUmb > h1')
    table = html.select('#hz-page-content-wrapper > div.sc-183mtny-0.sc-1wm9uar-0.kVLgJv.ljilJP.hui-grid > div.sc-183mtny-0.sc-1uw6j8i-0.bRDPne.ecpWHO.hui-cell > div > div.sc-183mtny-0.sc-15uvirn-0.bLnFJI.eForze > div')
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


if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    content = make_request(session, headers, r'https://www.houzz.com/professionals/interior-designer/c/AK')
    links = get_links_from_page(content)

    all_info = []
    print(links)
    for i in links:
        count = 0
        while True:
            count += 1
            cont = make_request(session, headers, i)
            info = parse_page(cont)
            if info != 'reload':
                info['url'] = i
                all_info.append(info)
                # print('page done')
                break
            if count == 5:
                print('page dropped')
                break
    for i in all_info:
        print(i)
    # cont = make_request(session, headers, r'https://www.houzz.com/professionals/interior-decorators/forty-nine-interiors-pfvwus-pf~976567930')
    # parse_page(cont)
