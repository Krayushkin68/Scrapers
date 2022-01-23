import os
import re
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
# opts.add_argument('--headless')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

chrome_driver = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

driver.get('https://tinyhabits.com/')
time.sleep(5)

regex = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'

html = bs(driver.page_source, 'html.parser')

urls = [i.get('href') for i in html.select('a') if i.get('href')]
urls = [i for i in urls if re.match(regex, i)]

[print(i) for i in urls]
driver.quit()
