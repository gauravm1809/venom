import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://www.google.com/travel"


@pytest.fixture
def setup():
    chrome_driver_path = "/Users/gauravmishra/PycharmProjects/crawl-o-tron/drivers/chromedriver"
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
    driver.get(URL)
    yield driver
    driver.quit()
