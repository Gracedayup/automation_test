# -*- coding: utf-8 -*-
"""
@Time : 2022/7/11 12:20
@Author : name
@File : login_page_locs.py
"""
from selenium.webdriver.common.by import By

class LoginPageLocs:
    # 用户名输入框
    home_login_btn = (By.XPATH, '//*[@id="dataExchange"]/div/div[1]/div[1]/div[3]/div')
    user_input = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[1]/div/div[1]/input')
    pwd_input = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[2]/div/div/input')
    captcha_input = (By.XPATH, '//*[@id="app"]/div/div/div[2]/div/form/div[3]/div/div/input')
    captcha = (By.CLASS_NAME, 'captcha')
    login_btn = (By.CLASS_NAME, '//*[@id="app"]/div/div/div[2]/div/form/div[4]/div/button')


