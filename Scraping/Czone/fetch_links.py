from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch(driver, category_name, category_url):

    # Navigations
    print(f"Trying {category_url} at {time.ctime()}") 
    driver.get(category_url)
    driver.find_element(By.CSS_SELECTOR, "#ddlResults").click()
    driver.find_element(By.CSS_SELECTOR, "#ddlResults > option:nth-child(6)").click()
    products = driver.find_elements(By.CSS_SELECTOR, "div > h4 > a")

    links = []
    for product in products:
        link = product.get_attribute("href")
        if link[-5:] == ".aspx":
            links.append(link)

        
    # Saving the Data
    with open(f"cz_{category_name}_links.txt",'a') as txt:
        for link in links:
            txt.write(f"\n{link}")

    print(f"Collected {len(links)} products in Category: {category_name}")

CATEGORIES = {
    "Laptop": "https://www.czone.com.pk/laptops-pakistan-ppt.74.aspx",
    "Used Laptop": "https://www.czone.com.pk/laptops-used-pakistan-ppt.715.aspx",
    "Headsets": "https://www.czone.com.pk/headsets-headphones-mic-pakistan-ppt.175.aspx",
    "Speakers": "https://www.czone.com.pk/speakers-pakistan-ppt.97.aspx",
    "Cameras": "https://www.czone.com.pk/cameras-drones-pakistan-ppt.136.aspx",
    "Mouse": "https://www.czone.com.pk/mouse-pakistan-ppt.95.aspx",
    "Keyboard": "https://www.czone.com.pk/keyboard-pakistan-ppt.162.aspx",
    "Watch": "https://www.czone.com.pk/smart-watches-pakistan-ppt.403.aspx",
    "Mobile": "https://www.czone.com.pk/tablet-pc-pakistan-ppt.278.aspx",
    "Monitor": "https://www.czone.com.pk/lcd-led-monitors-pakistan-ppt.108.aspx"
}

# Create an instance of Chrome webdriver
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.maximize_window()

for category_name, category_url in CATEGORIES.items():
    fetch(driver, category_name, category_url)
# driver.quit()