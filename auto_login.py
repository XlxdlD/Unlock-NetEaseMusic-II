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
    browser.add_cookie({"name": "MUSIC_U", "value": "00064CB01EDA82D9B37DDC3584C7E154E2A48ABB86F5EDDB2E039BBEB5738BC3BBAFD54108F1FEAFEAF7A8555C0B1E611617783C8EAB858012E86F47D6D48693ACC9C56233E1DB8D80A0FD7D62CC298210C77038B6B8FC6A0BF24E43CFEE2044666EFE13944748FCEFD5651F752943CE3BCDF6B61A9DE8185DBFFA3846F210D4B1BF54E0B66CCBB2DE9F3F995AE3C925188990E35BE8D5D8DBBB5AA1495BFEC8E6D99D9E80248D47CCD3D007F2B7E6D9B7F81664ED3ACA67C93CE2CF8E9D99060D2A618243AA6A6256C6CBD202F3A618CDAC8FAA5E0F92A31EF6A4D8BF4391043D2A8720A05D9492B8C5B6CE1AA76001CCA8C67CE4A3648E89F6FD6E17190E0F642F2593C9B082F4ADE0697F454A8C027FC82F5AE3008050223DF4196DA2B7328BCD0F782C9FE5918882178B2F9440F0AC193D53B73F79D8A4EAB8870AC797204E40A8B9DB31E5895DC62B8BBF3DF40702C29A38F6AC692D06CF6BA068A1B05304"})
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
