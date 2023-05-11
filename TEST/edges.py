from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get("http://127.0.0.1:8000/")



username = "blog_personal1"
password = "blogABC@123"
driver.find_element("id", "inputUsername").send_keys(username)
driver.find_element("id", "inputPassword").send_keys(password)
driver.find_element("name", "btn_signin").click()

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
# error-code
errors = driver.find_element("css selector", ".error-code")

print(errors.text)