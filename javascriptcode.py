# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
#
# chrome_driver_path = "/Users/gauravmishra/PycharmProjects/crawl-o-tron/drivers/chromedriver"
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--start-maximized")
# driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
# driver.implicitly_wait(60)
# driver.get("https://upswing-grms-prod.web.app/login-password")
# driver.find_element("xpath", "//input[@name='signIn_username']").send_keys("gaurav@upswing.global")
# driver.find_element("xpath", "//input[@name='signInPassword']").send_keys("123456")
# driver.find_element("xpath", "//button[@label='Sign In']").click()
# sleep(6)
# driver.find_element("xpath", "//span[@aria-label='Organization']").click()
# driver.find_element("xpath", "//input[@role='searchbox']").send_keys("test_org_01")
# driver.find_element("xpath", "(//li[@role='option'])[1]").click()
# driver.find_element("xpath", "//p-dropdown[@placeholder='Property']").click()
# driver.find_element("xpath", "(//li[@role='option'])[1]").click()
# driver.find_element("xpath", "(//div[@class='card-title'])[2]").click()
# driver.find_element("xpath", "(//button[contains(@class,'p-ripple')])[4]").click()
#
# text = driver.execute_script("return document.querySelector('body > app-root > app-landing > app-users-list > div > div > div.ng-trigger.ng-trigger-panelState.ng-tns-c4029148367-4.side-bar-65rem.p-sidebar.p-sidebar-active.p-sidebar-right.ng-star-inserted > user-shared-form > div > form > div > div:nth-child(2) > div:nth-child(1) > div > span').textContent;")
# print(text)
# assert text == "test_user_01"
# driver.quit()














import requests

# Backend API URL
api_url = "https://backend.rmsplusapi.messerschmitt.cloud/admin/user/list"

# Headers
headers = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImMwYTQwNGExYTc4ZmUzNGM5YTVhZGU5NTBhMjE2YzkwYjVkNjMwYjMiLCJ0eXAiOiJKV1QifQ.eyJyIjowLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdXBzd2luZy1ncm1zLXByb2QiLCJhdWQiOiJ1cHN3aW5nLWdybXMtcHJvZCIsImF1dGhfdGltZSI6MTczNjMxNDE3MSwidXNlcl9pZCI6ImFEbDB2eEZudGdYYUpDVjloQnV4c3ZraUtvNzMiLCJzdWIiOiJhRGwwdnhGbnRnWGFKQ1Y5aEJ1eHN2a2lLbzczIiwiaWF0IjoxNzM2MzE3OTkyLCJleHAiOjE3MzYzMjE1OTIsImVtYWlsIjoiZ2F1cmF2QHVwc3dpbmcuZ2xvYmFsIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImdhdXJhdkB1cHN3aW5nLmdsb2JhbCJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ZHwzDTmqCj_h3eMAe_S2QW6u7oHfr6Xm87ZMMWgq64QqdnnJJ3GAE8-PFzATNMKVHOu3CPsrKYn3jT-Ujk-gKKhMhBq0TS1j-jGLshqMrEK6UE1KN7rm_FQUb4krfIXC6xsjJI6ui41SbbBCEeXSz7Y8P8I3r-8SZDwdCgc7KBSXOUh9KfdKqINSoAH3_sxmW31XvfW2Rm42u52YZcCKdJKqkBD5queXyZSFuRwOz1YRxLq7RfOXbduP3dyGYliKjPk-Xx7x8OPkiMmWbbD7u0MzbO_cOPGbpCgZA9jFydu6lpEFzk65dYVW69K_umIIDfWPI8i2hKQ0UjMUKEFMhQ",  # Replace with your actual token
    "Content-Type": "application/json"
}

# Payload (if required by the API)
payload = {
  "orgId": "676e867075a210651f269d69",
    "page": "1",
    "pageSize": "10",
    "propertyId": "676e867b75a210651f269d6f",
    "searchString": "",
    "uid": ""

}

# Make a POST request
response = requests.post(api_url, headers=headers, json=payload)

# Validate API response
assert response.status_code == 200, f"API call failed with status code {response.status_code}"
backend_data = response.json()
print(backend_data)
# Example: Validate specific data in the API response
# expected_value = "test_user_01"
# assert backend_data.get("key") == expected_value, f"Text mismatch! Expected: {expected_value}, Found: {backend_data.get('key')}"

