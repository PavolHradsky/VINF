from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import re
import time
# first unscraped: Something in China

# Countries
base_url = "https://www.tripadvisor.com"
url = f"{base_url}/SiteIndex"

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ")
driver = uc.Chrome(options=options)

# First level
driver.delete_all_cookies()
driver.get(url)
pageSource = driver.page_source
driver.delete_all_cookies()

cont = True

with open("urls2.txt", "a") as f:
    regex = r"\bhref=\"(/SiteIndex-g[0-9]{3,}[^\"]*\.html)\""
    for country in re.finditer(regex, pageSource):
        url = f"{base_url}{country.groups()[0]}"
        print(url)
        if "United_States" in url:
            cont = False
        if cont:
            continue
        cont = True
        time.sleep(3)
        
        # Second level
        driver.get(url)
        pageSource = driver.page_source
        driver.delete_all_cookies()
        regex = r"\bhref=\"(/SiteIndex-[^\"]*Hotel_Review[^\"]*\.html)\""
        for page in re.finditer(regex, pageSource):
            url = f"{base_url}{page.groups()[0]}"
            print(url)
            time.sleep(3)

            # Third level
            driver.get(url)
            pageSource = driver.page_source
            driver.delete_all_cookies()

            regex = r"\bhref=\"(/SiteIndex-[^\"]*Hotel_Review[^\"]*\.html)\""
            for innerPage in re.finditer(regex, pageSource):
                url = f"{base_url}{innerPage.groups()[0]}"
                print(url)
                time.sleep(4)

                # Forth level
                driver.get(url)
                pageSource = driver.page_source
                driver.delete_all_cookies()
                    
                regex = r"\bhref=\"(/Hotel_Review-g[^\"]*\.html)\""
                for review in re.finditer(regex, pageSource):
                    url = f"{base_url}{review.groups()[0]}"
                    f.write(f"{url}\n")

            regex = r"\bhref=\"(/Hotel_Review-g[^\"]*\.html)\""
            for review in re.finditer(regex, pageSource):
                url = f"{base_url}{review.groups()[0]}"
                f.write(f"{url}\n")
        # break

driver.quit()

