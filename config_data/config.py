from environs import Env
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium_stealth import stealth


def load_config(path: str | None = None):
    """Loading login and password from the virtual environment"""
    env = Env()
    env.read_env(path)
    username = env('username_')
    password = env('password')
    path_to_profile = env('path_to_profile')
    path_to_webdriver = env('path_to_webdriver')
    return username, password, path_to_profile, path_to_webdriver


def create_driver_instance():
    """Creating a driver object"""
    _path_to_profile = load_config()[2]
    _path_to_webdriver = load_config()[3]
    _options = webdriver.ChromeOptions()

    # background mode
    _options.add_argument("--headless")

    # stealth arguments
    _options.add_argument("start-maximized")
    _options.add_experimental_option("excludeSwitches", ["enable-automation"])
    _options.add_experimental_option('useAutomationExtension', False)

    # Saving session data in the profile (works only with the closed Chrome browser)
    _options.add_argument('--allow-profiles-outside-user-dir')
    _options.add_argument('--enable-profile-shortcut-manager')
    _options.add_argument(f'user-data-dir={_path_to_profile}')
    _options.add_argument(f'--profile-directory=Profile1')

    driver = webdriver.Chrome(options = _options,
                              service = Service(_path_to_webdriver))

    stealth(driver,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


def check_authorithation(self) -> bool:
    """Checking account authorization"""
    try:
        self.driver.find_element(By.NAME, 'password')
    except NoSuchElementException:
        return False
    return True


class InstagramBot():
    def __init__(self):
        self.username = load_config()[0]
        self.password = load_config()[1]
        self.driver = create_driver_instance()

    def close_browser(self):
        """method for closing the browser"""
        self.driver.close()
        self.driver.quit()

    def login(self):
        """login method"""
        self.driver.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))


        if check_authorithation(self):
            username_input = self.driver.find_element(By.NAME, 'username')
            username_input.clear()
            username_input.send_keys(self.username)
            time.sleep(random.randrange(1, 3))

            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.clear()
            password_input.send_keys(self.password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(random.randrange(3, 5))



if __name__ == '__main__':
    InstagramBot().login()
    InstagramBot().close_browser()
