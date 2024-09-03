from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime, time as datetime_time, timedelta
import time
import json
import re
import os
import base64
import ddddocr
from utils import open_driver, search_keyword

def place_order(driver, wait, product_name, delay=1):
    def login():
        driver.get(url)
        try:
            login_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="basic-navbar-nav"]/div/a[2]')))
            login_button.click()
            username = "your_email@example.com"
            password = "your_password"
            driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(username)
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/form/button').click()
            time.sleep(delay)
        except TimeoutException:
            print("User might be already logged in.")

    def add_to_cart():
        card_body = driver.find_element(By.CLASS_NAME, "card-body")
        product_link = card_body.find_element(By.XPATH, './/a')
        if os.name == 'posix':
            product_link.send_keys(Keys.COMMAND, Keys.RETURN)
        else:
            product_link.send_keys(Keys.CONTROL, Keys.RETURN)
        time.sleep(delay)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(delay)

        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-block.btn.btn-primary')
        add_to_cart_button.click()
        time.sleep(delay)

    def checkout_order():
        checkout_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-block.btn.btn-primary')
        checkout_button.click()
        time.sleep(delay)

        address_input = driver.find_element(By.ID, 'address')
        city_input = driver.find_element(By.ID, 'city')
        postalcode_input = driver.find_element(By.ID, 'postalCode')
        country_input = driver.find_element(By.ID, 'country')
        address_input.clear()
        city_input.clear()
        postalcode_input.clear()
        country_input.clear()

        address_input.send_keys("No.1 Hebin Road")
        city_input.send_keys("Chengdu")
        postalcode_input.send_keys("610000")
        country_input.send_keys("China")
        continue_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        continue_button.send_keys(Keys.ENTER)
        time.sleep(delay)

        payment_continue_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        payment_continue_button.click()
        time.sleep(delay)

        place_order_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-block.btn.btn-primary')
        place_order_button.click()
        time.sleep(delay)

    def solve_captcha():
        canva_element = wait.until(EC.presence_of_element_located((By.ID, "canv")))
        script = """
        const canvas = document.getElementById('canv');
        const img = canvas.toDataURL('image/jpg');
        return img;
        """
        img = driver.execute_script(script)      
        img_data = img.split(',')[1]
        image_bytes = base64.b64decode(img_data)
        with open("results/captcha_image.jpg", 'wb') as f:
            f.write(image_bytes)
        print("Captcha image saved successfully.")

        ocr = ddddocr.DdddOcr(beta=True)
        with open("results/captcha_image.jpg", 'rb') as f:
            image = f.read()
        captcha_res = ocr.classification(image)
        print(captcha_res)
        time.sleep(delay)

        user_captcha_input = driver.find_element(By.ID, 'user_captcha_input')
        user_captcha_input.send_keys(captcha_res)
        time.sleep(delay)
        submit_button = driver.find_element(By.CLASS_NAME, "btn-primary")
        submit_button.send_keys(Keys.ENTER)
        time.sleep(delay)

    login()
    search_keyword(driver, product_name, delay)
    add_to_cart()
    checkout_order()
    solve_captcha()

def find_top_expensive_products(driver, wait, x, keyword, delay=1):
    products = []

    def get_product_info():
        card_bodys = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-body")))

        for card_body in card_bodys:
            product_link = card_body.find_element(By.TAG_NAME, 'a')
            if os.name == 'posix':
                product_link.send_keys(Keys.COMMAND, Keys.RETURN)
            else:
                product_link.send_keys(Keys.CONTROL, Keys.RETURN)

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            list_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-group-item")))
            time.sleep(delay)

            product = {}
            name = list_items[0].text
            price = re.findall(r'\d+\.\d+|\d+', list_items[2].text)[0]
            product['name'] = name
            product['price'] = float(price)
            product['description'] = list_items[3].text
            products.append(product)
            print(product, end='\n\n')
            driver.close()
            time.sleep(delay)
            driver.switch_to.window(windows[0])

    def go_to_next_page():
        next_page_button.click()
        time.sleep(delay)

    def save_products_to_csv():
        top_x_result = sorted(products, key=lambda x: x['price'], reverse=True)[:x]
        with open(f'results/top_{x}_products_{keyword}.csv', 'w') as f:
            json.dump(top_x_result, f, indent=4)
        return top_x_result

    search_keyword(driver, keyword, delay)

    page = 2
    while True:
        get_product_info()
        try:
            next_page_button = driver.find_element(By.XPATH, f'//a[@class="page-link" and text()="{page}"]')
        except NoSuchElementException:
            break
        go_to_next_page()
        page += 1
        time.sleep(delay)

    return save_products_to_csv()

def order_top_products(driver, wait, x, keyword, delay=1):
    top_products = find_top_expensive_products(driver, wait, x, keyword, delay)
    for product in top_products:
        place_order(driver, wait, product["name"], delay)
        time.sleep(delay)

# Example usage
if __name__ == "__main__":
    url = 'http://10.113.178.219'
    delay = 1
    driver = open_driver(url)
    wait = WebDriverWait(driver, 10)

    try:
        place_order(driver, wait, 'IPHONE 11 PRO 256GB MEMORY', delay)
        find_top_expensive_products(driver, wait, 3, 'apple', delay)
        order_top_products(driver, wait, 2, 'phone', delay)
    finally:
        driver.quit()