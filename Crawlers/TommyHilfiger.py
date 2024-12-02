from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import random as r
import os 
import requests
from datetime import datetime

PATH = "../Data/TommyHilfiger"

def price(item):
    try:
        selling = item.find_element(by=By.CSS_SELECTOR, value=".vtex-product-price-1-x-sellingPriceRangeUniqueValue .vtex-product-price-1-x-currencyContainer").find_elements(by=By.CSS_SELECTOR, value="span")
        selling_price = "".join(part.text for part in selling)
        selling_price = selling_price.replace("$", "").replace(",", "")
        selling_price = str(int(float(selling_price)))

        list_price = item.find_element(by=By.CSS_SELECTOR, value=".vtex-product-price-1-x-listPriceValue .vtex-product-price-1-x-currencyContainer").find_elements(by=By.CSS_SELECTOR, value="span")
        listPrice = "".join(part.text for part in list_price)
        listPrice = listPrice.replace("$", "").replace(",", "")
        listPrice = str(int(float(listPrice)))

        return {"selling_price": selling_price, "list_price": listPrice}
    except Exception as e:
        return {"selling_price": None, "list_price": None}
    
def download(url, path):
    try:
        response = requests.get(url, stream=True, timeout=10)  
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):  
                    f.write(chunk)
            print(f"Downloaded: {path}")
        else:
            print(f"Failed to download image. URL: {url}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

def extract(page):
    page -= 1
    items = driver.find_elements(by=By.CSS_SELECTOR, value=".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100")
    for i, item in enumerate(items):
        img_url = item.find_element(by=By.CSS_SELECTOR, value='[style*="width: 100%;"][style*="height: 534px;"][style*="object-fit: contain;"][style*="max-height: unset;"][style*="max-width: 400px;"]').get_attribute('src')
        prices = price(item)
        name = prices["list_price"] if prices["list_price"] else prices["selling_price"]
        name = f"{name}_{i + (page*42)}.jpg"
        path = os.path.join(PATH, name)
        download(img_url, path)

# Browser options and configurations
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--incognito')

link = "https://mx.tommy.com/hombre/ropa?page="

# Starting the search
driver = webdriver.Chrome(options=options)
driver.get(link)

for i in range(1, 45):
    try:
        driver.get(link + str(i))
        sleep(r.uniform(6.0,8.0))
        extract(i)

        driver.quit()
    except Exception as e:
        print(f"Error on page {i}: {e}")
        driver.quit()
        break 