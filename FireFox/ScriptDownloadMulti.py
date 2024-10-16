import os
import time
import logging
import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import torch
from torchvision import models, transforms
import cv2
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import time
from paligemma import PaliGemma
from datetime import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize the PaliGemma model
model = PaliGemma()
text_prompt = "Give me only the 4 characters"

# Path to the JSON file
file_path = '/home/vfourel/ProjectGym/SmallDataset/Minutes_matchingVideosTest.json'

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

base_download_dir="/home/vfourel/ProjectGym/FireFox/DownloadedOutput"

# Set up logging
logging.basicConfig(level=logging.INFO)

# This needs to run only once to load the model into memory

def check_value_above_400(driver):
    """
    Function to check if the value in the specified span is above 400.

    Args:
    driver: Selenium WebDriver instance
    url: URL of the page to check

    Returns:
    bool: True if value is 400 or above, False otherwise
    """
    try:

        # Wait for the result div to be present in the DOM
        result_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sf_result"))
        )

        # Find the span inside the div with class "def-btn-name"
        span_element = result_div.find_element(By.CSS_SELECTOR, ".def-btn-name span")

        # Get the text content of the span
        span_value = span_element.text.strip()

        # Try to convert the value to a number
        try:
            numeric_value = float(span_value)
            is_above_400 = numeric_value >= 400
            print(f"Value found: {numeric_value}, Is above or equal to 400: {is_above_400}")
            return is_above_400
        except ValueError:
            print(f"Unable to convert span value '{span_value}' to a number")
            return False

    except TimeoutException:
        print("Timed out waiting for element to be present")
        return False
    except NoSuchElementException:
        print("Could not find the specified element")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False




def check_and_process_captcha(driver, model):
    try:
        # Wait for up to 10 seconds for the element to be present
        main_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "output-captcha-dialog"))
        )

        # If the element is found, process the captcha
        process_captcha(driver, model)

    except TimeoutException:
        # If the element is not found within 10 seconds, this block will execute
        print("Captcha dialog not found. Continuing without processing captcha.")


def getDownload(driver):
    """
    Function to get the first download link within the specified div.

    Args:
    driver: Selenium WebDriver instance
    url: URL of the page containing the download link

    Returns:
    str: URL of the download link if found, None otherwise
    """
    try:

        # Wait for the result div to be present in the DOM
        result_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sf_result"))
        )

        # Find the first 'a' link inside the div with class "def-btn-box"
        download_link = result_div.find_element(By.CSS_SELECTOR, ".def-btn-box a")
        download_link.click()

        return download_link

    except TimeoutException:
        print("Timed out waiting for element to be present")
        return None
    except NoSuchElementException:
        print("Could not find the specified element")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def PopUpLargeVideos(driver):
    """
    Function to interact with the video download popup.

    Args:
    driver: Selenium WebDriver instance

    Returns:
    bool: True if successful, False otherwise
    """
    print("PopUpLargeVideos")
    try:
        # Wait for the popup to be present in the DOM
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "c-ui-popup"))
        )
        print("Popup found")
        capture_screenshot(driver)

                # Once popup is present, wait for the download button to be present within the popup
        download_button = WebDriverWait(popup, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-ui-download-button"))
        )
        print("Download button found")
            # Find the download button within the popup
        # download_button = popup.find_element(By.CLASS_NAME, "c-ui-download-button")

            # Click the download button
        download_button.click()
        capture_screenshot(driver)

        print("Download button clicked successfully!")

            # Wait for the close button to be clickable
        close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "c-ui-popup-btn-close"))
            )

            # Click the close button
        close_button.click()
        print("Close button clicked successfully!")

    except TimeoutException:
        print("Timed out waiting for popup to be present")
        capture_screenshot(driver)

        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def capture_screenshot(driver):
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Define screenshot path
    screenshot_dir = 'tmpImages'
    screenshot_filename = f'tmp-{timestamp}.png'
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    # Ensure the directory exists
    os.makedirs(screenshot_dir, exist_ok=True)

    # Capture and save the screenshot
    driver.save_screenshot(screenshot_path)

    print(f"Screenshot saved: {screenshot_path}")

    return screenshot_path



