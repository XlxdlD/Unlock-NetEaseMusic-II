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
    browser.add_cookie({"name": "MUSIC_U", "value": "00215E9F92E46801B2CAEE6A4B22C930828759C63B97EDF0C1614111173E3BDD1FE35B8C6521A0D3F517CD913887E27D30236D2BF429609FE3BA629D059B007DDB2D8D2C08F525668E06FB232E201B6AE7E20D2088A2C64D3B5BA0C9769486E0AB7049F7885100F3D69092B9CDA7E4FB53C2D8CF3FE4F11F5FFF3269235B23A0378441022AC37FBBE7B0B0751F3A9706DA83E290E953D8E5668BFAE8509F32FDC18928F1CE08E8B2C55D2300CFFC7470392081413069F3CB731201D277D63E24DCA907490677E6BB95806B5AB3070E67F60863E428ECE43670FD5DE274B01B458E7ECE36F209712C6ADAB9C554E50C74CD4CED7515A4D6A255CD7FD01BEA32DA2B42DE66FF6BA050A055A80AFBED5C241C004CDE015FB56CB69EC6C3FADB2827993E09B2A175DAC2AACE6D1A72FB565146750BBF6B0C3CF5DD4BD9AEC0C85F75742654C35282902AB813C27AB29B3B077A55EC56C345B34027676CB1F4A4BE052E"})
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
