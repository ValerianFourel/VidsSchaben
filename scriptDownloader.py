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

# Set up logging
logging.basicConfig(level=logging.INFO)


# Set up the Firefox profile
firefox_profile = webdriver.FirefoxProfile()
# Set download directory path
firefox_profile.set_preference("browser.download.folderList", 2)  # 2 means custom directory
firefox_profile.set_preference("browser.download.dir", "/home/vfourel/ProjectGym")
# Add .mp4 MIME type to download preferences
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
firefox_profile.set_preference("media.play-stand-alone", False)


# Set up the GeckoDriver path
geckodriver_path = "/usr/local/bin/geckodriver"  # Replace with the actual path to geckodriver

# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")  # Run in headless mode (optional)
firefox_options.log.level = "trace"  # Enable verbose logging

# Set up the Firefox service
firefox_service = FirefoxService(executable_path=geckodriver_path)

try:
    logging.info("Initializing WebDriver")
    print('Initializing WebDriver')
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options, firefox_profile = firefox_profile)

    logging.info("Navigating to webpage")
    print('Navigating to webpage')
    driver.get("https://cobalt.tools/")

    logging.info("Waiting for input area")
    print('Waiting for input area')
    input_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "link-area"))
    )

    logging.info("Sending string to input area")
    print("Sending string to input area")
    string_to_send ="https://www.youtube.com/watch?v=NqvooBJ8FY8" #  "https://www.youtube.com/watch?v=jEF-u4ntt2Q"
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
