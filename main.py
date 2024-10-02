import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import random

import constants
import utils

def setup_driver():
    """Set up the Chrome driver with the specified profile."""
    os.system("taskkill /f /im chrome.exe")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--user-data-dir=C:\\Users\\ff\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument('--profile-directory=Profile 13')
    
    return webdriver.Chrome(options=options)

def load_podcast_data_for_region(driver, region_code):
    """Load podcast data for a specific region and save to JSON."""
    initial_url = f"https://www.listennotes.com/best-podcasts/?page=1&sort_type=listen_score&region={region_code}"
    driver.get(initial_url)
    num_page_div = driver.find_element(By.CSS_SELECTOR, ".flex-1.flex.flex-wrap.items-center.text-sm.text-helper-color")
    num_pages = int(num_page_div.find_elements(By.TAG_NAME, "div")[0].text.replace("Page 1 of", "").replace("podcasts", ""))
    num_pages = num_pages // 10 + 1
    print("number of pages", num_pages)
    for i in range(num_pages):
        try:
            # Load page
            url = f"https://www.listennotes.com/best-podcasts/?page={i+1}&sort_type=listen_score&region={region_code}"
            # time.sleep(random.uniform(10, 15))
            driver.get(url)
            time.sleep(random.uniform(5, 15))
            print(f'{region_code} - page {i + 1} loaded successfully')

            # Find podcast cards (10 cards per page)
            cards = driver.find_elements(By.CLASS_NAME, "ln-page-card")
            for card_div in cards:
                card_info = utils.get_initial_info(card_div)
                if card_info is not None:
                    utils.write_initial_info_into_json(region_code, card_info)

        except Exception as e:
            print(f'Error loading page {i + 1} for region {region_code}: {e}')

def update_hosts_in_json(driver, region_code):
    """Update the hosts field in the JSON for a given region."""
    json_file_path = f'result/{region_code}.json'
    xlsx_file_path = f'result/{region_code}.xlsx'

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # Read the JSON file into a DataFrame
        df = pd.read_json(json_file_path)
        url_arr = df['url'].tolist()

        # Loop through each URL
        for index, url in enumerate(url_arr):
            try:
                driver.get(url)
                time.sleep(2)  # Wait for the page to load
                print('Page loaded successfully {}'.format(index))

                # Find host info
                host_arr = [host_div.text for host_div in driver.find_elements(By.CSS_SELECTOR, ".pr-3.text-sm.font-semibold.whitespace-nowrap.mb-2")]
                print(host_arr)
                # Update the 'hosts' field in the DataFrame
                df.at[index, 'hosts'] = ', '.join(host_arr)  # Join hosts into a single string

            except Exception as e:
                print(f'Error loading page: {e}')

        # Save the updated DataFrame back to the JSON file
        df.to_json(json_file_path, orient='records', lines=True, indent=2)
        df.to_excel(xlsx_file_path)
    else:
        print("JSON file does not exist.")

def main():
    """Main function to run the web scraping and data updating process."""
    driver = setup_driver()
    try:
        for region_code in constants.REGIONS:
            load_podcast_data_for_region(driver, region_code)  # Load data first
            # update_hosts_in_json(driver, region_code)  # Update hosts after loading data

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
