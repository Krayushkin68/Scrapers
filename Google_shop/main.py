import os
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

opts = Options()
# opts.add_argument('--headless')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

chrome_driver = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

driver.get('https://shopping.google.com/')
search = 'Jacket'
driver.find_element(By.XPATH, '//*[@id="REsRA"]').send_keys(search)
driver.find_element(By.XPATH, '//*[@id="REsRA"]').send_keys(Keys.RETURN)

with open('data/test.html', 'wb') as f:
    f.write(driver.page_source.encode())
html = bs(driver.page_source, 'html.parser')
items = html.select('div.sh-dgr__content')
if items:
    for i in items:
        print(i.select_one('h4').text)

time.sleep(5)
driver.quit()
