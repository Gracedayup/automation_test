# -*- coding: utf-8 -*-
"""
@Time : 2022/7/28 18:16
@Author : name
@File : login_page.py
"""
import time

from page_locators.login_page_locs import LoginPageLocs as loc
from base.basepage import BasePage
from base.get_token import GetToken


class LoginPage(BasePage):
    def login(self, username, password):
        self.click_element(loc.home_login_btn, "首页_点击登录按钮")
        # 识别验证码
        time.sleep(2)
        captcha_base64 = self.find_element_presence(loc=loc.captcha).get_attribute("src").split("base64,")[1]
        captcha_text = GetToken().recognize_text(captcha_base64)
        self.input_text(loc.user_input, username, "登录页面_输入用户名")
        self.input_text(loc.pwd_input, password, "登录页面_输入密码")
        self.input_text(loc.captcha_input, captcha_text, "登录页面_输入验证码")
        self.click_element(loc.login_btn, "登录页面_点击登录按钮")
