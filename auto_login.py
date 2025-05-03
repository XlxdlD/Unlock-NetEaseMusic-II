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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E3F0FF0E8E749A19D34C95D93E636CBABC8CBF23511D09A934AFDF0697907FCBAAD58E9CF12F322D2875C0CA098C8BC4FFB8177B928C8FC5AA75B55BDDFDF98CE611B32C7A66825FBE3A8AB35B253AAB3EBCA0DEBB1BC5B48FAB480C38ECF705217E2BF5F9CF9D3DC3F22326D09B9F3F20383067E0365818E6D047A340F114CEC344356836F78E74B739EA8339075D9C29C8538E04101F28BFC8974681DBBFA93258104B79B9DAE2A64B2705C27F7C0A30442BA85C8B9BF7AFF87B2057530900C018854296F8ED69744558A3E6CA89B8F41E63A2E7C5CC0F837924FB170BB87E3E7CC7E17A57E8CE4399300DD7B6DECD38BB1960BCDE4D17B67E79069BB6E6E32F6E36EB85C7FF9147A91D87B18E5B61E2FAEECCAAC08463B84004CBB8FE90D3D945CA905FCB96477ECDAAF3A8CF19FA96C64DD8196344A42A5BF2EC7ED168A2D3C05421A3F47BD826E13067A05254387E0C6A99D53809FCE58811224E3BD949"})
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
