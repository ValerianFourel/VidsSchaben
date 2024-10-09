import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import os
import time

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the Firefox profile
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.download.folderList", 2)
firefox_profile.set_preference("browser.download.dir", "/home/vfourel/ProjectGym")
firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
firefox_profile.set_preference("media.play-stand-alone", False)

# Set up the GeckoDriver path
geckodriver_path = "/usr/local/bin/geckodriver"

# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.log.level = "trace"

# Set up the Firefox service
firefox_service = FirefoxService(executable_path=geckodriver_path)

def check_download_status(driver, timeout=60):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".download-complete"))
        )
        logging.info("Download completed successfully")
        return True
    except TimeoutException:
        logging.warning("Download did not complete within the expected time")
        return False

try:
    logging.info("Initializing WebDriver")
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options, firefox_profile=firefox_profile)

    logging.info("Navigating to webpage")
    driver.get("https://cobalt.tools/")

    logging.info("Waiting for input area")
    input_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "link-area"))
    )

    logging.info("Sending string to input area")
    string_to_send = "https://www.youtube.com/watch?v=NqvooBJ8FY8"
    input_area.send_keys(string_to_send)

    logging.info("Waiting for 5 seconds")
    time.sleep(5)

    logging.info("Locating and clicking the download button")
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button"))
    )
    download_button.click()

    logging.info("Button clicked, checking download status")
    if check_download_status(driver):
        logging.info("Download completed successfully")
    else:
        logging.warning("Download may not have completed or encountered issues")

    # Check if the file exists in the download directory
    expected_file_path = os.path.join("/home/vfourel/ProjectGym", "video.mp4")
    if os.path.exists(expected_file_path):
        logging.info(f"File downloaded successfully: {expected_file_path}")
    else:
        logging.warning(f"File not found in the expected location: {expected_file_path}")

    logging.info("Script execution completed")

except WebDriverException as e:
    logging.error(f"WebDriver error occurred: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    logging.info("Closing WebDriver")
    if 'driver' in locals():
        driver.quit()
