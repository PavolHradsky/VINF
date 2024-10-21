import re
import time
import os
import random

from utils import create_driver


def create_shuffled_list(all_urls_path: str, shuffled_urls_path: str, num: int = 1000):
    if not os.path.exists(shuffled_urls_path):
        with open(all_urls_path, 'r') as src, open(shuffled_urls_path, 'w+') as dest:
            lines = src.readlines()
            random.shuffle(lines)
            lines = lines[:num]
            dest.writelines(lines)


def is_blocked(page_source: str):
    return not not len(re.findall(r"'host':'geo\.captcha-delivery.com'", page_source))


def scrape_all(html_dir: str, shuffled_urls_path: str, sleep: int = 4):
    blocked = 0
    htmls_usa = os.listdir(html_dir)

    with open(shuffled_urls_path, 'r') as src:
        with create_driver() as driver:
            lines = src.readlines()
            for i, line in enumerate(lines):
                print(i)
                name = line.split("/")[3]
                if name in htmls_usa:
                    print(f"Skipping: {line}")
                    continue

                driver.get(line)
                pageSource = driver.page_source
                driver.delete_all_cookies()

                if is_blocked(pageSource):
                    print(f'Blocked: {line}')
                    blocked += 1
                    if blocked > 3:
                        break
                    time.sleep(sleep)
                    continue
                blocked = 0

                with open(f'data/htmls_usa/{name}', "w+") as html:
                    html.write(pageSource)

                print(line)
                time.sleep(sleep)


if __name__ == "__main__":
    create_shuffled_list('data/urls_usa.txt', 'data/shuffled_urls_usa.txt')
    scrape_all('./data/htmls_usa', 'data/shuffled_urls_usa.txt', sleep=4)