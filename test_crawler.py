# from datetime import date
# import time
# import pytest
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
#
# CITY_NAME = "Dubai"
#
# class TestCrawler:
#     locator_type = "xpath"
#     click_hotel_button_xpath = "(//span[.='Hotels'])[2]"
#     click_search_input_field_xpath = "(//input[contains(@placeholder,'Search')])[1]"
#     click_remove_button_xpath = "(//div[@class='SS0SXe'])[2]"
#     enter_city_xpath = "//input[@value='']"
#     check_in_date = "//div[@class='BLohnc q5Vmde']"
#     check_in_date_2 = "(//input[@jsname='yrriRe'])[3]"
#     hotel_names_xpath = "//div[@class='pjDrrc']//h2"
#     click_hotel_xpath = "//a[@class='PVOOXe']"
#     click_prices_button_xpath = "//span[contains(text(),'Prices')]"
#
#
#     @pytest.mark.usefixtures("setup")
#     def test_scrapper(self, setup):
#         self.driver = setup
#         wait = WebDriverWait(self.driver, 40)
#         wait.until(EC.element_to_be_clickable((self.locator_type, self.click_hotel_button_xpath))).click()
#         wait.until(EC.element_to_be_clickable((self.locator_type, self.click_search_input_field_xpath))).click()
#         wait.until(EC.element_to_be_clickable((self.locator_type, self.click_remove_button_xpath))).click()
#
#         enter_city_element = wait.until(EC.element_to_be_clickable((self.locator_type, self.enter_city_xpath)))
#         enter_city_element.send_keys(CITY_NAME)
#         enter_city_element.send_keys(Keys.RETURN)
#
#         wait.until(EC.element_to_be_clickable((self.locator_type, self.check_in_date))).click()
#
#         enter_checkin_date = wait.until(EC.element_to_be_clickable((self.locator_type, self.check_in_date_2)))
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", enter_checkin_date)
#         today = date.today().strftime("%Y-%m-%d")
#         enter_checkin_date.send_keys(today)
#         enter_checkin_date.send_keys(Keys.RETURN)
#
#         time.sleep(3)
#
#         hotel_names = self.driver.find_elements(self.locator_type, self.hotel_names_xpath)
#         hotel_links = self.driver.find_elements(self.locator_type, self.click_hotel_xpath)
#
#         for i, hotel_name in enumerate(hotel_names):
#             try:
#                 print(f"Hotel: {hotel_name.text}")
#
#                 hotel_link = wait.until(EC.element_to_be_clickable((self.locator_type, f"({self.click_hotel_xpath})[{i+1}]")))
#                 hotel_link.click()
#
#                 time.sleep(4)
#
#                 wait.until(EC.element_to_be_clickable((self.locator_type, self.click_prices_button_xpath))).click()
#
#                 self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 time.sleep(4)
#
#                 price_source_website_list = self.driver.find_elements("xpath", "//span[@class='NiGhzc']")
#                 prices_list_from_different_websites = self.driver.find_elements("xpath", "//span[@class='pNExyb']")
#
#                 d = {
#                     names_of_websites.text: prices_list_from_different_websites.text
#                     for names_of_websites, prices_list_from_different_websites in
#                     zip(price_source_website_list, prices_list_from_different_websites)
#                 }
#                 print(d)
#
#                 self.driver.back()
#                 time.sleep(3)
#
#             except TimeoutException:
#                 print(f"Timeout clicking hotel link {i+1}. Skipping to the next hotel.")
#                 self.driver.back()
#                 time.sleep(3)
#                 continue
#
import os
from datetime import date
import time
import json
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CITY_NAME = "Dubai"

