from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json

def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Ignore warning and error logs
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(7)  # Set an implicit wait
    driver.maximize_window()
    return driver

def search_keyword(driver, keyword, delay=1):
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(keyword)
    time.sleep(delay)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(delay)

def save_results(products, filename='product_results.json'):
    with open(f'results/{filename}', 'w') as f:
        json.dump(products, f, indent=4)