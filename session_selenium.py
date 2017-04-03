#!/usr/bin/python
# -*- coding: utf-8 -*-

import ctypes
import re
import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import TimeoutException

from libs.conf_reader import creds


uri_login = "https://www.pinnacle.com/en/login"
uri_bjmh = "https://www1.pinnacle.com/Casino/MS/BJMH/0"
customer = creds.user
passw = creds.password


def init_driver(_driver_path=None):
    """
    At libs-folder ChromeDrives for Linux and Windows
    :param _driver_path:
    :return:
    """
    driver = webdriver.Chrome(_driver_path)
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


# Not Used
def enter_casino(_driver,):

    try:
        button = _driver.wait.until(Ec.element_to_be_clickable(
            (By.XPATH, "//a[@href='https://www1.pinnacle.com/en/casino']")))
        button.click()
    except TimeoutException:
        print("Casino entering Failed.")


# Not Used
def enter_bjmh(_driver,):

    try:
        button = _driver.wait.until(Ec.element_to_be_clickable(
            (By.XPATH, "//a[@data-gamecode='BJMH']")))
        button.click()
    except TimeoutException:
        print("BJMH entering Failed.")


def click_coord(_driver, x=None, y=None, delay=None):

    if not x and not y:
        x, y = 1, 1

    if delay:
        time.sleep(delay)

    time.sleep(0.2)
    _driver.maximize_window()

    pyautogui.moveTo(x, y)
    pyautogui.click()


def exec_clicks(_driver):

    metrics = ctypes.windll.user32

    resolution = [
        metrics.GetSystemMetrics(0),
        metrics.GetSystemMetrics(1),
    ]

    # 1024x768
    if resolution[0] == 1024 and resolution[1] == 768:

        time.sleep(2)
        click_coord(_driver, 905, 180)  # Never save password

        click_coord(_driver, 620, 316, 20)  # Close deposit frame
        click_coord(_driver, 800, 160)  # Click Options
        click_coord(_driver, 800, 265, 1)  # Click History

    # 1920x1080
    if resolution[0] == 1920 and resolution[1] == 1080:

        time.sleep(2)
        click_coord(_driver, 905, 180)  # Never save password

        click_coord(_driver, 1155, 365, 35)  # Close deposit frame
        click_coord(_driver, 1480, 75)  # Click Options
        click_coord(_driver, 1480, 265, 1)  # Click History


def get_session_uri(_driver):

    # Short way
    login(_driver, customer, passw)
    time.sleep(5)
    _driver.get(uri_bjmh)

    exec_clicks(_driver)

    _driver.switch_to.window(_driver.window_handles[1])
    uri_session = _driver.current_url

    _driver.quit()
    session = re.match(r"(.*GameSession=)(.*)(.{3})", uri_session)
    return session.groups()[1]


def update_conf_session(session):

    with open(creds.conf_path, "r") as f:

        old_lines_list = []
        for line in f.readlines():
            if line[:7] == "session":
                line = "session={}\n".format(session)
            old_lines_list.append(line)
        new_text = "".join(old_lines_list)

    with open(creds.conf_path, "w") as f:
        f.write(new_text)


def update_session():
    """
    Function for parser.py
    :return:
    """
    _d = init_driver(creds.driver_path)
    session = get_session_uri(_d)

    update_conf_session(session)


if __name__ == "__main__":

    update_session()