class TestCrawler:

    locator_type = By.XPATH
    click_hotel_button_xpath = "(//span[.='Hotels'])[2]"
    click_search_input_field_xpath = "(//input[contains(@placeholder,'Search')])[1]"
    click_remove_button_xpath = "(//div[@class='SS0SXe'])[2]"
    enter_city_xpath = "//input[@value='']"
    check_in_date = "//div[@class='BLohnc q5Vmde']"
    check_in_date_2 = "(//input[@jsname='yrriRe'])[3]"
    hotel_names_xpath = "//div[@class='pjDrrc']//h2"
    click_hotel_xpath = "//a[@class='PVOOXe']"
    click_prices_button_xpath = "//span[contains(text(),'Prices')]"
    view_more_prices_xpath = "//button[@jsname='wQivvd']"
    next_page_button_xpath = "//span[.='Next']"

    @pytest.mark.usefixtures("setup")
    def test_scrapper(self, setup):
        self.driver = setup
        wait = WebDriverWait(self.driver, 40)

        wait.until(EC.element_to_be_clickable((self.locator_type, self.click_hotel_button_xpath))).click()
        wait.until(EC.element_to_be_clickable((self.locator_type, self.click_search_input_field_xpath))).click()
        wait.until(EC.element_to_be_clickable((self.locator_type, self.click_remove_button_xpath))).click()

        enter_city_element = wait.until(EC.element_to_be_clickable((self.locator_type, self.enter_city_xpath)))
        enter_city_element.send_keys(CITY_NAME)
        enter_city_element.send_keys(Keys.RETURN)
        wait.until(EC.element_to_be_clickable((self.locator_type, self.check_in_date))).click()

        enter_checkin_date = wait.until(EC.element_to_be_clickable((self.locator_type, self.check_in_date_2)))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", enter_checkin_date)
        today = date.today().strftime("%Y-%m-%d")
        enter_checkin_date.send_keys(today)
        enter_checkin_date.send_keys(Keys.RETURN)

        os.makedirs("hotel_data", exist_ok=True)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join("hotel_data", f"hotel_prices_{timestamp}.json")

        hotel_data = {}

        while True:
            time.sleep(3)

            hotel_names = self.driver.find_elements(self.locator_type, self.hotel_names_xpath)
            hotel_links = self.driver.find_elements(self.locator_type, self.click_hotel_xpath)

            for i, hotel_name in enumerate(hotel_names):
                try:
                    hotel_name_text = hotel_name.text.replace("\n", " ")
                    hotel_data[hotel_name_text] = {}

                    hotel_link = wait.until(EC.element_to_be_clickable((self.locator_type, f"({self.click_hotel_xpath})[{i+1}]")))
                    hotel_link.click()

                    time.sleep(4)

                    wait.until(EC.element_to_be_clickable((self.locator_type, self.click_prices_button_xpath))).click()

                    try:
                        view_more_button = wait.until(EC.element_to_be_clickable((self.locator_type, self.view_more_prices_xpath)))
                        view_more_button.click()
                        time.sleep(2)
                    except (TimeoutException, NoSuchElementException):
                        pass

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)

                    price_source_website_list = self.driver.find_elements("xpath", "//span[@class='NiGhzc']")
                    prices_list_from_different_websites = self.driver.find_elements("xpath", "//span[@class='pNExyb']")

                    for names_of_websites, prices_list_from_different_websites in zip(price_source_website_list, prices_list_from_different_websites):
                        website_name = names_of_websites.text.replace("\n", " ")
                        price_text = self.driver.execute_script(
                            "return arguments[0].innerHTML.match(/<span class=\"nDkDDb\">(.*?)<\\/span>/)[1];",
                            prices_list_from_different_websites
                        )
                        price_text = price_text.encode('utf-8').decode('unicode_escape')

                        hotel_data[hotel_name_text][website_name] = price_text

                    self.driver.back()
                    time.sleep(3)

                except TimeoutException:
                    self.driver.back()
                    time.sleep(3)
                    continue

            with open(filename, "w") as f:
                json.dump(hotel_data, f, indent=4)

            print(f"Hotel data saved to {filename}")

            try:
                next_button = self.driver.find_element(self.locator_type, self.next_page_button_xpath)
                if next_button.is_displayed():
                    next_button.click()
                    time.sleep(3)
                else:
                    break
            except NoSuchElementException:
                break