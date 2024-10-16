import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import time
import json

# Json File for the smallDataset
json_file_path = "/home/vfourel/ProjectGym/SmallDataset/Minutes_matchingVideosReduced.json"

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for video_info in data.items():
        video_id = video_info[0]
        subject_name = video_info[1].get('subject_name')
        webpage_url = video_info[1].get('webpage_url')
        if subject_name and webpage_url:
            yield video_id, subject_name, webpage_url
        else:
            print(f"Skipping incomplete entry for video ID: {video_id}")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the GeckoDriver path
geckodriver_path = "/usr/local/bin/geckodriver"

# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.log.level = "trace"

# Set up the Firefox service
firefox_service = FirefoxService(executable_path=geckodriver_path)

try:
    # Create a single driver instance
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

    for video_id, subject_name, webpage_url in process_json_file(json_file_path):
        logging.info(f"Processing: Video ID: {video_id}, Subject: {subject_name}, URL: {webpage_url}")

        driver.get("https://cobalt.tools/")

        input_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "link-area"))
        )
        assert input_area.is_enabled(), "Input area is not enabled"
        input_area.clear()  # Clear any previous input
        input_area.send_keys(webpage_url)
        
        logging.info("Waiting for 5 seconds")
        time.sleep(5)

        logging.info("Locating and clicking the download button")
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "download-button"))
        )
        assert download_button.is_displayed(), "Download button is not visible"
        download_button.click()
        
        logging.info("Waiting for 10 seconds after clicking the download button")
        time.sleep(10)

    logging.info("Script execution completed")

except WebDriverException as e:
    logging.error(f"WebDriver error occurred: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    logging.info("Closing WebDriver")
    if 'driver' in locals():
        driver.quit()
