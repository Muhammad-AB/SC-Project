# Script: Product URL Scraper
# Author: Syed Ahsan Ullah Tanweer
# Date: 16/12/2023

# Script to extract product URLs for a given category and store them in a txt file
# Uses Selenium and ChromeDriverManager for web scraping

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

def initialize_driver():
    """
    Initialize and return a Chrome webdriver.

    Returns:
    webdriver.Chrome: Initialized Chrome webdriver
    """
    # Create an instance of Chrome webdriver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver

def get_phone_links(category, num_pages):
    """
    Retrieve phone links from Daraz for the given category and number of pages.

    Parameters:
    category (str): Category of the products
    num_pages (int): Number of pages to scrape

    Returns:
    list: List of phone links
    """
    phone_links = []
    driver = initialize_driver()

    for page_num in range(1, num_pages + 1):
        url = f'https://www.daraz.pk/{category}/?from=filter&page={page_num}'
        driver.get(url)
        driver.implicitly_wait(10)

        phone_names = driver.find_elements(By.CLASS_NAME, 'title--wFj93')
        for phone in phone_names:
            phone_links.append(phone.find_element(By.TAG_NAME, 'a').get_attribute("href"))

    driver.quit()
    return phone_links

def save_links_to_file(links, filename):
    """
    Save the phone links to a text file.

    Parameters:
    links (list): List of phone links
    filename (str): Name of the text file to save the links

    Returns:
    None
    """
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")

def main():
    category = "smartphones"
    num_pages = 4  # Adjust the number of pages as needed
    output_file = f"{category}_links.txt"

    phone_links = get_phone_links(category, num_pages)
    save_links_to_file(phone_links, output_file)

if __name__ == "__main__":
    main()