def process_screenshot(driver):
    # Take the screenshot
    screenshot_path = capture_screenshot(driver)

    # Open the screenshot for editing
    img = Image.open(screenshot_path)

    # Get the width and height of the image
    width, height = img.size

    # Calculate the coordinates of the middle rectangle in a 3 by 3 grid
    left = width / 3
    top = height / 3
    right = 2 * (width / 3)
    bottom = height / 2  # Adjust to get the upper half of the middle rectangle

    # Crop the image
    img_cropped = img.crop((left, top, right, bottom))

    # Save the cropped image as a JPG file
    if img_cropped.mode == 'RGBA':
        img_cropped = img_cropped.convert('RGB')
    img_cropped.save(screenshot_path)
    
    # Load the image
    img = cv2.imread(screenshot_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(max(contours, key = cv2.contourArea))

    # Crop the original image using the coordinates of the bounding box
    crop_img = img[y:y+h, x:x+w]
    
    # Save the cropped image as a JPG file
    cv2.imwrite(screenshot_path, crop_img)

    return screenshot_path


def check_and_rename_mp4_files(directory, timestamp,id):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.mp4'):
            file_path = os.path.join(directory, filename)
            file_creation_time = os.path.getctime(file_path)
            
            if file_creation_time > timestamp:
                # File was created after the specified timestamp
                new_filename = f"{id}.mp4"
                new_file_path = os.path.join(directory, new_filename)
                
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")

def setup_firefox_webdriver(download_dir="/home/vfourel/ProjectGym/FireFox/DownloadedOutput", geckodriver_path="/usr/local/bin/geckodriver"):
    # Set up the Firefox profile
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)  # 2 means custom directory
    firefox_profile.set_preference("browser.download.dir", download_dir)
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
    firefox_profile.set_preference("media.play-stand-alone", False)

    # Set up Firefox options
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.log.level = "trace"  # Enable verbose logging

    # Set up the Firefox service
    firefox_service = FirefoxService(executable_path=geckodriver_path)

    try:
        logging.info("Initializing WebDriver")
        print('Initializing WebDriver')
        driver = webdriver.Firefox(
            service=firefox_service,
            options=firefox_options,
            firefox_profile=firefox_profile
        )
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {str(e)}")
        print(f"Failed to initialize WebDriver: {str(e)}")
        return None


def process_captcha(driver, model, text_prompt= text_prompt):
    # Process screenshot and run model
    screenshot_path = process_screenshot(driver)
    max_attempts = 5

    # Wait for the main div to be present
    main_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "output-captcha-dialog"))
    )

    # Get all elements inside main_div
    all_elements = main_div.find_elements(By.XPATH, ".//*")
    print(f"Total elements found inside main_div: {len(all_elements)}")

    # Get all direct child div elements of main_div
    child_divs = main_div.find_elements(By.XPATH, "./div")
    print(f"Number of direct child div elements: {len(child_divs)}")

    # Print information about each child div
    for index, div in enumerate(child_divs, start=1):
        div_class = div.get_attribute("class")
        div_text = div.text.strip() if div.text else "No text"
        print(f"\nChild Div {index}:")
        print(f"  Class: {div_class or 'No class'}")
        print(f"  Text: {div_text}")

    # Get the second child div
    second_child_div = main_div.find_elements(By.XPATH, "./div")[1]
    print("Second Child Div:")
    print(f"  Class: {second_child_div.get_attribute('class')}")

    # Find the form within the second child div
    form = second_child_div.find_element(By.TAG_NAME, "form")

    # Find the input field
    input_field = form.find_element(By.CSS_SELECTOR, "div.captcha-dialog__input__ctr > input[type='text'][name='val']")

    # Input the text
    attempt = 0
    text = model.run(text_prompt, screenshot_path).replace(" ", "")
    print("We get: ", text)
    input_field.send_keys(text)

    # Find and click the submit button
    submit_button = form.find_element(By.CSS_SELECTOR, "button.captcha-dialog__button[type='submit']")
    
    submit_button.click()
    time.sleep(3)
            # Check if the CAPTCHA dialog is still present
    while attempt < max_attempts:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "output-captcha-dialog"))
            )
            # If we reach here, the CAPTCHA dialog is still present, so we need to retry
            print("CAPTCHA not solved. Retrying...")
            text_prompt_revised = f"{text} is not correct. {text_prompt}"
            attempt += 1
            text = model.run(text_prompt_revised, screenshot_path).replace(" ", "")
            print("We get: ", text)
            input_field.send_keys(text)

            # Find and click the submit button
            submit_button = form.find_element(By.CSS_SELECTOR, "button.captcha-dialog__button[type='submit']")
            
            submit_button.click()
        except TimeoutException:
            # If we reach here, the CAPTCHA dialog is no longer present, indicating success
            print("CAPTCHA solved successfully!")
            return True



