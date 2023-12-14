from selenium import webdriver   # basic driver type
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv 
import json
import time



def extract_product_details(url, f_product_details):
    print("Entered extract detail function")
    
    for i in range(1, 195):

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
        

        # 17. img link
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

        # 2. Title
        try:
            title = soup.find('div', {'class': 'col-xs-12 col-sd-12 col-md-7 item-detail-right-panel'})
            # Find the <h3> element within the <div> element
            h2 = title.find('h2')
            title = str(h2.text)

        except Exception:
            print("Title Error")
            continue

        print("\nTitle: ",title)

        # 3. Discounted Price
        # try:
        #     actual_price = soup.find('div', {'class': 'retail-price market-price'})
        #     actual_price = actual_price.find('span')
        #     actual_price = actual_price.text

        # except AttributeError:
        #     actual_price = "null"
        # print("Actual Price:",actual_price)

        discount_price = None


        # 4. Actual Price
        try:
            # Find the price span element

            # price_span = soup.find('div', {'class': 'col-xs-12 col-md-5  no-padding '})

            # # Get the price from the content attribute of the desc-price span
            # discount_price = price_span.find('span', {'id': 'price'}).text
            # #discount_price = discount_price[1].text

            price_element = soup.find("span", {"id": "price"})
            actual_price = price_element.text.strip()
            if (actual_price != 'N/A' and actual_price != 'Coming Soon'):
                cleaned_data = ''.join(filter(str.isdigit, actual_price))
                actual_price = int(cleaned_data)

        except AttributeError:
            print("Price Error")
            continue
        print("Actual Price: ",actual_price)


        # # 5. Discounted Perecent
        # try:
        #     discount_percent = soup.find('div', {'class': 'save-price-section'})
        #     discount_percent = discount_percent.find('span')
        #     discount_percent = discount_percent.text

        # except AttributeError:
        #     discount_percent = "null"
        # print("Discount Percent:",discount_percent)

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

        '''
        # 7. Rating
        try:
            rating = soup.find('div', {'class': 'semi-bold rating-points'})
            rating = rating.text

        except AttributeError:
            rating ="null"
        print("Rating:",rating)

        # 8. Reviews_count
        try:
            review_count = soup.find('div', {'class': 'semi-bold rating-count'})
            review_count = review_count.text

        except AttributeError:
            review_count = 'null'
        print("Review Count:",review_count)


        # 15. Specs
        specs_dict = {}
        
        try:
            specs = soup.find('div', {'class': 'column column-80'})
            # extract data from the div
            tables = specs.find_all('table', {'class': 'p-spec-table card'})
            for table in tables:
                tbody = table.find('tbody')
                rows = tbody.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    attribute = th.text.strip()
                    value = td.text.strip()
                    specs_dict[attribute] = value
                    #specification.append([attribute, value])
        except AttributeError:
            specs_dict = {}
            print("Error")

        json_specs = json.dumps(specs_dict)
        # print("Specifications: ",specs_dict)
        print("\nKeys: ", specs_dict.keys())



        # 16. Comments/Reviews
        comments = []
        try:
            review_boxes = soup.find_all('div', {'class': 'review-box'})

            print("Review Boxes: ", len(review_boxes))
            if (len(review_boxes) == 0):
                comments = []

            # Loop through each review box and extract the review and date
            for box in review_boxes:
                # Extract the review content and date
                review_content = box.find('div', {'class': 'user-reivew-description client-review h6'}).text.strip()
                review_date = box.find('div', {'class': 'review-date'}).text.strip()
                # Print the review content and date
                comments.append(review_content)
                # print('Review:', review_content)
                # print('Date:', review_date)
                # print('-'*50)

        except AttributeError:
            print("Error")

        print("Comments: ", comments)
        json_comments = json.dumps(comments)


        print("\nImage link: ", len(image_sources),image_sources)
        '''


        # For storing data in CSV

        data = [i,URL, title, brand, 'Laptops', 'PKR', actual_price, discount_price, availability, warranty_duration, warranty_period,
                warranty_type, None, None, None, specs_dict, None, None, 0, None, None,None, None, None, None, img_src,
                'Office 11, 12, 14 Basement Ahmed Center, I-8 Markaz, Islamabad, Pakistan', "MEGA.PK", 'https://www.mega.pk/', time.ctime()]

        print("Entering Results to csv:")
        with open(f_product_details, 'a+', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        

        # For storing data in Json
        '''
        new_dict = {
        'slug': URL,
        'title': title,
        'currency': "PKR",
        'original_price': actual_price,
        'discounted_price': None,
        'address': 'Office 11, 12, 14 Basement Ahmed Center, I-8 Markaz, Islamabad, Pakistan',
        'delivery_time_from': None,
        'delivery_time_to': None,
        'delivery_time_period': None,
        'delivery_time_unparsed': None,
        'delivery_fee': None,
        'imgs': img_src,
        'brand': brand,
        'average_rating': None,
        'num_ratings': None,
        'reviews': None,
        'similer_products': None,
        'category': 'Mobile',
        'availability': availability,
        'vendor': 'MEGA.PK',
        'vendor_url': 'https://www.mega.pk/',

        'warranty_duration': warranty_duration,
        'warranty_period': warranty_period,

        'last_updated': time.ctime(),
        'description': None,
        'specifications': specs_dict,
        'used': 0,

        'warranty_type': warranty_type,

        'delivery_details': None
        }

        json_data = json.dumps(new_dict, indent=4)

        # Write JSON data to a file
        with open("data.json", "w") as file:
            file.write(json_data)
        '''




driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

f_product_url = 'Laptops_URL(1).csv'   #Name of csv file in which URLs are stored
f_product_details = "Mega.pk Laptops.csv"   #Name of csv file in which you want to store product details

file = open(f_product_url)
csvreader = csv.reader(file)
url = []
#i = 1
for row in csvreader:
    row = ' '.join(row)
    url.append(row)

#print("URL is: ", url)


header = ['Row','slug', 'title', 'brand', 'category', 'currency', 'original_price', 'discounted_price', 'availability', 'warranty_duration', 'warranty_period',
          'warranty_type', 'average_rating', 'num_ratings', 'reviews', 'Specifications', 'description', 'similar_products', 'used','delivery_time_from',
          'delivery_time_to','delivery_time_period', 'delivery_time_unparsed', 'delivery_fee', 'delivery_details', 'imgs', 'address', 'vendor','Vendor URL', 'last_updated']


with open(f_product_details, 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
file.close()

data = extract_product_details(url, f_product_details)



driver.close()

#header = [, 'Brand', 'Vendor', "Vendor_URL"]
