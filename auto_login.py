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
    browser.add_cookie({"name": "MUSIC_U", "value": "00774484CCFB969345EB4199053B05848CE22926822E525C881672D7E2D32E72F18E07E3A3F21E29106BB502EF1B89B1815A60EA7EA068202A4472FE292D7A61FCB897AE34C11A3E9D2B5D6E15592A4C8B80960F3366950CE7B59CEF9DD44F70F5B3E606FD21C13887ADECB68E9B93E8F57879B59B98F162CCEDE9F9024D2E944D9F2B7A7DA7D62F66967057CB7CE42BAFE937CE8681D219D8422E7786324547129322F3CD709AD2C81E790A5DC2F55C1E748609299AB9D6B07F8480130B15A19633E6002CE1DBFFE7B140A1E6358CF725142FF77DBD9CF9EB29F8E1440E84619A6740C9C73C7018C13D50A9A281B775E7ED2854A40B3636C6D59EA0BB4CEB0AB4D1117341E64B9FD9372FE8D4E1B9B708E481B03C840F25DD281907449D3853DA3C417AAF65AE13EA535A51360E5753A0A43C21670FC3C274C6A7982C78BB82979BF18FC0759BDECB542E3B8787487CFB126D46A86B9E924BB44D21B052E49DBF"})
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
