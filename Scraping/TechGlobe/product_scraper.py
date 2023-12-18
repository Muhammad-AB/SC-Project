# Script: Product Details Scraper
# Author: Syed Ahsan Ullah Tanweer
# Date: 16/12/2023

# Script to extract product details from a list of URLs and store them in a json file
# Uses Selenium, BeautifulSoup, and ChromeDriverManager for web scraping

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import re
import json
import time

def initialize_browser():
    """
    Initialize and return a Chrome webdriver.

    Returns:
    webdriver.Chrome: Initialized Chrome webdriver
    """
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.maximize_window()
    return browser

def scroll_to_bottom(browser):
    """
    Scroll to the bottom of the page.

    Parameters:
    browser (webdriver.Chrome): Chrome webdriver instance

    Returns:
    None
    """
    ActionChains(browser).send_keys_to_element(browser.find_element(By.TAG_NAME, "body"), Keys.END).perform()

def scrape_product_details(link, browser):
    """
    Scrape product details from the given link.

    Parameters:
    link (str): URL of the product
    browser (webdriver.Chrome): Chrome webdriver instance

    Returns:
    dict: Dictionary containing scraped product details
    """
    print(f"Trying {link} at {time.ctime()}")
    browser.get(link)
    scroll_to_bottom(browser)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    product_name = soup.title.text.replace(' Laptop Price in Pakistan - TechGlobe.pk','').strip()
    stockstatus = soup.find('span', id = 'spnStockStatus').text.strip()
    if "In" in stockstatus:
        availibility = "Available"
    elif "Order" in stockstatus:
        availibility = "Available on Order"
    else:
        availibility = "Not Available"
    imgs = []
    for img in soup.find('div', class_ = 'zoomMain').find_all('a'):
        imgs.append(img['href'])
    cprice = soup.find('span', id = 'spnCurrentPrice')
    if not cprice:
        availibility = "Not Available"
        cprice = "Coming Soon"
    else:
        cprice = cprice.text
        cdigs = re.findall('[0-9]+', cprice)
        cprice = ''
        for i in cdigs:
            cprice += i
        cprice = int(cprice)
    try:
        oprice = soup.find('span', id = 'spnOldPrice').text.replace('\n','').replace('Regular Price','')
        odigs = re.findall('[0-9]+', oprice)
        oprice = ''
        for i in odigs:
            oprice += i
        oprice = int(oprice)
    except:
        oprice = None
    warranty = soup.find('span', id = 'spnWarranty').text.strip()
    if "International" in warranty:
        warranty_type = "International Warranty"
    else:
        if "Local" in warranty:
            warranty_type = "Local Warranty"
        else:
            warranty_type = None
    warranty_duration = re.findall('[0-9]+', warranty)[0]
    if 'day' in warranty.lower():    
        warranty_period = "days"
    elif 'week' in warranty.lower():
        warranty_period = "weeks"
    elif 'month' in warranty.lower():
        warranty_period = "months"
    else:
        warranty_period = "years"
    brand = soup.find('span', id = "spnBrand").text.strip()
    sim_prods_links = []
    sim_prods = soup.find('div', id = "SimilarProductSlider").find_all('div', class_ = "image product-image")
    for prod in sim_prods:
        sim_prods_links.append("https://www.techglobe.pk"+prod.find('a')['href'])
    description = soup.find('h1', id = "spnProductName").text.strip() + ". " + soup.find('div', id = "divProductDesc").text.strip()
    last_updated = time.ctime()
    product = {
        "slug":link,
        "title":product_name, 
        "currency":"PKR",
        "original_price":oprice, 
        "discounted_price":cprice,
        "address":None,
        "delivery_time_from":None,
        "delivery_time_to":None,
        "delivery_time_period":None,
        "delivery_time_unparsed":None,
        "delivery_fee":None,
        "imgs":imgs,  
        "brand":brand,
        "average_rating":None,
        "num_ratings":None,
        "reviews":None,
        "similar_products":sim_prods_links,
        "category":"Laptop",
        "availibility":availibility,
        "vendor":"TechGlobe",
        "vendor_url":"https://www.techglobe.pk/",
        "warranty_duration":warranty_duration,
        "warranty_period":warranty_period,            
        "last_updated":last_updated,
        "description":description,
        "used": 0,
        "warranty_type":warranty_type,
        "delivery_details":None
        }
    

    return product

def extract_specifications(soup):
    """
    Extract specifications based on the product category.

    Parameters:
    soup (BeautifulSoup): Parsed HTML content

    Returns:
    dict: Dictionary containing specifications
    """
    specs = dict({})
    try:
        highlights = soup.find('div', id = "divProductHighlights").find_all("li")
        specs["Processor Type"] = highlights[0].text
        if "gb" in highlights[1].text.lower():
            mem = highlights[1].text.split(', ')
            specs["Installed RAM"] = mem[0]
            specs["Hard drive size"] = mem[1]
        elif "gb" in highlights[2].text.lower():
            mem = highlights[2].text.split(', ')
            specs["Installed RAM"] = mem[0]
            specs["Hard drive size"] = mem[1]
        if "graphics" in highlights[2].text.lower():
            mem = highlights[2].text.split(', ')
            for i in mem:
                if "Graphics" in i:  
                    specs["Graphics memory"] = i.replace(' Graphics','')
    except:
        pass
    overview = soup.find('span', id = "producttabs1_spnContent")
    if overview.find('section', class_ = "spec-table"):
        for section in overview.find_all('section', class_ = "spec-table"):
            for item in section.find_all("div", class_ = "spec-table__item"):
                specs[str(item.find('p').text.strip())] = str(item.find('ul').text.strip())
    elif overview.find('tbody'):
        for table in overview.find_all('tbody'):
            for item in table.find_all('tr'):
                try:    
                    specs[str(item.find('th').text.strip())] = str(item.find('td').text.strip())
                except:
                    pair = item.find_all('td')
                    specs[str(pair[0].text.strip())] = str(pair[1].text.strip())
    else:
        pass

    return specs

def save_to_json(data, category):
    """
    Save the data to a JSON file.

    Parameters:
    data (list): List of product details dictionaries
    category (str): Category name

    Returns:
    None
    """
    with open(f"tg_{category}.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    data = []
    categs = ["laptops"]

    for categ in categs:
        filename = f"tg_{categ}_links.txt"

        with open(filename, "r") as file:
            link = file.readline()
            link = file.readline()
            browser = initialize_browser()

            while link:
                product_details = scrape_product_details(link, browser)
                specifications = extract_specifications(product_details)
                product_details["specifications"] = specifications
                product_details["category"] = "Laptop"
                data.append(product_details)
                link = file.readline()

            browser.quit()

        save_to_json(data, categ)

if __name__ == "__main__":
    main()
