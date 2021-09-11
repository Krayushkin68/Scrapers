from bs4 import BeautifulSoup as Bs
import requests
import json
import pandas as pd

link = r'https://www.lazada.com.ph/landmall/?q=All-Products&langFlag=en&from=wangpu&lang=en&pageTypeId=2'

r = requests.get(link)
if r.status_code != 200:
    print('error')
    exit(0)

bs2 = Bs(r.content, 'html.parser')
# with open('data/777.html', 'wb') as f:
#     f.write(r.content)

for i in bs2.select('script'):
    if i.string:
        s = i.string.strip()
        if 'window.pageData' in s:
            json_part = json.loads(s[s.find('{'): -1])
            # with open('data/json_part.json', 'wt') as f:
            #     json.dump(json_part, f)
            # print(json_part)

if json_part:
    items = json_part['mods']['listItems']
    scraped_items = []
    for i in items:
        item = {'name': '', 'image': '', 'originalPrice': '', 'price': '', 'discount': '', 'review': '',
                'ratingScore': '', 'categories': '', 'sellerName': '', 'productUrl': ''}

        if i['name']:
            item['name'] = i['name']
        if i['image']:
            item['image'] = i['image']
        if i['originalPrice']:
            item['originalPrice'] = i['originalPrice']
        if i['price']:
            item['price'] = i['price']
        if i['discount']:
            item['discount'] = i['discount']
        if i['review']:
            item['review'] = i['review']
        if i['ratingScore']:
            item['ratingScore'] = i['ratingScore']
        if i['categories']:
            item['categories'] = i['categories']
        if i['sellerName']:
            item['sellerName'] = i['sellerName']
        if i['productUrl']:
            item['productUrl'] = i['productUrl']

        scraped_items.append(item)

    df = pd.DataFrame(scraped_items)
    # df.to_excel('data/scraped_shop.xlsx')
    print(df)
