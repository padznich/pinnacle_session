#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


# Setup
customer = "hello"
passw = "world"
phantomjs_path = "C:\Users\ASUS\Code\pinnacle_session\driver\phantomjs.exe"
conf_path = "C:\Users\ASUS\Code\pinnacle_session\conf\conf.ini"

uri_login = "https://www.pinnacle.com/en/login"
uri_bjmh = "https://www1.pinnacle.com/Casino/MS/BJMH/0"


def init_driver(_phantomjs_path=None):
    """
    At drivers-folder PhantomJS for Linux and Windows
    :param _phantomjs_path:
    :return:
    """
    driver = webdriver.PhantomJS(_phantomjs_path)
    driver.wait = WebDriverWait(driver, 10)
    return driver


def login(_driver, _customer, _password):

    _driver.get(uri_login)
    try:
        customer_form = _driver.wait.until(ec.presence_of_element_located(
            (By.NAME, "CustomerId")))
        password_form = _driver.wait.until(ec.presence_of_element_located(
            (By.NAME, "Password")))
        button = _driver.wait.until(ec.element_to_be_clickable(
            (By.NAME, "loginSubmit")))
        customer_form.send_keys(_customer)
        password_form.send_keys(_password)
        button.click()
    except TimeoutException:
        print("Login Failed.")


def get_session_uri(_driver):

    # Short way
    login(_driver, customer, passw)
    time.sleep(1)
    _driver.get(uri_bjmh)
    time.sleep(1)

    page_html_unicode = _driver.page_source
    _driver.quit()

    page_html_str = page_html_unicode.encode('utf-8')
    page_html_str = "".join([i for i in page_html_str.split("\n")])

    session = re.match(r"(.*)Token=(\w+)&amp(.*)", page_html_str)

    return session.groups()[1]


def update_conf_session(session):

    with open(conf_path, "r") as f:

        old_lines_list = []
        for line in f.readlines():
            if line[:7] == "session":
                line = "session={}\n".format(session)
            old_lines_list.append(line)
        new_text = "".join(old_lines_list)

    with open(conf_path, "w") as f:
        f.write(new_text)


def update_session():
    """
    Function for parser.py
    :return:
    """
    _d = init_driver(phantomjs_path)
    session = get_session_uri(_d)

    update_conf_session(session)


if __name__ == "__main__":

    update_session()
