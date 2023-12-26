# Script: Product Details Scraper
# Author: Muhammad Abdul Basit
# Date: 16/12/2023

# Script to extract product details from a list of URLs and store them in a CSV file
# Uses Selenium, BeautifulSoup, and ChromeDriverManager for web scraping

# Importing required libraries
from selenium import webdriver   # basic driver type
from selenium.common.exceptions import TimeoutException as TE
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import csv 
import json
import time


def extract_product_details(url, f_product_details):
    """
    Function to extract product details from a list of URLs and store them in a CSV file

    Args:
        url_list (list): List of URLs to extract product details from
        f_product_details (str): Name of the CSV file to store product details

    Returns:
        None
    """
    
    print("Entered extract detail function")
    
    for i in range(1, len(url)-1):

        print("\n"+str(i)+"- Entered for loop")

        # 1. URL
        URL = url[i]
        try:
            driver.get(URL)
            # Wait for the page to fully load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait = WebDriverWait(driver, 2)
            #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'review-box')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #soup = BeautifulSoup(soup.prettify(), "html.parser")
        except TE:
            pass

        except AttributeError:
            continue
        

        # 2. img link
        try:
            img_src = []
            # Find the img tag
            img_tag = soup.find('img', {'id': 'main-prod-img'})

            # Extract the src attribute
            img = img_tag['src']
            img_src.append(img)

        except Exception:
            print("img Error")
            continue
        
        print("Image source is:\n",img_src)
        print("Image source is:", type(img_src))

        # 3. Title
        try:
            title = soup.find('div', {'class': 'col-xs-12 col-sd-12 col-md-7 item-detail-right-panel'})
            # Find the <h3> element within the <div> element
            h2 = title.find('h2')
            title = str(h2.text)

        except Exception:
            print("Title Error")
            continue

        print("\nTitle: ",title)

        discount_price = None


        # 4. Actual Price
        try:
            price_element = soup.find("span", {"id": "price"})
            actual_price = price_element.text.strip()
            if (actual_price != 'N/A' and actual_price != 'Coming Soon'):
                cleaned_data = ''.join(filter(str.isdigit, actual_price))
                actual_price = int(cleaned_data)

        except AttributeError:
            print("Price Error")
            continue
        print("Actual Price: ",actual_price)


        discount_percent = None

        
        # 6. Availability
        try:
            stock_detail_div = soup.find('div', {'class': 'stock-detail'})
            #print("Stock Div: \n",stock_detail_div)
            availability = str(stock_detail_div.find('span', text='Stock Info:').next_sibling.strip())
            #print("Stock Div: \n",availability)
            if (availability.lower() == 'on order'):
                availability = "Available on Order"
            elif (availability.lower() == 'out of stock' or availability.lower() == 'unavailable'):
                availability = "Not Available"

        except Exception:
            availability = None
        print("Availability: ",availability)


        # 7. Waranty
        try:
            warranty = str(stock_detail_div.find('span', text='Warranty:').next_sibling.strip())
            warranty_period = "Year"
            if (warranty == 'No Warranty'):
                warranty_duration = None
                warranty_period = None
                warranty_type = None
            else:
                array = warranty.split(" ")
                warranty_duration = int(array[0])
                warranty_type = None
                try:
                    if (array[2].lower() == "international"):
                        warranty_type = "International Warranty"
                    elif (array[2].lower() == "local"):
                        warranty_type = "Local Warranty"
                    else:
                        warranty_type = None
                except Exception:
                    pass

        except Exception:
            warranty = None
            warranty_duration = None
            warranty_period = None
            warranty_type = None
        print("Warranty: ",warranty)


        # 8. Brand
        try:
            brand_div = soup.find('div', {'class': 'col-xs-12 col-sd-12 col-md-7 item-detail-right-panel'})
            a_tag = brand_div.find('a')
            brand = str(a_tag.span.text.strip())
            if (brand.lower() == 'real me'):
                brand = "Realme"
        
        except AttributeError:
            brand = None
            pass
        print("Brand : ", brand)


        # 9. Specs
        specs_dict = {}
        try:
            table = soup.find('table', id='laptop_detail')

            # Find all the rows in the table
            rows = table.find_all('tr')

            # Iterate over the rows and extract the data
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    key = columns[0].text.strip()
                    value = columns[1].text.strip()
                    specs_dict[key] = value

            # Print the data dictionary
            print('Specs: ',specs_dict)
        except AttributeError:
            print("Specs Error")
            pass


        # Storing data in CSV

        data = [i,URL, title, brand, 'Laptops', 'PKR', actual_price, discount_price, availability, warranty_duration, warranty_period,
                warranty_type, None, None, None, specs_dict, None, None, 0, None, None,None, None, None, None, img_src,
                'Office 11, 12, 14 Basement Ahmed Center, I-8 Markaz, Islamabad, Pakistan', "MEGA.PK", 'https://www.mega.pk/', time.ctime()]

        print("Entering Results to csv:")
        with open(f_product_details, 'a+', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        

# # Initializing the Chrome WebDriver
# driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
chromedriver_autoinstaller.install()

# Create a WebDriver instance
driver = webdriver.Chrome()


# File names
f_product_url = 'D:/Muhammad AB/NUST/5th Semester/Software Construction/Project/SC-Project/Apple Airpods_URL(1).csv'   #Name of csv file in which URLs are stored
f_product_details = "Mega.pk Bluethothhandfree.csv"   #Name of csv file in which you want to store product details

# Reading URLs from CSV file
file = open(f_product_url)
csvreader = csv.reader(file)
url = []
#i = 1
for row in csvreader:
    row = ' '.join(row)
    url.append(row)

#print("URL is: ", url)

# Writing Header in CSV
header = ['Row','slug', 'title', 'brand', 'category', 'currency', 'original_price', 'discounted_price', 'availability', 'warranty_duration', 'warranty_period',
          'warranty_type', 'average_rating', 'num_ratings', 'reviews', 'Specifications', 'description', 'similar_products', 'used','delivery_time_from',
          'delivery_time_to','delivery_time_period', 'delivery_time_unparsed', 'delivery_fee', 'delivery_details', 'imgs', 'address', 'vendor','Vendor URL', 'last_updated']

with open(f_product_details, 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
file.close()

# Extracting and storing product details
data = extract_product_details(url, f_product_details)

# Closing the WebDriver
driver.close()