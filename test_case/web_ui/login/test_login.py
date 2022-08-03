# -*- coding: utf-8 -*-
"""
@Time : 2022/7/28 18:15
@Author : name
@File : test_login.py
"""
import allure
from page_objects.login_page import LoginPage
from setting import login_url

@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
class TestLogin:
    def test_001_login_success(self, driver):
        driver.get(login_url)
        self.lg = LoginPage(driver)
        self.lg.login("admin", "admin123456")




