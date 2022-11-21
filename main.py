import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import json


def open_page(url):
    webdriver.get(url)


def scroll_down():
    # get scroll height
    last_height = webdriver.execute_script("return document.body.scrollHeight")
    a = 0
    while a <= 10:
        # scroll down to bottom
        webdriver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # calculate new scroll height and compare with last scroll height
        new_height = webdriver.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(0.2)
            a += 1
        else:
            a = 0
        last_height = new_height


def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element(
            By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def find_element_by_xpath(xpath, timeout=10):
    try:
        element = WebDriverWait(webdriver, timeout, 1, [ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
    except TimeoutException:
        return None
    return element


def find_elements_by_xpath(xpath, timeout=10):
    try:
        elements = WebDriverWait(webdriver, timeout, 1, [ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_all_elements_located(
            (By.XPATH, xpath)))
    except TimeoutException:
        return None
    return elements


# webdriver and options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.headless = True
options.page_load_strategy = "normal"
webdriver = webdriver.Chrome(options=options)

# open page
open_page("https://www.ikonka.com.pl/black-friday-sale")

# get all product's <li> tags
scroll_down()
if check_exists_by_xpath("/html/body/div[4]/div[1]/div/section/div/div[4]/div[5]/ul"):
    products_li_tags = find_elements_by_xpath(
        "/html/body/div[4]/div[1]/div/section/div/div[4]/div[5]/ul/li")

data = []

for product in products_li_tags:
    img_src = None
    if product.find_element(By.XPATH, ".//img").get_attribute("src") != None:
        img_src = product.find_element(By.XPATH, ".//img").get_attribute("src")

    product_name = None
    product_url = None
    if product.find_element(By.XPATH, ".//a[@data-type='product-url']").get_attribute("title") != None:
        product_name = product.find_element(
            By.XPATH, ".//a[@data-type='product-url']").get_attribute("title")
        product_url = product.find_element(
            By.XPATH, ".//a[@data-type='product-url']").get_attribute("href")

    product_code = None
    if product.find_element(By.XPATH, "./div[3]/ul/li[1]/strong").text != None:
        product_code = product.find_element(
            By.XPATH, "./div[3]/ul/li[1]/strong").text

    product_EAN_code = None
    if product.find_element(By.XPATH, "./div[3]/ul/li[3]/strong").text != None:
        product_EAN_code = product.find_element(
            By.XPATH, "./div[3]/ul/li[3]/strong").text

    product_price = None
    if product.find_element(By.XPATH, "./div[4]/div/span[5]").text != None:
        product_price = product.find_element(
            By.XPATH, "./div[4]/div/span[5]").text

    data.append({
        "product_name": product_name,
        "img_src": img_src,
        "product_code": product_code,
        "product_EAN_code": product_EAN_code,
        "product_price": product_price,
        "product_url": product_url,
    })

print(json.dumps(data, indent=4))

webdriver.quit()
