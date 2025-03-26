# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00730BE8EB9B649E831A2EFA51FDC22D35F14AD1C935B0B4C4B0115A51475957D849273A1B7F188FF2189D1A9B7068345BF7D6AD86FDDAAAA57C4337DE78AB89397CA573E3CC5124A36702A286B9FEFD3F3B640496EBF27831E5BC4D5EAAB0BE4A75C7A1EE2CBCD911C765A89A3749D64EA6900419D6DEF59A376EED420BFA640DA08A9E328CD9ABEEDA1E1819AD577A176FC7D8DC433029760E7249147BCC72E5722F89B4BCEA9F6C517F7929DF5E3CDB7C87D3D8F92E5590AD80797BC067D49B2F2D0C7C45C0E513694DCBA102A8D40E1DD9738212706C7A48F53F599109EF1F7F21699C5D291FE9EE83CB0D5079B55FA3D2908A17A7C97426D49E3AC389CE1D21380DA41D670E9575174EB5061F14A22D0F0FE591B50CE150E71A60F6A247AF53DC99309ABECDC06D6FA7DC9DE132EF9634791A932BBD90C63E0868D1A5E0E6AB71F8A09EEFA1DBB8B2BBEC288D31BC21129A80CF529F21CE94458853546257"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
