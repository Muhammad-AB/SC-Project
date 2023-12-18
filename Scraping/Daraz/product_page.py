from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def initialize_driver():
    """
    Initialize and return a Chrome webdriver.

    Parameters:
        None

    Returns:
        webdriver.Chrome: An instance of the Chrome webdriver.
    """
    return webdriver.Chrome(executable_path=ChromeDriverManager().install())

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
    title = soup.find('span', class_='pdp-mod-product-badge-title').text if soup else ''
    oprice = soup.find('span', class_='pdp-price pdp-price_type_deleted pdp-price_color_lightgray pdp-price_size_xs').text if soup else ''
    dprice = soup.find('span', class_='pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl').text if soup else ''
    discount = soup.find('span', class_='pdp-product-price__discount').text if soup else ''
    address = soup.find('div', class_='location__address').text if soup else ''
    dedetails_list = [dedetail.text for dedetail in soup.findAll('div', class_='delivery-option-item__title')] if soup else []
    deltime = soup.find('div', class_='delivery-option-item__time').text if soup else ''
    delfee = soup.find('div', class_='delivery-option-item__shipping-fee').text if soup else ''
    img = soup.find('img', class_='pdp-mod-common-image gallery-preview-panel__image').get("src") if soup else ''
    brand = soup.find('a', class_='pdp-link pdp-link_size_s pdp-link_theme_blue pdp-product-brand__brand-link').text if soup else ''
    scoreavg = soup.find('span', class_='score-average').text if soup else ''
    scoremax = soup.find('span', class_='score-max').text if soup else ''
    count = soup.find('div', class_='count').text if soup else ''
    reviews_list = [review.text for review in soup.findAll('div', class_='content')[1:]] if soup else []
    recommended_products_list = [recommended_product.get("href") for recommended_product in soup.findAll('a', class_='product-item-link')] if soup else []
    recommended_products_img_list = [recommended_product_img.get("src") for recommended_product_img in soup.findAll('img', class_='image')] if soup else ''

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
    df = pd.read_excel('test.xlsx')
    filename = "test.txt"
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

        df = df.append(row, ignore_index=True)
        df.to_excel('test.xlsx', index=False)
        url = file.readline()

if __name__ == "__main__":
    main()
