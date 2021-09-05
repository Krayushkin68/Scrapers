import requests
from bs4 import BeautifulSoup as Bs
import json
import re
import pandas as pd


def make_request(session, headers, id):
    content = session.get(f'https://www.imdb.com/title/{id}/', headers=headers)
    if content.status_code == 200:
        pass
        # print('HTML page received')
        # with open('test.html', 'wb') as f:
        #     f.write(content.content)
    return content.content


def parse_imdb(content):
    html = Bs(content, 'html.parser')
    js_script = html.find_all('script', attrs={'type': 'application/ld+json'})
    js_script = html.select_one('script#__NEXT_DATA__')
    data = json.loads(js_script.contents[0])
    # with open('data.json', 'wt') as f:
    #     json.dump(data, f)
    # for i in data.get('props').get('urqlState'):
    #     if data.get('props').get('urqlState').get(i).get('data').get('title'):
    #         if i.startswith('15'):
    #             digit_id = i
            # if data.get('props').get('urqlState').get(i).get('data').get('title').get('spokenLanguages'):
            #     digit_id = i
    director =''
    country = ''
    language = ''
    actors = []
    if data.get('props').get('urqlState'):
        for digit_id in data.get('props').get('urqlState'):
            try:
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors'):
                    if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors')[0].get('credits'):
                        director = data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('directors')[0].get('credits')[0].get('name').get('nameText').get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('countriesOfOrigin').get('countries'):
                    country = data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('countriesOfOrigin').get('countries')[0].get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('spokenLanguages').get('spokenLanguages'):
                    language = data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('spokenLanguages').get('spokenLanguages')[0].get('text')
                if data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('principalCast'):
                    for i in data.get('props').get('urqlState').get(digit_id).get('data').get('title').get('principalCast')[0].get('credits'):
                        actors.append(i.get('name').get('nameText').get('text'))
            except Exception:
                continue
    return country, language, director, actors


def get_all_ids():
    # df = pd.read_excel(r'data.xlsx')
    # df = df[:1000]
    # ids = df['tconst'].tolist()
    
    # ids = ['tt0000502', 'tt0000574', 'tt0000591', 'tt0000615', 'tt0000630', 'tt0000675', 'tt0000679', 'tt0000739', 'tt0000793', 'tt0000862']
    ids = ['tt0000502', 'tt0000574', 'tt0000793', 'tt0000862']
    return ids


if __name__ == '__main__':
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    df = pd.DataFrame(columns= ['tconst', 'country', 'language', 'director', 'actors'])
    for num, id in enumerate(get_all_ids()):
        content = make_request(session, headers, id)
        try:
            country, language, director, actors = parse_imdb(content)
        except Exception:
            print('error')
            continue
        finally:
            df.to_excel('scarped_data_save.xlsx', index=False)
        # row = {'tconst': id, 'country': country, 'language': language, 'director': director, 'actors': actors}
        df.at[num, 'tconst'] = id
        df.at[num, 'country'] = country
        df.at[num, 'language'] = language
        df.at[num, 'director'] = director
        df.at[num, 'actors'] = actors
        # df.append(row, ignore_index=True)
        print(f'page {num} scarped')
    df.to_excel('scarped_data.xlsx', index=False)


    # content, session = make_request()
    # parse_imdb(content)
