import json
import os
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs


def get_page_data(link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
    r = requests.get(link, headers=headers)
    if r.status_code != 200:
        print('Connection error')
        return None
    else:
        print('HTML page received')
        return r.content


def scrape_products_info(content):
    bs2 = Bs(content, 'html.parser')
    json_part = None
    for i in bs2.select('script'):
        if i.string:
            s = i.string.strip()
            if 'window.pageData' in s:
                json_part = json.loads(s[s.find('{'): -1])

    if json_part:
        trigger_next = True
        if json_part['mainInfo'].get('pageSize') and json_part['mainInfo'].get('page') \
                and json_part['mainInfo'].get('totalResults'):
            if int(json_part['mainInfo']['pageSize']) * int(json_part['mainInfo']['page']) > \
                    int(json_part['mainInfo']['totalResults']):
                trigger_next = False

        items = json_part['mods']['listItems']
        scraped_items = []
        for i in items:
            item = {'name': '', 'image': '', 'originalPrice': '', 'price': '', 'discount': '', 'review': '',
                    'ratingScore': '', 'sellerName': '', 'productUrl': ''}
            if i.get('name'):
                item['name'] = i['name']
            if i.get('image'):
                item['image'] = i['image']
            if i.get('originalPrice'):
                item['originalPrice'] = i['originalPrice']
            if i.get('price'):
                item['price'] = i['price']
            if i.get('discount'):
                item['discount'] = i['discount']
            if i.get('review'):
                item['review'] = i['review']
            if i.get('ratingScore'):
                item['ratingScore'] = i['ratingScore']
            if i.get('sellerName'):
                item['sellerName'] = i['sellerName']
            if i.get('productUrl'):
                item['productUrl'] = i['productUrl']
            scraped_items.append(item)
        return scraped_items, trigger_next
    else:
        print('No json part here')
        return None


def srape_until_result(link):
    try_count = 5
    sleep_time = 4
    while try_count:
        print(f'Try № {6 - try_count}')
        page_content = get_page_data(link)
        if page_content:
            res = scrape_products_info(page_content)
            if res:
                return pd.DataFrame(res[0]), res[1]
        try_count -= 1
        sleep(sleep_time)
    return None


def scrape_all_pages(main_link, start_page):
    res_df = pd.DataFrame(columns=['name', 'image', 'originalPrice', 'price', 'discount', 'review',
                                   'ratingScore', 'sellerName', 'productUrl'])

    page_num = start_page
    continue_scrap = True

    while continue_scrap:
        print(f'\nScraping page № {page_num}')
        link = main_link + f'&page={page_num}'
        res = srape_until_result(link)
        if res:
            res_df = pd.concat([res_df, res[0]], axis=0).reset_index(drop=True)
            print(f'Page № {page_num} scrapped succesfull')
            continue_scrap = res[1]
            page_num += 1
        else:
            print(f'Error scraping page № {page_num}')
            break
    print('Finished scraping')
    return res_df


def download_main_images(items, path):
    if not os.path.exists(path):
        os.mkdir(path)
    img_count = len(items['image'])
    for num, i in enumerate(items['image']):
        try:
            form = i[i.rfind('.'):]
            filename = f"{path}\\{num}{form}"
            img = requests.get(i)
            if img.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img.content)
                    print(f'Image № {num + 1} / {img_count} downloaded')
        except Exception:
            print(f'Image № {num + 1} / {img_count} passed')
            continue


if __name__ == '__main__':
    url = input('Input link to sellers products page.\n'
                '(it should look like that: https://www.lazada.com.ph/landmall/?q=All-Products&langFlag=en&'
                'from=wangpu&lang=en&pageTypeId=2)\nYour url: ')

    products = scrape_all_pages(url.strip(), start_page=1)

    if isinstance(products, type(pd.DataFrame())):
        if not os.path.exists('data'):
            os.mkdir('data')
        products.to_excel(r'data\General_product_info.xlsx')
        download_main_images(products, 'data\\images')

    input('\nPress Enter for exit ...')
