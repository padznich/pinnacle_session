
import re
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import TimeoutException

chromedriver = "C:\Users\ASUS\Code\pinnacle_session\libs\chromedriver.exe"

uri_login = "https://www.pinnacle.com/en/login"
uri_bjmh = "https://www1.pinnacle.com/Casino/MS/BJMH/0"
customer = "Hello"
passw = "World"


def init_driver(chromedriver_path=None):
    """
    At libs-folder ChromeDrives for Linux and Windows
    :param chromedriver_path:
    :return:
    """
    if not chromedriver_path:
        chromedriver_path = "/home/pad/code/blackjack-parser/libs/chromedriver"
    driver = webdriver.Chrome(chromedriver_path)
    driver.wait = WebDriverWait(driver, 10)
    return driver


def login(_driver, _customer, _password):

    _driver.get(uri_login)
    try:
        customer_form = _driver.wait.until(Ec.presence_of_element_located(
            (By.NAME, "CustomerId")))
        password_form = _driver.wait.until(Ec.presence_of_element_located(
            (By.NAME, "Password")))
        button = _driver.wait.until(Ec.element_to_be_clickable(
            (By.NAME, "loginSubmit")))
        customer_form.send_keys(_customer)
        password_form.send_keys(_password)
        button.click()
    except TimeoutException:
        print("Login Failed.")


def enter_casino(_driver,):

    try:
        button = _driver.wait.until(Ec.element_to_be_clickable(
            (By.XPATH, "//a[@href='https://www1.pinnacle.com/en/casino']")))
        button.click()
    except TimeoutException:
        print("Casino entering Failed.")


def enter_bjmh(_driver,):

    try:
        button = _driver.wait.until(Ec.element_to_be_clickable(
            (By.XPATH, "//a[@data-gamecode='BJMH']")))
        button.click()
    except TimeoutException:
        print("BJMH entering Failed.")


def click_coord(_driver, x=None, y=None, delay=None):

    if delay:
        time.sleep(delay)

    time.sleep(0.2)
    _driver.maximize_window()

    pyautogui.moveTo(x, y)
    pyautogui.click()


def get_session_uri(d):

    # Short way
    login(d, customer, passw)
    time.sleep(5)
    d.get(uri_bjmh)
    click_coord(d, 1155, 365, 30)  # Close frame
    click_coord(d, 1480, 75, 2)  # Click Options
    click_coord(d, 1480, 265, 2)  # Click History

    d.switch_to.window(d.window_handles[1])
    uri_session = d.current_url

    d.quit()
    session = re.match(r"(.*GameSession=)(.*)(.{3})", uri_session)
    return session.groups(2)[1]

if __name__ == "__main__":

    _d = init_driver(chromedriver)
    print get_session_uri(_d)
