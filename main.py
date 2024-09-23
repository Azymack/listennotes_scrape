from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

import constants
import utils

os.system("taskkill /f /im chrome.exe")

# Chrome profile path
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--user-data-dir=C:\\Users\\ff\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 13')

# Create a new Chrome session
driver = webdriver.Chrome(options=options)

try:
    for region_code in constants.REGIONS:
        for i in range(5):
            try:
                # Load page
                url = f"https://www.listennotes.com/best-podcasts/?page={i+1}&sort_type=listen_score&region={region_code}"
                driver.get(url)
                time.sleep(2)
                print(f'{region_code} - page {i+1} loaded successfully')

                # Find podcast cards (10 cards per page)
                cards = driver.find_elements(By.CLASS_NAME, "ln-page-card")
                for card_div in cards:
                    card_info = utils.get_initial_info(card_div)
                    if card_info is not None:
                        utils.write_initial_info_into_json(region_code, card_info)
                    else:
                        pass

            except Exception as e:
                print(f'Error loading page {i+1} for region {region_code}: {e}')
finally:
    driver.quit()