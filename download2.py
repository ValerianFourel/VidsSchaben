import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-data-dir=/home/vfourel/.config/google-chrome")
#chrome_options.add_argument('--profile-directory=\'Profile 3\'')
chrome_options.add_argument('--profile-directory=Default')

# Set download directory
download_dir = "~/ProjectGym/SmallDataset/DownloadsVideos"  # Replace with your desired download directory
#chrome_options.add_experimental_option("prefs", {
#    "download.default_directory": download_dir,
#    "download.prompt_for_download": False,
#    "download.directory_upgrade": True,
#    "safebrowsing.enabled": True
# })

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())

def accept_cookies(driver):
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
        )
        logger.info("Cookie consent dialog found.")
        cookie_button.click()
        logger.info("Accepted cookies.")
    except (TimeoutException, NoSuchElementException):
        logger.info("No cookie consent dialog found or it's not clickable.")

try:
    logger.info("Starting Chrome WebDriver...")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)

    # First, handle Google cookies
    logger.info("Navigating to Google...")
    driver.get("https://www.google.com")
    accept_cookies(driver)

    # Now proceed with video download
    logger.info("Navigating to cobalt.tools...")
    driver.get("https://cobalt.tools/")

    logger.info("Waiting for input area")
    input_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "link-area"))
    )

    logger.info("Sending YouTube URL to input area")
    youtube_url = "https://www.youtube.com/watch?v=NqvooBJ8FY8"
    input_area.send_keys(youtube_url)

    logger.info("Waiting for 5 seconds")
    time.sleep(5)

    logger.info("Locating and clicking the download button")
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button"))
    )
    download_button.click()

    logger.info("Waiting for 10 seconds after clicking the download button")
    time.sleep(10)

    logger.info("Script execution completed")

except WebDriverException as e:
    logger.error(f"WebDriver error occurred: {e}")
except Exception as e:
    logger.error(f"An error occurred: {e}")
    if 'driver' in locals():
        screenshot_path = "error_screenshot.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved to {screenshot_path}")
finally:
    logger.info("Closing WebDriver")
    if 'driver' in locals():
        driver.quit()
