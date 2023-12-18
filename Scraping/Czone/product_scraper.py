from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import json
import time

def initialize_browser():
    """Initialize and return a Chrome webdriver."""
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.maximize_window()
    return browser

def scroll_to_bottom(browser):
    """Scroll to the bottom of the page."""
    ActionChains(browser).send_keys_to_element(browser.find_element(By.TAG_NAME, "body"), Keys.END).perform()

def scrape_product_details(link, browser):
    """Scrape product details from the given link."""
    print(f"Trying {link} at {time.ctime()}")
    browser.get(link)
    scroll_to_bottom(browser)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    product_name = soup.title.text.replace(' Price in Pakistan','').replace(' | Used Price in','').replace(' Pakistan','').strip()
    stockstatus = soup.find('span', id = 'spnStockStatus').text.strip()
    if "In" in stockstatus:
        availibility = "Available"
    elif "Order" in stockstatus:
        availibility = "Available on Order"
    else:
        availibility = "Not Available"
    imgs = []
    for img in soup.find('div', class_ = 'zoomMain').find_all('a'):
        imgs.append("https://www.czone.com.pk"+img['href']) 
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
    try:    
        warranty_duration = re.findall('[0-9]+', warranty)[0]
    except:
        warranty_duration = None
    if 'day' in warranty.lower():    
        warranty_period = "days"
    elif 'week' in warranty.lower():
        warranty_period = "weeks"
    elif 'month' in warranty.lower():
        warranty_period = "months"
    elif 'year' in warranty.lower():
        warranty_period = "years"
    else:
        warranty_period = None
    brand = soup.find('span', id = "spnBrand").text.strip()
    sim_prods_links = []
    sim_prods = soup.find('div', id = "SimilarProductSlider").find_all('div', class_ = "image product-image")
    for prod in sim_prods:
        sim_prods_links.append("https://www.czone.com.pk"+prod.find('a')['href'])
    description = soup.find('h1', id = "spnProductName").text.strip() + ". " + soup.find('div', id = "divProductDesc").text.strip()
    
    if soup.find('div', id = "producttabs1_tabsReview"):
        if soup.find('a', id = "producttabs1_anNoOverallReview"):
            average_rating = None
            num_ratings = None
            reviews = None
        else:
            average_rating = float(soup.find('span', id = "producttabs1_spnOverallProductRating").text.strip())
            num_ratings = int(re.findall('[0-9]+', soup.find('span', id = "producttabs1_spnOverallRatingCount").text.strip())[0])   
            reviews = soup.find_all('div', class_ = "review-subject")
            for i in range(len(reviews)):
                reviews[i] = reviews[i].text.strip()
            if len(reviews) == 0:
                reviews = None
    else:
        average_rating = None
        num_ratings = None    
        reviews = None
    last_updated = time.ctime()

    return {
                "slug":link,
                "title":product_name, 
                "currency":"PKR",
                "original_price":oprice, 
                "discounted_price":cprice,
                "address":"FL 4/20, Main Rashid Minhas Road, Gulshan-e-Iqbal Block-5, Karachi, Pakistan.",
                "delivery_time_from":None,
                "delivery_time_to":None,
                "delivery_time_period":None,
                "delivery_time_unparsed":None,
                "delivery_fee":None,
                "imgs":imgs,  
                "brand":brand,
                "average_rating":average_rating,
                "num_ratings":num_ratings ,
                "reviews":reviews,
                "similar_products":sim_prods_links,
                "availibility":availibility,
                "vendor":"ComputerZone",
                "vendor_url":"https://www.czone.com.pk/",
                "warranty_duration":warranty_duration,
                "warranty_period":warranty_period,            
                "last_updated":last_updated,
                "description":description,
                "used":1 if "used" in soup.find('h1', id = "spnProductName").text.strip().lower() else 0,
                "warranty_type":warranty_type,
                "delivery_details":None
            }

