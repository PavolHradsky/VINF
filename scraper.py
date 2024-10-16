from selenium import webdriver
import undetected_chromedriver as uc
import re
import time
import os
import random

if not os.path.exists('data/shuffled_urls.txt'):
    with open('data/urls.txt', 'r') as src, open('data/shuffled_urls.txt', 'w+') as dest:
        lines = src.readlines()
        random.shuffle(lines)
        lines = lines[:10000]
        dest.writelines(lines)


options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ")

blocked = 0


with open('data/shuffled_urls.txt', 'r') as src, open('data/scraped_urls.txt', 'a+') as dest:
    with uc.Chrome(options=options, version_main=129) as driver:
    # with webdriver.Chrome(options=options) as driver:
        lines = src.readlines()
        scraped_lines = dest.readlines()
        for line in lines:
            if line in scraped_lines:
                continue

            name = line.split("-Reviews-")[1]

            driver.get(line)
            pageSource = driver.page_source
            driver.delete_all_cookies()

            if len(re.findall(r"'host':'geo\.captcha-delivery.com'", pageSource)):
                print(f'Blocked: {line}')
                blocked += 1
                if blocked > 3:
                    break
                time.sleep(4)
                continue
            blocked = 0

            with open(f'data/htmls/{name}', "w+") as html:
                html.write(pageSource)

            print(line)
            dest.write(line)
            time.sleep(4)
