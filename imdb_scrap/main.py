import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as Bs


def make_request(session, headers, id):
    content = session.get(f'https://www.imdb.com/title/{id}/', headers=headers)
    if content.status_code == 200:
        return content.content
    else:
        exit(0)


def parse_imdb(content):
    html = Bs(content, 'html.parser')
    js_script = html.find_all('script', attrs={'type': 'application/ld+json'})
    js_script = html.select_one('script#__NEXT_DATA__')
    data = json.loads(js_script.contents[0])
    director = ''
    country = ''
    language = ''
    actors = []
    if data.get('props').get('urqlState'):
        for digit_id in data.get('props').get('urqlState'):
            try:
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors'):
                    if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors')[
                        0].get('credits'):
                        director = \
                            data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors')[
                                0].get('credits')[0].get('name').get('nameText').get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get(
                        'countriesOfOrigin').get('countries'):
                    country = data.get('props').get('urqlState').get(digit_id).get('data').get('title').get(
                        'countriesOfOrigin').get('countries')[0].get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('spokenLanguages').get(
                        'spokenLanguages'):
                    language = data.get('props').get('urqlState').get(digit_id).get('data').get('title').get(
                        'spokenLanguages').get('spokenLanguages')[0].get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('principalCast'):
                    for i in \
                            data.get('props').get('urqlState').get(digit_id).get('data').get('title').get(
                                'principalCast')[
                                0].get('credits'):
                        actors.append(i.get('name').get('nameText').get('text'))
            except Exception:
                continue
    return country, language, director, actors


def get_all_ids():
    # df = pd.read_excel(r'data.xlsx')
    # df = df[:1000]
    # ids = df['tconst'].tolist()

    # Manual set ids
    ids = ['tt0000502', 'tt0000574', 'tt0000793', 'tt0000862']
    return ids


if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    df = pd.DataFrame(columns=['tconst', 'country', 'language', 'director', 'actors'])
    for num, id in enumerate(get_all_ids()):
        content = make_request(session, headers, id)
        try:
            country, language, director, actors = parse_imdb(content)
        except Exception:
            print('error')
            continue
        finally:
            df.to_excel('scarped_data_save.xlsx', index=False)
        df.at[num, 'tconst'] = id
        df.at[num, 'country'] = country
        df.at[num, 'language'] = language
        df.at[num, 'director'] = director
        df.at[num, 'actors'] = actors
        print(f'page {num} scarped')
    df.to_excel('scarped_data.xlsx', index=False)
