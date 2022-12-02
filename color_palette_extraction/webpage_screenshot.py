from io import BytesIO

from selenium import webdriver
from PIL import Image
from selenium.webdriver.firefox.options import Options


def get_screenshot(url_string):
    # Create options for the headless browser
    options = Options()
    options.add_argument('--headless')

    # Use selenium to open the webpage in a headless browser
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Take a screenshot of the webpage
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(BytesIO(screenshot))

    # Save the screenshot to a file
    image.save('screenshot.png')


# Get the URL from the user
url = "https://www.acagroup.be/"

# Get the screenshot of the webpage
get_screenshot(url)
