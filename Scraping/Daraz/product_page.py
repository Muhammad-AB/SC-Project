# Script: Product Details Scraper
# Author: Syed Ahsan Ullah Tanweer
# Date: 16/12/2023

# Script to extract product details from a list of URLs and store them in an excel file
# Uses Selenium, BeautifulSoup, and ChromeDriverManager for web scraping

from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import chromedriver_autoinstaller
from openpyxl import Workbook

def initialize_driver():
    """
    Initialize and return a Chrome webdriver.

    Parameters:
        None

    Returns:
        webdriver.Chrome: An instance of the Chrome webdriver.
    """
    # Create an instance of Chrome webdriver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver

def scroll_page(driver):
    """
    Scroll the page to load additional content.

    Parameters:
        driver (webdriver.Chrome): An instance of the Chrome webdriver.

    Returns:
        None
    """
    for i in range(1, 10):
        j = 500 * i
        script = 'window.scrollTo(0, ' + str(j) + ');'
        driver.execute_script(script)
        time.sleep(1)

def click_view_more_button(driver):
    """
    Click the 'View More' button if available.

    Parameters:
        driver (webdriver.Chrome): An instance of the Chrome webdriver.

    Returns:
        None
    """
    try:
        button = driver.find_element(By.CLASS_NAME, "pdp-view-more-btn")
        button.click()
        time.sleep(3)
    except:
        pass

def get_soup(driver):
    """
    Return BeautifulSoup object from the current page source.

    Parameters:
        driver (webdriver.Chrome): An instance of the Chrome webdriver.

    Returns:
        BeautifulSoup or None: BeautifulSoup object representing the page source or None if an exception occurs.
    """
    try:
        page_src = driver.page_source
        return BeautifulSoup(page_src, 'html.parser')
    except:
        return None

def extract_product_details(soup):
    """
    Extract product details from the BeautifulSoup object.

    Parameters:
        soup (BeautifulSoup): BeautifulSoup object representing the page source.

    Returns:
        dict: A dictionary containing extracted product details.
    """
    try:
        title = soup.find('span', class_ = 'pdp-mod-product-badge-title').text
    except:
        title = ''
    
    try:
        oprice = soup.find('span', class_ = 'pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs').text
    except:
        oprice = ''
    
    try:
        dprice = soup.find('span', class_ = 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl').text
    except:
        dprice = ''
    
    try:
        discount = soup.find('span', class_ = 'pdp-product-price__discount').text
    except:
        discount = ''
    
    try:
        address = soup.find('div', class_ = 'location__address').text
    except:
        address = ""

    try:
        dedetails_list = []
        dedetails = soup.findAll('div', class_ = 'delivery-option-item__title')
        for dedetail in dedetails:
            dedetails_list.append(dedetail.text)
    except:
        dedetails_list = []
    
    try:
        deltime = soup.find('div', class_ = 'delivery-option-item__time').text
    except:
        deltime = ''
    
    try:
        delfee = soup.find('div', class_ = 'delivery-option-item__shipping-fee').text
    except:
        delfee = ''
    
    try:
        img = soup.find('img', class_ = 'pdp-mod-common-image gallery-preview-panel__image').get("src")
    except:
        img = ''
    
    try:
        brand = soup.find('a', class_ = 'pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link').text
    except:
        brand = ''
    
    try:
        scoreavg = soup.find('span', class_ = 'score-average').text
    except:
        scoreavg = ''
    
    try:
        scoremax = soup.find('span', class_ = 'score-max').text
    except:
        scoremax  = ''
    
    try:
        count = soup.find('div', class_ = 'count').text
    except:
        count = ''
    
    try:
        reviews_list = []
        reviews = soup.findAll('div', class_ = 'content')[1:]
        for review in reviews:
            reviews_list.append(review.text)
    except:
        reviews_list = []
    
    try:
        recommended_products_list = []
        recommended_products = soup.findAll('a', class_ = 'product-item-link')
        for recommended_product in recommended_products:
            recommended_products_list.append(recommended_product.get("href"))
    except:
        recommended_products_list = []
        
    try:
        recommended_products_img_list = []
        recommended_products_img = soup.findAll('img', class_ = 'image')
        for recommended_product_img in recommended_products_img:
            recommended_products_img_list.append(recommended_product_img.get("src"))
    except:
        recommended_products_list = []
    
    return {
        "title": title,
        "original_price": oprice,
        'Discounted Price': dprice,
        'Discount': discount,
        'Address': address,
        'Delivery Details': str(dedetails_list),
        'Delivery Time': deltime,
        'Delivery Fee': delfee,
        'Image': img,
        'Brand': brand,
        'Avg Score': scoreavg,
        'Max Score': scoremax,
        'Count': count,
        'Reviews': str(reviews_list),
        'Recommended Products': str(recommended_products_list),
        'Recommended Products Images': str(recommended_products_img_list)
    }

def main():
    """
    Main function to execute the web scraping process and save results to an Excel file.

    Parameters:
        None

    Returns:
        None
    """
    file_path = 'test.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        # If the file doesn't exist, create it and write an empty DataFrame to it
        df = pd.DataFrame()
        df.to_excel(file_path, index=False)
        print(f"Created {file_path}")
        df = pd.read_excel(file_path)
    filename = "smartphones_links.txt"
    file = open(filename, "r")
    driver = initialize_driver()

    url = file.readline()
    while url:
        try:
            driver.get(url)
        except:
            pass

        driver.implicitly_wait(20)
        scroll_page(driver)
        click_view_more_button(driver)

        soup = get_soup(driver)
        product_details = extract_product_details(soup)

        if "usd" in product_details['Discounted Price'].lower() or "dollar" in product_details['Discounted Price'].lower() or "$" in product_details['Discounted Price'].lower():
            currency = "USD"
        else:
            currency = "PKR"

        row = {"slug": url,
                "title": product_details['title'],
                "original_price": product_details['original_price'],
                'Discounted Price': product_details['Discounted Price'],
                'Currency': currency,
                'Discount': product_details['Discount'],
                'Address': product_details['Address'],
                'Delivery Details': product_details['Delivery Details'],
                'Delivery Time': product_details['Delivery Time'],
                'Delivery Fee': product_details['Delivery Fee'],
                'Image': product_details['Image'],
                'Brand': product_details['Brand'],
                'Avg Score': product_details['Avg Score'],
                'Max Score': product_details['Max Score'],
                'Count': product_details['Count'],
                'Reviews': product_details['Reviews'],
                'Recommended Products': product_details['Recommended Products'],
                'Recommended Products Images': product_details['Recommended Products Images']
                }

        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_excel('test.xlsx', index=False)
        url = file.readline()

if __name__ == "__main__":
    main()
