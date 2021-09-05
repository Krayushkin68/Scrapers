import requests
from html_parse import parse_html_json
from sqlite import *


def make_request():
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    city = 'moskva'
    category = 'tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw'
    page = '?p=<номер>'
    content = session.get(f'https://www.avito.ru/{city}/{category}', headers=headers, timeout=5)
    if content.status_code == 200:
        print('HTML page received')
    else:
        print('Connection aborted')
        exit(0)
    return content.content, session


if __name__ == '__main__':
    content, session = make_request()
    offers = parse_html_json(content)
    con = sql_connection()
    insert_offers(con, offers)
    con.close()
    session.close()
