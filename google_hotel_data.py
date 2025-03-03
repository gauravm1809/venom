from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from datetime import datetime
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "/Users/gauravmishra/PycharmProjects/venom/drivers/chromedriver"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# # chrome_options.add_argument("--headless")
# # chrome_options.add_argument("--no-sandbox")
# # chrome_options.add_argument("--disable-dev-shm-usage")
# # chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--start-maximized")
#
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
# driver.get("https://www.google.com/travel/")
driver.implicitly_wait(60)
# driver.find_element("xpath", "(//button[@role='link'])[4]").click()
# driver.find_element("xpath", "(//input[@type='text'])[1]").click()
# driver.find_element("xpath", "(//div[@class='SS0SXe'])[2]").click()
# sleep(3)
# destination_name = driver.find_element("xpath", "(//input[@type='text'])[2]").send_keys("Dubai")
# driver.find_element("xpath", "(//input[@type='text'])[2]").send_keys(Keys.RETURN)
# driver.find_element("xpath", "//div[@class='BLohnc q5Vmde']").click()
# driver.find_element("xpath", "(//div[.='18'])[3]").click()
# driver.find_element("xpath", "(//div[.='20'])[3]").click()
# driver.find_element("xpath", "(//span[.='Done'])[1]").click()



driver.get("https://upswing-grms-dev.web.app/login-password")
driver.find_element("xpath", "//input[@name='signIn_username']").send_keys("gaurav@upswing.global")
driver.find_element("xpath", "//input[@name='signInPassword']").send_keys("123456")
driver.find_element("xpath", "//button[@label='Sign In']").click()
sleep(6)
driver.find_element("xpath", "//span[@aria-label='Organization']").click()
driver.find_element("xpath", "//input[@role='searchbox']").send_keys("man")
driver.find_element("xpath", "(//li[@role='option'])[1]").click()
driver.find_element("xpath", "//p-dropdown[@placeholder='Property']").click()
driver.find_element("xpath", "(//li[@role='option'])[1]").click()
driver.find_element("xpath", "(//div[@class='card-title'])[1]").click()
sleep(9)
t = driver.find_element("xpath", "(//p[@class='m-0 stats text-xl'])[1]").text
print(t)
sleep(9)
l = driver.find_element("xpath", "(//div[@class='p-paginator p-component ng-star-inserted']//span)[1]").text
d = l.split()
a = d[-1]
if t == a:
    print("verified")

driver.quit()