def extract_specifications(soup, category):
    """Extract specifications based on the product category."""
    specs = dict({})

    highlights = soup.find('div', id = "divProductHighlights").find_all("li")
    specs["Processor Type"] = highlights[0].text
    mem = highlights[1].text.split(', ')
    if len(mem) < 2:
        mem = highlights[1].text.split(' | ')
    if len(mem) < 2:
        mem = highlights[1].text.split(' - ')
    if len(mem) < 2:
        mem = highlights[1].text.split(' + ')
    if category == "Mobile":
        try:
            try:
                if "ram" in mem[1].lower():
                    specs["Installed RAM"] = mem[1]
                    specs["Hard drive size"] = mem[0]
                else:
                    specs["Installed RAM"] = mem[0]
                    specs["Hard drive size"] = mem[-1]
            except:
                mem = highlights[2].text.split(', ')
                if len(mem) < 2:
                    mem = highlights[2].text.split(' | ')
                if len(mem) < 2:
                    mem = highlights[2].text.split(' - ')
                if len(mem) < 2:
                    mem = highlights[2].text.split(' + ')
                specs["Installed RAM"] = mem[0]
                specs["Hard drive size"] = mem[-1]
                if "ram" in mem[1].lower():
                    specs["Installed RAM"] = mem[1]
                    specs["Hard drive size"] = mem[0]
        except:
            pass
    if category == "Laptop":
        specs["Installed RAM"] = mem[0]
        specs["Hard drive size"] = mem[-1]
        if ("graphics" in highlights[2].text.lower())  or ("gpu"  in highlights[2].text.lower()): 
            if ',' in highlights[2].text:
                mem = highlights[2].text.split(', ')
                if '-' in mem[0]:
                    mem[0] = mem[0].split(' - ')[0]
            elif '|' in highlights[2].text:
                mem = highlights[2].text.split(' | ')
            elif '-' in highlights[2].text:
                mem = highlights[2].text.split(' - ')
            else:
                mem = highlights[2].text
            if type(mem) is list:
                for i in mem:
                    if "Graphics" in i or "GPU" in i:
                        specs["Graphics memory"] = i
            else:
                specs["Graphics memory"] = mem
        elif ("graphics" in highlights[3].text.lower())  or ("gpu"  in highlights[3].text.lower()): 
            if ',' in highlights[3].text:
                mem = highlights[3].text.split(', ')
                if '-' in mem[0]:
                    mem[0] = mem[0].split(' - ')[0]
            elif '|' in highlights[3].text:
                mem = highlights[3].text.split(' | ')
            elif '-' in highlights[3].text:
                mem = highlights[3].text.split(' - ')
            else:
                mem = highlights[3].text
            if type(mem) is list:
                for i in mem:
                    if "Graphics" in i or "GPU" in i:
                        specs["Graphics memory"] = i
            else:
                specs["Graphics memory"] = mem
        else:
            if ',' in highlights[2].text:
                mem = highlights[2].text.split(', ')
                if '-' in mem[0]:
                    mem[0] = mem[0].split(' - ')[0]
            elif '|' in highlights[2].text:
                mem = highlights[2].text.split(' | ')
            elif '-' in highlights[2].text:
                mem = highlights[2].text.split(' - ')
            else:
                mem = highlights[2].text
            if type(mem) is list:
                for i in mem:
                    if "gb" in i.lower():
                        specs["Graphics memory"] = i
            else:
                specs["Graphics memory"] = mem
    
    return specs

def save_to_json(data, category):
    """Save the data to a JSON file."""
    with open(f"cz_{category}.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    data = []
    categories = ["Laptop", "Used Laptop", "Mobile"]

    for category in categories:
        filename = f"cz_{category}_links.txt"

        with open(filename, "r") as file:
            link = file.readline()
            link = file.readline()
            browser = initialize_browser()

            while link:
                product_details = scrape_product_details(link, browser)
                specifications = extract_specifications(product_details, category)
                product_details["specifications"] = specifications
                product_details["category"] = category
                data.append(product_details)
                link = file.readline()

        save_to_json(data, category)

if __name__ == "__main__":
    main()