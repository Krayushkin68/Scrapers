from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import winsound
import time
from win10toast import ToastNotifier
import sys




def beep(msg, duration=3000):
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
    white = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[1]').get_attribute("class")
    green = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[2]').get_attribute("class")
    # red = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[3]')
    blue = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[4]').get_attribute("class")
    black = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[5]').get_attribute("class")
    purple = driver.find_element(By.XPATH, '//*[@id="#content"]/div[6]/div[2]/div[6]').get_attribute("class")

    flag = [1 for i in [white, green, blue, purple] if 'active' in i]
    if flag:
        if 'active' in white:
            beep('Белый')
            print('white')
        if 'active' in green:
            beep('Зеленый')
            print('green')
        if 'active' in blue:
            beep('Синий')
            print('blue')
        if 'active' in purple:
            beep('Фиолетовый')
            print('purple')
        if 'active' in black:
            beep('Черный',1000)
            print('black')
    else:
        print('Не появилось')


if __name__ == '__main__':
    while True:
        opts = Options()
        opts.add_argument('--headless')
        opts.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        chrome_driver = os.getcwd() + r'\chromedriver.exe'
        driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)
        driver.get(
            'https://aliexpress.ru/item/1005001767088712.html?_ga=2.193159661.1907989268.1634919614-2058209869.1624122667&mp=1&sku_id=12000017492118776&spm=a2g0o.cart.0.0.30363c002s7eY1')

        k = 0
        try:
            while True:
                k += 1
                print(f'Проверка № {k}')
                check_ali()
                driver.refresh()
                time.sleep(20)
        except Exception:
            print('Ошибка')
            continue
        except KeyboardInterrupt:
            print('Interrupted')
            driver.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
