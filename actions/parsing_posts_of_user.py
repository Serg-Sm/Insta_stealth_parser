import random
import time

from selenium.webdriver.common.by import By

from config_data.config import create_driver_instance


"""
UPLOAD and UNLOAD data
"""

def get_url_users() -> list:
    """Get a list of URL users to collect posts"""
    with open('input_data/url_users.txt') as file:
        urls_list = file.readlines()

    return urls_list


def write_to_file(file_name: str, posts_urls: list) -> None:
    """Write a list of post URLs to a file"""
    with open(f'result/{file_name}.txt', 'a') as file:
        for post_url in posts_urls:
            file.write(post_url + "\n")

    with open(f'result/list_userpages.txt', 'a') as file:
        file.write(file_name)


"""
PROCESSING
"""

def get_posts_count(driver) -> int:
    """Number of records per page"""
    posts_count = int(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span").text.replace(',', ''))
    loops_count = int(posts_count / 12)
    return loops_count


def scrol_page(driver, i: int) -> None:
    """Loading posts on the page by scrolling"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randrange(1, 5))
    print(f"[+] Iteration #{i}")


def pars_urls_page(driver) -> list:
    """Parsing page urls"""
    hrefs = driver.find_elements(By.TAG_NAME, 'a')
    hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

    return hrefs


"""
MAIN
"""

def get_posts_of_user() -> None:
    """Collect post urls from a page into a file"""
    driver = create_driver_instance()
    urls_list = get_url_users()

    for url in urls_list:
        driver.get(url.replace('\n', ''))
        time.sleep(random.randrange(3, 7))

        loops_count: int = get_posts_count(driver)
        print('[+] Number of scrolls: ', loops_count)

        posts_urls = []
        for i in range(0, loops_count):
            hrefs: list = pars_urls_page(driver)

            for href in hrefs:
                if href in posts_urls:
                    continue
                else:
                    posts_urls.append(href)

            scrol_page(driver, i)

        file_name: str = url.split("/")[-2]

        write_to_file(file_name, posts_urls)


if __name__ == '__main__':
    get_url_users()
