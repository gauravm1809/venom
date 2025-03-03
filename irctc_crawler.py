from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


chrome_driver_path = "/Users/gauravmishra/PycharmProjects/venom/drivers/chromedriver"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)
ChromeDriverManager().install()
driver = webdriver.Chrome(options=chrome_options)


# driver.maximize_window()
driver.implicitly_wait(40)
driver.get("https://hotels.irctc.co.in/hotels")

sleep(10)

location_name = "Pune"

driver.find_element("xpath", "//input[@formcontrolname='where']").click()
sleep(10)
driver.find_element("xpath", "//input[@formcontrolname='where']").send_keys(location_name)
sleep(10)
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "(//div[@id='autofillId']//p)[1]"))).click()


WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "//input[@placeholder='Check-in Date']"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "(//td[@role='gridcell'])[35]"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "//input[@placeholder='Check-out Date']"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "//button[@class='next']"))).click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("xpath", "(//span[@class='ng-star-inserted'])[3]"))).click()


WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable(("xpath", "(//button[@class='hvr-shutter-in-vertical'])[1]"))).click()


def scroll_to_load_all_hotels(driver, prev_count=0):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

    hotel_details = driver.find_elements("xpath", "(//div[@id='hotelContainer']//span)")
    curr_count = len(hotel_details)

    if curr_count > prev_count:
        scroll_to_load_all_hotels(driver, curr_count)


scroll_to_load_all_hotels(driver)

hotel_details = driver.find_elements("xpath", "(//div[@id='hotelContainer']//span)")
hotel_prices = driver.find_elements("xpath", "//div[@class='priceMain ng-star-inserted']")

print(f"Found {len(hotel_details)} hotel details and {len(hotel_prices)} prices.")

hotels_data = []
for detail, price in zip(hotel_details, hotel_prices):
    hotel_info_lines = detail.text.split("\n")
    price_info_lines = price.text.split("\n")

    price_text = price_info_lines[0] if len(price_info_lines) > 0 else "N/A"
    taxes_text = price_info_lines[1] if len(price_info_lines) > 1 else "N/A"

    hotel_data = {
        "Hotel Name": hotel_info_lines[0],
        "Location": hotel_info_lines[1] if len(hotel_info_lines) > 1 else "N/A",
        "Features": hotel_info_lines[2] if len(hotel_info_lines) > 2 else "N/A",
        "Rating Category": hotel_info_lines[3] if len(hotel_info_lines) > 3 else "N/A",
        "Number of Ratings": hotel_info_lines[4] if len(hotel_info_lines) > 4 else "N/A",
        "Rating": hotel_info_lines[5] if len(hotel_info_lines) > 5 else "N/A",
        "Price": price_text,
        "Taxes & Fees": taxes_text
    }
    hotels_data.append(hotel_data)


directory_name = "irctc_hotel_fares"
if not os.path.exists(directory_name):
    os.makedirs(directory_name)


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"{location_name}_{timestamp}.json"
file_path = os.path.join(directory_name, file_name)


with open(file_path, "w", encoding="utf-8") as f:
    json.dump(hotels_data, f, indent=4, ensure_ascii=False)

print(f"Data saved to {file_path}")

driver.quit()
