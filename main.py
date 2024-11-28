import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Print a startup message
print("Hello I'm starting the project")

# Setup Chrome options for headless operation in Google Cloud Shell
options = Options()
options.add_argument('--headless')  # Ensure headless mode
options.add_argument('--no-sandbox')  # Run Chrome without sandboxing (necessary for Linux environments)
options.add_argument('--disable-dev-shm-usage')  # Overcome resource issues in some environments
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--window-size=1920x1080')  # Set window size for headless mode

# Set the binary location to Chromium's path (Google Cloud Shell default)
options.binary_location = '/usr/bin/chromium-browser'

# Set up the WebDriver with Chromium
driver = webdriver.Chrome(service=Service('/usr/lib/chromium-browser/chromedriver'), options=options)

# Function to retrieve video description and timestamps
def get_video_description(url):
    driver.get(url)

    # Wait for the "Accept Cookies" button (if it exists) and click it
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-text="Accept Cookies"]'))).click()
    except:
        print("No Accept Cookies button found")

    # Wait for the video metadata to load (title and description)
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
    )

    video = {}

    # Get the video title
    title = driver.find_element(By.CSS_SELECTOR, 'h1.ytd-watch-metadata').text
    video['title'] = title
    print("Title:", title)

    # Wait for the "Show More" button to be clickable and click it
    try:
        time.sleep(5)  # Adding a small delay before trying to expand description
        expand_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "expand")))
        expand_button.click()
    except Exception as e:
        print("Could not click 'Show More' button:", e)

    # Attempt to retrieve the description text after expansion
    try:
        description = driver.find_element(By.CSS_SELECTOR, '#description-inline-expander .ytd-text-inline-expander span').text
    except Exception as e:
        print("Could not fetch description after clicking 'Show More':", e)
        description = ""

    # Print out the full description for debugging
    print("Full Description:", description)

    video['description'] = description

    # Define the updated regex pattern for timestamps (handles multiple formats)
    timestamp_pattern = r'\b(?:[0-9]{1,2}:)?[0-9]{2}:[0-9]{2}\b|\b\d{1,2}m \d{1,2}s\b|\b\d{1,2}h \d{1,2}m\b'

    # Attempt to find the timestamps in the description
    timestamps = re.findall(timestamp_pattern, description)
    video['timestamps'] = timestamps
    print("Timestamps found:", timestamps)

    driver.quit()
    return video

# Example URL (You can replace this with any YouTube video URL)
video_url = "https://www.youtube.com/watch?v=iTmlw3vQPSs"
description_text = get_video_description(video_url)
print(description_text)