from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import time

cat = "smartphones"
file = open("smartphones.txt", "w")
s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.maximize_window()
for pg_no in range(1, 20):
    driver.get('https://www.daraz.pk/'+str(cat)+'/?from=filter &page=+'+str(pg_no))
    driver.implicitly_wait(10)
    phoneNames = driver.find_elements(By.CLASS_NAME,'title--wFj93')
    for phone in phoneNames:
        file.write(phone.find_element(By.TAG_NAME, 'a').get_attribute("href"))
        file.write("\n")
file.close()    

    
        
