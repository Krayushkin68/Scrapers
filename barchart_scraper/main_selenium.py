from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os

login = 'angarragnar777@rambler.ru'
password = 'Gfhjkmangarragnar777'

opts = Options()
# opts.add_argument('--headless')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

chrome_driver = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)


def check_exists_by_xpath(wdriver, xpath):
    try:
        wdriver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

driver.get('https://www.barchart.com/login')
driver.find_element(By.XPATH, '//*[@id="bc-main-content-wrapper"]/div/div[2]/div[2]/div/div/div/div[1]/form/div[1]/input').send_keys(login)
driver.find_element(By.XPATH, '//*[@id="login-page-form-password"]').send_keys(password)
driver.find_element(By.XPATH, '//*[@id="bc-main-content-wrapper"]/div/div[2]/div[2]/div/div/div/div[1]/form/div[6]/button').click()

driver.get('https://www.barchart.com/options/most-active/stocks?orderBy=optionsTotalVolume&orderDir=desc')
driver.find_element(By.XPATH, '//*[@id="main-content-column"]/div/div[5]/div[2]/div[2]/a[3]').click()
