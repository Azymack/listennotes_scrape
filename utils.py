from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import json
import os

def get_initial_info(card_div):
    try:
        # Locate the header div and title in one go
        title_div = card_div.find_element(By.CSS_SELECTOR, ".flex.items-center h2")
        tag_div_arr = card_div.find_elements(By.CSS_SELECTOR, ".flex.items-center .flex-none div")
        by_div = card_div.find_element(By.CSS_SELECTOR, "a.ml-1.text-black.inline")
        contact_div = card_div.find_element(By.CSS_SELECTOR, ".flex.items-center.mt-2")
        email = contact_div.find_elements(By.TAG_NAME, "a")[3].get_attribute("href")
        # Get the title text and URL
        title_text = title_div.text
        title_url = title_div.find_element(By.TAG_NAME, "a").get_attribute("href")
        tag_1 = tag_div_arr[0].text
        tag_2 = tag_div_arr[2].text
        by = by_div.text
        email = email.replace("mailto:", "")
        
        return {"title": title_text, "url": title_url, "tag_1": tag_1,  "tag_2": tag_2, "by": by, "email": email}
    except (IndexError, NoSuchElementException):
        return None

def get_hosts(url):
    pass

def write_initial_info_into_json(region, info):
    # Specify the paths for JSON and Excel files
    json_file_path = "result/{}.json".format(region)
    excel_file_path = "result/{}.xlsx".format(region)

    # Ensure the 'result' directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # Read existing data
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist, start with an empty list
        data = []

    # Append the new data
    data.append({
        "title": info["title"],
        "url": info["url"],
        "LS": info["tag_1"],
        "rank": info["tag_2"],
        "By": info["by"],
        "email": info["email"],
        "hosts": ""
    })

    # Write updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=2)

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(data)
    df.to_excel(excel_file_path, index=False)
