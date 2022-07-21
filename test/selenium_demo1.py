# -*- coding: utf-8 -*-
"""
@Time : 2022/7/1 15:02
@Author : name
@File : selenium_demo1.py
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

# – coding: utf-8 --
"""
@Time : 2022/6/22 12:17
@Author : sunny cao
@File : conftest.py
"""
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from setting import DRIVER, GLOBAL_TIMEOUT
from base.get_token import GetToken

drivers = {
    "chrome": webdriver.Chrome(),
    "edge": None,
    "ie": None,
    "firefox": None,
    "Safari": None
}

def driver() -> WebElement:
    driver = drivers[DRIVER]
    driver.get(url="http://10.10.8.177")
    driver.maximize_window()
    driver.implicitly_wait(GLOBAL_TIMEOUT)
    return driver


def login_flow():
    drivers = driver()
    login_button = drivers.find_element(By.XPATH, '//*[@id="dataExchange"]/div/div[1]/div[1]/div[3]/div')
    login_button.click()
    # 元素定位
    username = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[1]/div/div[1]/input')
    password = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[2]/div/div/input')
    captcha_input = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[3]/div/div/input')
    captcha = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[3]/div/img')
    # captcha = drivers.find_element(By.CLASS_NAME, 'captcha')
    captcha_base64 = captcha.get_attribute("src").split("base64,")[1]
    print("captcha_base64:", captcha_base64)
    # 识别验证码
    captcha_text = GetToken().recognize_text(captcha_base64)
    print("识别出的验证码：", captcha_text)

    login_btn = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[4]/div/button')
    # 输入用户名和密码
    username.send_keys("admin")
    password.send_keys("admin123456")
    captcha_input.send_keys(captcha_text)
    login_btn.click()

login_flow()






