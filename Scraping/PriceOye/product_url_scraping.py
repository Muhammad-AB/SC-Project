# Script: Product URL Scraper
# Author: Muhammad Abdul Basit
# Date: 16/12/2023

# Script to generate and extract product URLs for a given search term from priceoye.pk and store them in a CSV file
# Uses Selenium, BeautifulSoup, and ChromeDriverManager for web scraping

# Importing required libraries
from selenium import webdriver   # basic driver type
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv 


def get_search_url(search_term):
    """
    Function to generate the search URL and retrieve total pages

    Args:
        search_term (str): Search term for generating the URL

    Returns:
        list: A list containing the generated search URL and total pages
    """

    #Generate a url from search term
    print("\nEntered in get_url function\n")

    base_url = 'https://priceoye.pk/{}'
    search_term = search_term.replace(' ', '-')
    print("Search Term is",search_term)

    # add term query to url
    url = base_url.format (search_term)
    print("URL is",url)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    t_pages = soup.find('div', class_="pagination")
    #print("Total Pages: ", t_pages)
    t_pages = t_pages.find_all('a', href = True)
    #print("Total Pages: ", t_pages)
    t_pages = t_pages[len(t_pages)-2].text
    t_pages = int(t_pages)
    print("Total Pages: ", t_pages)

    url+="?page={}"
    print("URL is",url)
    return [url,t_pages]


def extract_product_url(url, t_pages):
    """
    Function to extract product URLs from the search results pages
    
    Args:
        url (str): Search URL with placeholders for page numbers
        t_pages (int): Total number of pages in the search results

    Returns:
        list: List of product URLs
    """

    final_product_links = []    #Array in which all the url are going to be inserted

    i = 1

    for page in range(1, t_pages+1):

        print(i,") Entered extract url function")
        i+=1

        driver.get(url.format(page))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        productlist = soup.find_all('div', class_="productBox b-productBox")
        #print("Results are:",productlist)
        #j = 0
        for item in productlist:            
            for link in item.find_all('a', href = True):
                #print("Link:",link['href'])
                href = link.get("href")
                a_href = []
                a_href= href.split(" ")
                final_product_links.append(a_href)
                #print("final_product_link: ",final_product_links[j])
                #j+=1
    return final_product_links


def enter_urls_in_csv(final_product_links):
    """
    Function to enter product URLs in a CSV file
    
    Args:
        final_product_links (list): List of product URLs

    Returns:
        None
    """

    print("Opening csv")
    with open('Wireless Earbuds_URL.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        print("Entering results:")
        writer.writerow(['Wireless Earbuds_URL'])
        for row in final_product_links:
            #print("row is: ", row)
            writer.writerows([row])

    print("Done")


def main(search_term):
    """
    Main function to execute the script
    
    Args:
        search_term (str): Search term for generating the URL and extracting product URLs

    Returns:
        None
    """
    
    # Generating the search URL and retrieving total pages using the search term
    [url, t_pages] = get_search_url(search_term)

    # Extracting product URLs from the search results pages using the generated URL and total pages
    final_product_links = extract_product_url(url, t_pages)

    # Entering the extracted product URLs into a CSV file
    enter_urls_in_csv(final_product_links)


# Initializing the Chrome WebDriver
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

# Executing the main function with a sample search term
main("wireless earbuds")

# Closing the WebDriver
driver.close()