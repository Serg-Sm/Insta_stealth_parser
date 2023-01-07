import os
import time
import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from config_data.config import create_driver_instance


"""
UPLOAD and PREPARE data
"""

def get_list_userpages() -> list:
    """Get a list of users"""
    with open(f'result/list_userpages.txt') as file:
        list_userpages = ''.join(file.readlines()).split('\n')

    return list_userpages


def create_directory(userpage) -> None:
    """Create directories for user"""
    if os.path.isdir(f"result/{userpage}"):
        print(f"The folder {userpage} already exists!")
    else:
        os.mkdir(f"result/{userpage}")


def get_followers_count(driver, xpath_number_followers) -> int:
    """Number of subscribers of the user"""
    followers_count = int(driver.find_element(By.XPATH, xpath_number_followers).text)
    loops_count = int(followers_count / 12)
    return loops_count


def scrol_page(driver, followers_dom, item: int) -> None:
    """Uploading subscribers on a popup"""
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_dom)
    time.sleep(random.randrange(1, 5))
    print(f"[+] Iteration #{item}")


def check_exists_by_xpath(driver, xpath) -> bool:
    """Checking the validity of the URL"""
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def write_to_file(userpage, list_followers) -> None:
    """Write a list of user urls to a file"""
    with open(f'result/{userpage}/followers.txt', 'a') as file:
        for post_url in list_followers:
            file.write(post_url + "\n")


"""
MAIN
"""

def get_followers_of_user() -> None:
    """Parsing subscribers of a user"""
    driver = create_driver_instance()
    list_userpages = get_list_userpages()

    for userpage in list_userpages:
        create_directory(userpage)
        driver.get(f'https://www.instagram.com/{userpage}/')
        time.sleep(3)

        xpath_number_followers = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span/span'
        xpath_button_followers = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div'
        xpath_popup = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]'

        loops_count = get_followers_count(driver, xpath_number_followers)
        print('Number of scrolls: ', loops_count)

        driver.find_element(By.XPATH, xpath_button_followers).click()
        time.sleep(3)
        followers_dom = driver.find_element(By.XPATH, xpath_popup)

        list_followers = []
        for item in range(0, loops_count):
            scrol_page(driver, followers_dom, item)
            time.sleep(2)

        all_urls_div = followers_dom.find_elements(By.TAG_NAME, "li")

        for url in all_urls_div:
            url = url.find_element(By.TAG_NAME, "a").get_attribute("href")
            list_followers.append(url)

        write_to_file(userpage, list_followers)

        print("Finish !!!")



if __name__ == '__main__':
    get_followers_of_user()