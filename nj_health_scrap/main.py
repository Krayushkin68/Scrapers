from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from time import sleep
from bs4 import BeautifulSoup as Bs
import pandas as pd


def make_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }
    content = requests.get(url, headers=headers)
    if content.status_code == 200:
        print('HTML page received')
        return content.content


def parse_main_page(content):
    html = Bs(content, 'html.parser')
    table = html.select('#main_table')[0]

    orgs = []
    cur_country = ''
    for row in table.select('tr'):
        if row.select('td')[0].get('class') == ['header']:
            cur_country = row.select('td')[0].text.strip()
            continue
        if row.select('td')[0].get('class') == ['black10bold']:
            continue

        try:
            org = {'Country': cur_country, 'Facility Name': '', 'URL': '', 'Street Address': '', 'City': '', 'State': '',
                   'Zip': '', 'Phone Number': '', 'Type': '', 'Medicaid?': 'No', 'Medicare?': 'No', 'Private?': 'No'}

            org['URL'] = 'https://healthapps.state.nj.us/facilities/' + row.select('td > a')[0].get('href')
            base_info = [i.strip() for i in row.select('td')[0].text.split('\n') if i.strip() != '']
            org['Facility Name'] = base_info[0]
            org['Street Address'] = base_info[1]
            org['City'] = base_info[2].split(',')[0].strip()
            org['State'] = base_info[2].split(',')[1].strip()
            org['Zip'] = base_info[3]
            org['Phone Number'] = base_info[4]
            org['Type'] = row.select('td')[1].text.strip()
            fundings = row.select('td')[2].text
            if fundings:
                if 'Medicaid' in fundings:
                    org['Medicaid?'] = 'Yes'
                if 'Medicare' in fundings:
                    org['Medicare?'] = 'Yes'
                if 'Private' in fundings:
                    org['Private?'] = 'Yes'
            orgs.append(org)
        except Exception:
            continue
    return orgs



def get_main_page():
    opts = Options()
    # opts.add_argument('--headless')
    opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    chrome_driver = os.getcwd() + r'\chromedriver.exe'
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
    driver.get(r'https://healthapps.state.nj.us/facilities/fsSetSearch.aspx?by=county')
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_0"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_1"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_2"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_3"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_4"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_5"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_6"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_cbType_8"]').click()
    driver.find_element(By.XPATH, '//*[@id="middleContent_btnGetList"]').click()
    sleep(3)
    content = driver.page_source
    driver.close()
    return content


if __name__ == '__main__':
    main_content = get_main_page()
    organizations = parse_main_page(main_content)
    df = pd.DataFrame(organizations)
    df.to_excel('data/sample.xlsx')



