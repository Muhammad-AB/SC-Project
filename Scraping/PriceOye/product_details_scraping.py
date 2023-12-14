from selenium import webdriver   # basic driver type
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv 
import json



def extract_product_details(url, f_product_details):
    print("Entered extract detail function")
    
    for i in range(1, len(url)-1):

        print("\n"+str(i)+"- Entered for loop")

        # 1. URL
        URL = url[i]
        try:
            driver.get(URL)
            # Wait for the page to fully load
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            wait = WebDriverWait(driver, 2)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'review-box')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #soup = BeautifulSoup(soup.prettify(), "html.parser")
        except TE:
            pass

        except AttributeError:
            continue
        

        # 17. img link
        try:
            # # Find the div with the specific class
            # div = soup.find('div', {'class': 'swiper-slide swiper-slide-visible'})
            # # Extract the image source from the img tag
            # img_src = div.find('img')['src']

            # # Find the div with specific class
            # image_list_div = soup.find('div', {'class': 'image-list'})

            # # Find the img tag and get the src attribute value
            # img_src = image_list_div.find('img')['src']

            image_list_div = soup.find("div", {"class": "image-list"})
            image_sources = []
            if image_list_div:
                images = image_list_div.find_all("img")
                for img in images:
                    if "src" in img.attrs:
                        image_sources.append(img["src"])
            #print(image_sources)

        except Exception:
            print("img Error")
            continue


        # 2. Title
        try:
            title = soup.find('div', {'class': 'product-title'})
            # Find the <h3> element within the <div> element
            h3 = title.find('h3')
            title = h3.text

        except AttributeError:
            continue

        print("Title:",title)

        # 3. Actual Price
        try:
            actual_price = soup.find('div', {'class': 'retail-price market-price'})
            actual_price = actual_price.find('span')
            actual_price = actual_price.text

        except AttributeError:
            actual_price = "null"
        print("Actual Price:",actual_price)


        # 4. Discounted Price
        try:
            discount_price = soup.find('div', {'class': 'product-price po-price-border'})
            discount_price = discount_price.find_all('span')
            discount_price = discount_price[1].text

        except AttributeError:
            continue
        print("Discount Price:",discount_price)



        # 5. Discounted Perecent
        try:
            discount_percent = soup.find('div', {'class': 'save-price-section'})
            discount_percent = discount_percent.find('span')
            discount_percent = discount_percent.text

        except AttributeError:
            discount_percent = "null"
        print("Discount Percent:",discount_percent)


        # 6. Availability
        try:
            availability = soup.find('div', {'class': 'retail-price product-price'})
            availability = availability.find_all('span')
            availability = availability[1].text

        except AttributeError:
            availability = "null"
        print("Availability:",availability)


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

        '''
        # 9. Delivery Fee
        try:
            delivery_fee = soup.find_all('div', {'class': 'spec-desc services-spec'})
            delivery_fee = delivery_fee[3].find('strong')
            delivery_fee = delivery_fee.text

        except AttributeError:
            print("Error")
            delivery_fee = 'null'

        print("Delivery Fee:",delivery_fee)


        # 10. Warranty
        try:
            warranty = soup.find('div', {'class': 'spec-desc services-spec'})
            warranty = warranty.find('strong')
            warranty = warranty.text

        except AttributeError:
            print("Error")
            warranty = 'null'
        print("Warranty:",warranty)
        

        # 11. Display

        try:
            specs = soup.find_all('div', {'class': 'spec-desc'})
            #print("specs:",specs)
            display = specs[4].find('strong')
            display = display.text

        except AttributeError:
            print("Error")
            display = 'null'
        print("Display:",display)



        # 12. RAM
        try:
            #display = soup.find-all('div', {'class': 'spec-desc'})
            ram = specs[5].find('strong')
            ram = ram.text

        except AttributeError:
            print("Error")
            ram = 'null'
        print("RAM:",ram)


        # 13. Battery
        try:
            #display = soup.find-all('div', {'class': 'spec-desc'})
            battery = specs[6].find('strong')
            battery = battery.text

        except AttributeError:
            print("Error")
            battery = 'null'
        print("Battery:",battery)


        # 14. Camera
        try:
            #camera = soup.find-all('div', {'class': 'spec-desc'})
            camera = specs[7].find('strong')
            camera = camera.text

        except AttributeError:
            print("Error")
            camera = 'null'
        print("Camera:",camera)
        '''

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


        # Wait for the page to finish loading
        # try:
        #     wait = WebDriverWait(driver, 10)
        #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "user-reivew-description client-review h6")))
        #     #wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # except TE:
        #     pass


        # 16. Comment/Reviews
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



        data = [i, URL, title, 'Earbuds', actual_price, discount_price, discount_percent, availability, rating, review_count, json_specs, json_comments, image_sources,
                "PriceOye", 'https://priceoye.pk/']

        print("Entering Results to csv:")
        with open(f_product_details, 'a+', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(data)




driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

f_product_url = 'Wireless Earbuds_URL.csv'   #Name of csv file in which URLs are stored
f_product_details = "PriceOye_Wireless Earbuds.csv"   #Name of csv file in which you want to store product details

file = open(f_product_url)
csvreader = csv.reader(file)
url = []
#i = 1
for row in csvreader:
    row = ' '.join(row)
    url.append(row)

#print("URL is: ", url)


header = ['Row','URL', 'Title', 'Category', 'Actual Price', 'Discount Price', 'Discount Percentage', 'Availability', 'Rating', 'Review Count', 'Specifications', 'Comments', 
          'Image Link', 'Vendor','Vendor URL']


with open(f_product_details, 'w', newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
file.close()

data = extract_product_details(url, f_product_details)



driver.close()

#header = [, 'Brand', 'Vendor', "Vendor_URL"]
