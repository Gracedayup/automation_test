# -*- coding: utf-8 -*-
"""
@Time : 2022/7/28 18:18
@Author : name
@File : conftest.py
"""
import time

import pytest
from selenium import webdriver
from setting import DRIVER
from setting import GLOBAL_TIMEOUT
from selenium.webdriver.remote.webelement import WebElement

drivers = {
    'chrome': webdriver.Chrome(),
    # 'edge': webdriver.Edge(executable_path='msedgedriver.exe'),
    'ie': None,
    'firefox': None,
    'Safari': None,
    '...': None
}

@pytest.fixture(scope="session", autouse=False)
def driver(request) -> WebElement:
    print("开始执行driver！")
    driver = drivers[DRIVER]
    driver.maximize_window()
    driver.implicitly_wait(GLOBAL_TIMEOUT)
    yield driver
    driver.close()




