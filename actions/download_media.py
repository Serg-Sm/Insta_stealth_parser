import os
import time
import random

import requests
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


def get_list_posts(userpage) -> list:
    """Get the list of URLs of the user's posts"""
    with open(f'result/{userpage}.txt') as file:
        list_posts = ''.join(file.readlines()).split('\n')

    return list_posts


def create_directory(userpage) -> None:
    """Create directories for media files"""
    if os.path.isdir(f"result/{userpage}"):
        print(f"The folder {userpage} already exists!")
    else:
        os.mkdir(f"result/{userpage}")
        os.mkdir(f"result/{userpage}/image")
        os.mkdir(f"result/{userpage}/video")


def check_exists_by_xpath(driver, xpath) -> bool:
    """Checking the validity of the URL"""
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


"""
IMAGE
"""

def save_image(userpage, post_id, img_src_url, item=0) -> None:
    """Save picture file"""
    get_img = requests.get(img_src_url)
    with open(f"result/{userpage}/image/image_{post_id}_{item}.jpg", "wb") as img_file:
        img_file.write(get_img.content)


def save_list_image(userpage, list_images) -> None:
    """Save a list of downloaded files"""
    with open(f'result/{userpage}/{userpage}_images.txt', 'a') as file:
        for i in list_images:
            file.write(i + "\n")


def get_image_of_post(driver, post_url) -> str:
    """Downloading a photo from a user record"""
    driver.get(post_url)
    time.sleep(random.randrange(3, 5))

    img_src = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/img"
    img_src_url = driver.find_element(By.XPATH, img_src).get_attribute("src")

    return img_src_url


"""
VIDEO
"""

def get_video_of_post():
    """Collect post urls from a page into a file"""
    pass


"""
MAIN
"""

def download_content() -> None:
    """Upload photos and videos from the user page"""
    driver = create_driver_instance()
    list_userpages = get_list_userpages()

    for userpage in list_userpages:
        create_directory(userpage)
        list_posts = get_list_posts(userpage)
        list_images = []
        # list_video = []

        for i, post_url in enumerate(list_posts):
            if not post_url:
                print('FINISH !!!')
                break

            post_id = post_url.split("/")[-2]
            xpath_404 = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/h2'
            xpath_button = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/button'
            xpath_image = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/img'
            xpath_video = ''

            # xpath for the loop (instagram changes the link after the first picture)
            xpath_button_new = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/button[2]/div'
            xpath_image_new = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[3]/div/div/div/div/div[1]/img'
            xpath_video_new = ''

            driver.get(post_url)
            time.sleep(2)

            # Checking for a broken URL - "Sorry, this page is unavailable"
            if check_exists_by_xpath(driver, xpath_404):
                print(f'Wrong URL:  {i} - {post_url}')
                continue

            else:
                # Verification - photo or video
                if check_exists_by_xpath(driver, xpath_image):
                    img_src_url = driver.find_element(By.XPATH, xpath_image).get_attribute("src")
                    save_image(userpage, post_id, img_src_url)
                    list_images.append(f'image_{post_id}_0')
                    time.sleep(3)
                else:
                    pass

                # First click next foto
                if check_exists_by_xpath(driver, xpath_button):
                    driver.find_element(By.XPATH, xpath_button).click()
                    time.sleep(3)

                item = 0
                while True:
                    item += 1

                    # Verification - photo or video
                    if check_exists_by_xpath(driver, xpath_image_new):
                        img_src_url = driver.find_element(By.XPATH, xpath_image_new).get_attribute("src")
                        save_image(userpage, post_id, img_src_url, item)
                        list_images.append(f'image_{post_id}_{item}')
                        time.sleep(3)
                    else:
                        pass

                    # Checking for next foto
                    if check_exists_by_xpath(driver, xpath_button_new):
                        driver.find_element(By.XPATH, xpath_button_new).click()
                        time.sleep(3)
                    else:
                        break

            print(f'Post {i} is ready!')

        save_list_image(userpage, list_images)


if __name__ == '__main__':
    get_list_userpages()

