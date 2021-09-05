from bs4 import BeautifulSoup as Bs
from Offer import *
from sqlite import *


def parse_html(content):
    html = Bs(content, 'html.parser')
    offers_html = html.select('div.items-items-kAJAg>div')
    offers = []
    for i in offers_html:
        try:
            o = Offer()
            # Забираем название из заголовка ссылки, отделяем только нужную инфу
            o.name = i.select_one('div > a > h3').text
            # Оттуда же берем ссылку
            link = i.select_one('div>a').attrs['href']
            o.link = f'https://www.avito.ru{link}'
            # Достаем описание
            if i.select_one('div.iva-item-descriptionStep-QGE8Y'):
                o.description = i.select_one('div.iva-item-descriptionStep-QGE8Y>div').text
            # Цена
            price = i.select_one('div>div.iva-item-priceStep-QN8Kl').select('meta')[1].attrs['content']
            if price in ['None', '...']:
                o.price = 'NULL'
            else:
                o.price = int(price)
            # Достаем все ссылки из тегов img и еще из слайдера пробуем забрать
            images = set()
            for j in i.select('div>img'):
                images.add(j.attrs['src'])
            if i.select_one('li.photo-slider-list-item-_fUPr'):
                images.add(i.select_one('li.photo-slider-list-item-_fUPr').attrs['data-marker'][19:])
            o.photo = list(images)
            # Берем текст из местоположения
            if i.select_one('span.geo-icons-gKaD_'):
                o.geo = i.select_one('span.geo-icons-gKaD_').parent.text
            o.time = i.find(attrs={'data-marker': 'item-date'}).text
            # Добавляем готовое объявление в список
            offers.append(o)
        except Exception:
            continue
    print(f'Found {len(offers)} offers')
    return offers


def parse_html_json(content):
    html = Bs(content, 'html.parser')
    try:
        html.select_one('div.js-initial').attrs['data-state']
    except Exception:
        print('No json part here...\nTry scarping html...')
        return parse_html(content)
    avito_json = json.loads(html.select_one('div.js-initial').attrs['data-state'])
    offers_html = avito_json['catalog']['items']
    offers = []
    for i in offers_html:
        if i['type'] == 'item':
            try:
                o = Offer()
                o.name = i['title']
                link = i['urlPath']
                o.link = f'https://www.avito.ru{link}'
                o.description = i['description']
                price = str(i['priceDetailed']['value'])
                if price in ['None', '...']:
                    o.price = 'NULL'
                else:
                    o.price = int(price)
                o.photo = list(i['gallery']['image_large_urls'].values())
                o.geo = str(i['addressDetailed']['locationName']) + ' ' + str(i['geo']['geoReferences'][0]['content'])\
                        + str(i['geo']['geoReferences'][0].get('after'))
                o.time = i['iva']['DateInfoStep'][0]['payload']['absolute']
                offers.append(o)
            except Exception:
                continue
    print(f'Found {len(offers)} offers')
    return offers


if __name__ == '__main__':
    con = sql_connection()
    offers = select_offers(con)
    con.close()
