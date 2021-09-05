from bs4 import BeautifulSoup as Bs
import re
from Offer import *
from sqlite import *


def parse_html(content):
    html = Bs(content, 'html.parser')
    offers_html = html.select('div.iva-item-content-m2FiN')
    offers = []
    for i in offers_html:
        try:
            o = Offer()
            # Забираем название из заголовка ссылки, отделяем только нужную инфу
            name = i.select_one('div>a').attrs['title']
            o.name = re.search('«(.*)»', name)[1]
            # Оттуда же берем ссылку
            link = i.select_one('div>a').attrs['href']
            o.link = f'https://www.avito.ru{link}'
            # Достаем описание
            if i.select_one('div.iva-item-descriptionStep-3i2NN'):
                o.description = i.select_one('div.iva-item-descriptionStep-3i2NN').text
            # Цена
            price = i.select_one('div>div.iva-item-priceStep-2qRpg').select('meta')[1].attrs['content']
            if price in ['None', '...']:
                o.price = 'NULL'
            else:
                o.price = int(price)
            # Достаем все ссылки из тегов img и еще из слайдера пробуем забрать
            images = set()
            for j in i.select('div>img'):
                images.add(j.attrs['src'])
            if i.select_one('li.photo-slider-list-item-35GzI'):
                images.add(i.select_one('li.photo-slider-list-item-35GzI').attrs['data-marker'][19:])
            o.photo = list(images)
            # Берем текст из местоположения
            if i.select_one('span.geo-icons-agBYC'):
                o.geo = i.select_one('span.geo-icons-agBYC').parent.text
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
        with open('777.html', 'wb') as f:
            f.write(content)
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
                # o.photo = list(i['gallery']['image_urls'].values())
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
    # with open('test_materials/111.html', 'rb') as f:
    #     cont = f.read()
    # # offers = parse_html(cont)
    # offers = parse_html_json(cont)
    # print(offers[0].name, offers[0].description, offers[0].price, offers[0].photo,offers[0].link, offers[0].geo, offers[0].time)
    # offers_str = str()
    # for num, k in enumerate(offers):
    #     offers_str = offers_str + f'{num+1}. {k.__str__()}\n'
    #     print(f'{num+1}. {k}')


# ----------------------------------------- Выгрузка из SQL --------------------------------------
    con = sql_connection()
    offers = select_offers(con)
    # for i in offers:
    #     i.download_image()
    print(len(offers))
    con.close()
# --------------------------------------------------------------------------------------------------

# (1, 'Nvidia RTX 3080 Ti Founders Edition', None, 159900, 'https://56.img.avito.st/208x156/11538759456.jpg https://67.img.avito.st/208x156/11538759467.jpg ', 'https://www.avito.ru/moskva/tovary_dlya_kompyutera/nvidia_rtx_3080_ti_founders_edition_2207181381', 'Москва Беляево 700\xa0м', '25 июля 16:48')
# Nvidia RTX 3080 Ti Founders Edition None 159900 ['https://56.img.avito.st/208x156/11538759456.jpg', 'https://67.img.avito.st/208x156/11538759467.jpg'] https://www.avito.ru/moskva/tovary_dlya_kompyutera/nvidia_rtx_3080_ti_founders_edition_2207181381 Москва Беляево 700 м 25 июля 16:48

# ----------------------------------------- Запись в txt файл --------------------------------------
#     with open('offers.txt', 'wb') as f:
#         f.write(offers_str.encode())
# --------------------------------------------------------------------------------------------------

# ----------------------------------------- Загрузка в SQL -----------------------------------------
#     con = sql_connection()
#     # drop_table(con)  # для теста
#     # create_table(con)
#     insert_offers(con, offers)
#     con.close()
# --------------------------------------------------------------------------------------------------

# ----------------------------------------- Парсинг json раздела страницы --------------------------
# avito_json = json.loads(html.select_one('div.js-initial').attrs['data-state'])
# offers_html = avito_json['catalog']['items']
# avito_json['catalog']['items'][1]['urlPath']
# avito_json['catalog']['items'][1]['title']
# avito_json['catalog']['items'][1]['description']
# avito_json['catalog']['items'][1]['priceDetailed']['value']
# avito_json['catalog']['items'][1]['addressDetailed']['locationName']
# avito_json['catalog']['items'][1]['geo']['geoReferences'][0]['content']
# avito_json['catalog']['items'][1]['geo']['geoReferences'][0]['after']

# def get_img(num, avito_json):
#     img = set()
#     for i in avito_json['catalog']['items'][num]['images']:
#         for j in i.values():
#             img.add(j)
#     return list(img)

# list(avito_json['catalog']['items'][2]['gallery']['image_urls'].values())
# list(avito_json['catalog']['items'][2]['gallery']['image_large_urls'].values())

# avito_json['catalog']['items'][2]['iva']['DateInfoStep'][0]['payload']['absolute']
# avito_json['catalog']['items'][2]['iva']['DateInfoStep'][0]['payload']['relative']
# --------------------------------------------------------------------------------------------------