# Get the start time of the loop
start_time = time.time()
print(f"Loop start time: {start_time}")

# Dictionary to store WebDriver instances for each subject
subject_drivers = {}

totalDuration = 0
totalDurationGoal = 0

# Set to keep track of unique subject names
unique_subjects = set()
try:

# Iterate through the dictionary
    for key, value in data.items():
        # Assuming the 'subject_name' is a field in your JSON data
        #subject_name = value.get('subject_name')
        if 'subject_name' in value:
            unique_subjects.add(value['subject_name'])

        # Calculate total duration goal
        totalDurationGoal += float(value.get('duration', 0))
    print("totalDurationGoal: ",totalDurationGoal)
    # Get the first 5 unique subject names (or all if there are fewer than 5)
    first_5_subjects = list(unique_subjects)[:5]

    for subject_name in first_5_subjects:
        subject_download_dir = os.path.join(base_download_dir, subject_name)
        os.makedirs(subject_download_dir, exist_ok=True)
        
        # Set up a WebDriver for this unique subject
        driver = setup_firefox_webdriver(subject_download_dir)
        if driver:
            subject_drivers[subject_name] = driver

    for key, value in data.items():
        subject_name = value.get('subject_name')
        id = value.get('id')
        subject_download_dir = os.path.join(base_download_dir, subject_name)
        timestamp = time.time()  # Current time
        driver = subject_drivers[subject_name]
        logging.info("Navigating to webpage")
        print('Navigating to webpage')
        driver.get("https://en1.savefrom.net/2ol/")

        logging.info("Waiting for input area")
        print('Waiting for input area')
        input_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sf_url"))
        )

        logging.info("Sending string to input area")
        print("Sending string to input area")
        string_to_send = value.get('webpage_url')# "https://www.youtube.com/watch?v=NqvooBJ8FY8" #  "https://www.youtube.com/watch?v=jEF-u4ntt2Q"
        input_area.send_keys(string_to_send)

        logging.info("Waiting for 2 seconds")
        time.sleep(2)

        logging.info("Locating and clicking the download button")
        print("Locating and clicking the download button")
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sf_submit"))
        )
        download_button.click()
        logging.info("Waiting for 3 seconds")
        time.sleep(3)

        # Take the screenshot
        print("1. ")
        capture_screenshot(driver)
        try:
            check_and_process_captcha(driver, model)
            print("Captcha processed")
        except Exception as e:
            print("No captcha found")

        time.sleep(3)
        download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sf_submit")))
        download_button.click()
        print('We click on the download button again')
        time.sleep(3)
        print("2. ")
        capture_screenshot(driver)
        try:
        # Wait for the section to be present
            print("try for low quality")
            section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "landingTz-main-screen-top"))
        )

        # Find the "with low quality" link and click it
            low_quality_link = section.find_element(By.XPATH, ".//a[@class='landingTz-btn-close' and contains(text(), 'with low quality')]")

            print("Found the 'with low quality' link. Clicking it now...")
            low_quality_link.click()
            print("Successfully clicked the 'with low quality' link.")
        except Exception as e:
            print("No low quality link found")
                # Wait for the sf_result div to be present
            getDownload(driver)
            

            print("Download link clicked successfully")
            print("3. ")
            if check_value_above_400(driver):
                getDownload(driver)
                PopUpLargeVideos(driver)
        check_and_rename_mp4_files(subject_download_dir, timestamp,id)
        totalDuration += float(value.get('duration'))
            # Wait for the sf_result div to be present

    # Find the download link within sf_result
        time.sleep(5)
        capture_screenshot(driver)


    logging.info("Waiting for 10 seconds after clicking the download button")
    time.sleep(300)


    logging.info("Script execution completed")
    print("Script execution completed")

except WebDriverException as e:
    logging.error(f"WebDriver error occurred: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
finally:
    capture_screenshot(driver)
    logging.info("Closing WebDriver")
    if 'driver' in locals():
        driver.quit()

# Get the end time of the loop
end_time = time.time()
print(f"Loop end time: {end_time}")

# Calculate and print the total execution time
execution_time = end_time - start_time
print(f"Total execution time: {execution_time} seconds")