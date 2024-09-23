from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import constants

chrome_profile_path = "C:/Users/ff/AppData/Local/Google/Chrome/User Data"

options = webdriver.ChromeOptions()

options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--user-data-dir=C:\\Users\\ff\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 13')
options.add_argument('--remote-debugging-pipe')

driver = webdriver.Chrome(options=options)

for region_code in constants.REGIONS:
  for i in range(5):
    # load page
    driver.get("https://www.listennotes.com/best-podcasts/?page={}&sort_type=listen_score&region={}".format(i+1, region_code))
    time.sleep(2)
    print('{} - page {} loaded successfully'.format(region_code, i+1))

    # find podcast cards(10 cards per page)
    cards = driver.find_elements(by=By.CLASS_NAME, value="ln-page-card")
    print(cards)


