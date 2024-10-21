import re
import time

from utils import create_driver


def crawl_urls(ase_url: str, url: str):
    with create_driver() as driver:
        # First level
        driver.delete_all_cookies()
        driver.get(url)
        pageSource = driver.page_source
        driver.delete_all_cookies()

        # cont = True

        with open("urls2.txt", "a") as f:
            regex = r"\bhref=\"(/SiteIndex-g[0-9]{3,}[^\"]*\.html)\""
            for country in re.finditer(regex, pageSource):
                url = f"{base_url}{country.groups()[0]}"
                print(url)
                # if "United_States" in url:
                #     cont = False
                # if cont:
                #     continue
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

if __name__ == "__main__":
    # Countries
    base_url = "https://www.tripadvisor.com"
    url = f"{base_url}/SiteIndex"

    crawl_urls(base_url, url)
