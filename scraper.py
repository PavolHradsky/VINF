from selenium import webdriver
from selenium.webdriver.common.by import By
url = "https://www.tripadvisor.com/Hotel_Review-g190454-d2557177-Reviews-Austria_Trend_Hotel_Doppio-Vienna.html"

driver = webdriver.Chrome()
driver.maximize_window()


driver.get(url)
pageSource = driver.page_source

text = driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")

with open("result.html", "w") as f:
    f.write(pageSource)
with open("result.txt", "w") as f:
    f.write(text)

driver.quit()