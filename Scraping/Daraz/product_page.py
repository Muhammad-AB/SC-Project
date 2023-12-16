from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

df = pd.read_excel('test.xlsx')
filename="test.txt" 
file = open(filename, "r")
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.maximize_window()
url = file.readline()

while url:
    try:
        driver.get(url)
    except:
        pass
    driver.implicitly_wait(20)
    
    for i in range(1,10):
        j = 500*i
        script = 'window.scrollTo(0, '+ str(j) + ');'
        driver.execute_script(script)
        time.sleep(1)
    
    try:
        button = driver.find_element(By.CLASS_NAME, "pdp-view-more-btn")
        button.click()
        time.sleep(3)
    except:
        pass

    try:
        page_src = driver.page_source
        soup = BeautifulSoup(page_src, 'html.parser')
    except:
        pass

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
        details = soup.find('div', class_ = 'html-content pdp-product-highlights').text
    except:
        details = []

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
    
    if "usd" or "dollar" or "$" in dprice.lower():
            currency = "USD"
    else:
            currency = "PKR"

    row = {"slug": url,
           "title": title,
           # "currency": currency,
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
           'Reviews':str(reviews_list),
           'Recommended Products': str(recommended_products_list),
           'Recommended Products Images': str(recommended_products_img_list)
           }
    df = df._append(row, ignore_index=True)
    df.to_excel('test.xlsx', index=False)
    url = file.readline()

    
