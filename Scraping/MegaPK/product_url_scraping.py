from selenium import webdriver   # basic driver type
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv 



def get_search_url(search_term):

    #Generate a url from search term
    print("\nEntered in get_url function\n")

    base_url = 'https://www.mega.pk/{}/'
    # search_term = search_term.replace(' ', '-')
    # print("Search Term is",search_term)

    # add term query to url
    url = base_url.format (search_term)
    print("URL is",url)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        t_pages = soup.find('div', class_="pagination")
        #print("Total Pages: ", t_pages)
        t_pages = t_pages.find_all('a', href = True)
        #print("Total Pages: ", t_pages)
        t_pages = t_pages[len(t_pages)-2].text
        t_pages = int(t_pages)
        print("Total Pages: ", t_pages)
    except Exception:
        print("Exception")
        t_pages = 1

    url+="{}/"
    print("URL is",url)
    return [url,t_pages]


def extract_product_url(url, t_pages):

    final_product_links = []    #Array in which all the url are going to be inserted

    i = 1

    for page in range(1, t_pages+1):

        print(i,") Entered extract url function")
        i+=1

        #print("\nHI\n")
        driver.get(url.format(page))
        #print("\nHI\n")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #print("\nSoup : \n",soup)
        #soup = soup.prettify()
        #print("\nPrettify Soup : \n",soup)
        
        productlist = soup.find('div', class_="product-grid-div")
        # print("Results are:",productlist)

        productlist = productlist.find_all('div', {'id': 'lap_name_div'})
        # href = a_tag['href']
        
        for item in productlist:
            j = 0
            for link in item.find_all('a', href = True):
                #print("Link:",link['href'])
                href = link.get("href")
                a_href = []
                a_href= href.split(" ")
                final_product_links.append(a_href)
                #print("final_product_link: ",final_product_links[j])
                j+=1
    return final_product_links


def enter_urls_in_csv(final_product_links):

    print("Opening csv")
    with open('Apple Airpods_URL(1).csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        print("Entering results:")
        writer.writerow(['Apple Airpods_URL'])
        for row in final_product_links:
            #print("row is: ", row)
            writer.writerows([row])

    print("Done")


def main(search_term):

    [url, t_pages] = get_search_url(search_term)

    final_product_links = extract_product_url(url, t_pages)

    enter_urls_in_csv(final_product_links)



driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

main("bluetoothhandfree-apple")

driver.close()