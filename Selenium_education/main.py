from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as Bs
import os
import time

opts = Options()
# opts.add_argument('--headless')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

chrome_driver = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)


driver.get(os.getcwd() + '/test.html')
bs = Bs(driver.page_source, 'html.parser')
print(bs.select_one('div#test').text)
time.sleep(3)

driver.get('http://www.google.com/');
time.sleep(3)
search_box = driver.find_element_by_name('q')
search_box.send_keys('Test command for chrome')
search_box.submit()
time.sleep(3)
driver.quit()
