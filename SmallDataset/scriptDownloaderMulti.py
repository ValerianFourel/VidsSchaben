import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import os
import time
import json

#Custom_Downloads_dir
base_download_dir = "/home/vfourel/ProjectGym/SmallDataset/DownloadsVideos"

# Json File for the smallDataset
json_file_path = "/home/vfourel/ProjectGym/SmallDataset/Minutes_matchingVideosReduced.json"

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for video_info in data.items():
        print(video_info)
        subject_name = video_info[1].get('subject_name')
        webpage_url = video_info[1].get('webpage_url')
        video_id = video_info[0]
        if subject_name and webpage_url:
            yield video_id, subject_name, webpage_url
        else:
            print(f"Skipping incomplete entry for video ID: {video_id}")


# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the GeckoDriver path
geckodriver_path = "/usr/local/bin/geckodriver"  # Replace with the actual path to geckodriver

# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")  # Run in headless mode (optional)
firefox_options.log.level = "trace"  # Enable verbose logging

# Set up the Firefox service
firefox_service = FirefoxService(executable_path=geckodriver_path)

try:
    for video_id, subject_name, webpage_url in process_json_file(json_file_path):
        string_to_send = webpage_url # "https://www.youtube.com/watch?v=jEF-u4ntt2Q"
        # Create a subfolder for the current subject_name
        subject_download_dir = os.path.join(base_download_dir, subject_name)
        os.makedirs(subject_download_dir, exist_ok=True)

        # Update Firefox preferences for the current subject
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.dir", subject_download_dir)
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel,application/x-gzip")

        logging.info(f"Processing: Video ID: {video_id}, Subject: {subject_name}, URL: {webpage_url}")
        logging.info(f"Download directory set to: {subject_download_dir}")

        # Create a new driver instance with updated preferences
        logging.info("Initializing WebDriver")
        print('Initializing WebDriver')
        driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
 #       if 'driver' in locals():
#            driver.quit()
        logging.info("Navigating to webpage")
        print('Navigating to webpage')
        driver.get("https://cobalt.tools/")

        logging.info("Waiting for input area")
        print('Waiting for input area')
        input_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "link-area"))
    )
        input_area.send_keys(string_to_send)
        logging.info("Waiting for 5 seconds")
        time.sleep(5)

        logging.info("Locating and clicking the download button")
        print("Locating and clicking the download button")
        download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button"))
    )
        download_button.click()
        logging.info("Waiting for 10 seconds after clicking the download button")
        time.sleep(10)
        if 'driver' in locals():
            driver.quit()

    logging.info("Script execution completed")
    print("Script execution completed")

except WebDriverException as e:
    logging.error(f"WebDriver error occurred: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    logging.info("Closing WebDriver")
    if 'driver' in locals():
        driver.quit()
