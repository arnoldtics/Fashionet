from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import random as r
import os 
import requests
from datetime import datetime

PATH = "../Data/Scappino"

def download(url, path):
    response = requests.get(url, stream=True) # download in chunks
    if response.status_code == 200:
        with open(path, 'wb') as f: 
            for chunk in response.iter_content(chunk_size=1024): 
                f.write(chunk)
    else: print(f"Failed image {url}")

def next_button():
    button = driver.find_element(by=By.XPATH, value="/html/body/div[2]/main/div[3]/div/div[3]/div[2]/div/button")
    button.click()

def extract():
    items = driver.find_elements(by=By.CSS_SELECTOR, value=".item.product.product-item")
    for i, item in enumerate(items):
        img_url = item.find_element(by=By.CLASS_NAME, value="product-image-photo").get_attribute("src")
        price = item.find_element(by=By.CLASS_NAME, value="price-wrapper").get_attribute("data-price-amount")
        name = f"{price}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}.jpg"
        path = os.path.join(PATH, name)
        download(img_url, path)

# Browser options and configurations
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
options.add_argument('--incognito')

link = "https://www.scappino.com/es/coleccion.html"

# Starting the search
driver = webdriver.Chrome(options=options)
driver.get(link)

# time for getting the web page ready manually
sleep(8)

while True:
    try:
        next_button()
        sleep(r.uniform(1.0, 3.0))
    except: break

extract()

driver.quit()