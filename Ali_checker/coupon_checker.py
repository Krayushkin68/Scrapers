from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import winsound
import time
from win10toast import ToastNotifier


opts = Options()
# opts.add_argument('--headless')
opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

chrome_driver = os.getcwd() + r'\chromedriver.exe'
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)



def beep(msg):
    duration = 3000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    toaster = ToastNotifier()
    toaster.show_toast("Появился айфон", msg)


def check_exists_by_xpath(wdriver, xpath):
    try:
        wdriver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def check_ali():
    white = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[1]')
    green = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[2]')
    red = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[3]')
    blue = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[4]')
    black = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[5]')
    purple = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[6]')

    driver.find_element(By.XPATH, '//*[@id="#content"]/div[9]/div[1]/button').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys('krayuskhinml97@yandex.ru')
    driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys('Bo648562300')
    driver.find_element(By.XPATH, '//*[@id="modal-popup-zh"]/div[2]/div[2]/div/div/form/button').click()

    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="#content"]/div[9]/div[1]/button').click()
    time.sleep(3)
    price = driver.find_element(By.XPATH, '//*[@id="price-overview"]/div[1]/div/div/div[1]/div[4]/dl/dd').text
    print(f'Старая цена: {price}')
    driver.find_element(By.XPATH, '//*[@id="code"]').send_keys('WOWBUY5000')
    driver.find_element(By.XPATH, '//*[@id="price-overview"]/div[1]/div/div/div[1]/div[3]/div/form/div[2]/div/button').click()
    time.sleep(2)
    new_price = driver.find_element(By.XPATH, '//*[@id="price-overview"]/div[1]/div/div/div[1]/div[4]/dl/dd').text
    print(f'Новая цена: {price}')
    if price != new_price:
        beep('Купончик сработал')
    else:
        print('Не сработал')


if __name__ == '__main__':
    while True:
        driver.get('https://aliexpress.ru/item/1005001767088712.html?_ga=2.193159661.1907989268.1634919614-2058209869.1624122667&mp=1&sku_id=12000017492118776&spm=a2g0o.cart.0.0.30363c002s7eY1')
        check_ali()
        time.sleep(5)
    driver.close()
