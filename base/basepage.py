# -*- coding: utf-8 -*-
"""
@Time : 2022/7/1 17:45
@Author : name
@File : basepage.py
"""
import datetime

from common.handle_log import logger
from setting import IMAGE_DIR, GLOBAL_TIMEOUT, FREQUENCY

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

    def find_element_presence(self, loc, timeout=GLOBAL_TIMEOUT, frequency=FREQUENCY, mark=None):
        """
        等待页面元素存在
        """
        logger.info("在{}等待元素{}存在：".format(mark, loc))
        try:
            return WebDriverWait(self.driver, timeout, frequency).until(EC.presence_of_element_located(loc))
        except:
            logger.exception("查找元素失败！")
            self.save_imgs(mark)

    def find_element(self, loc, mark=None):
        """
        查找元素
        """
        logger.info("{}查找元素{}".format(mark, loc))
        try:
            return self.driver.find_element(*loc)
        except:
            logger.exception("查找元素失败！")
            self.save_imgs(mark)
            raise

    def find_elements(self, loc, mark=None):
        """
        查找元素集
        """
        logger.info("{}查找元素{}".format(mark, loc))
        try:
            return self.driver.find_elements(*loc)
        except:
            logger.exception("查找元素失败！")
            self.save_imgs(mark)
            raise

    def input_text(self, loc, text, mark=None):
        """
        输入框输入文本
        """
        ele = self.find_element_presence(loc=loc, mark=mark)
        logger.info("{}在元素{}中输入文本：{}".format(mark, loc, text))
        try:
            ele.send_keys(text)
        except:
            logger.exception("输入操作失败")
            self.save_imgs(mark)
            raise

    def clear_input_text(self, loc, mark=None):
        """
        清除文本框内容
        """
        ele = self.find_element_presence(loc=loc, mark=mark)
        logger.info("{} 在元素 {} 中清除".format(mark, loc))
        try:
            ele.clear()
            ele.send_keys("")
        except:
            logger.exception("清除操作失败")
            self.save_imgs(mark)
            raise

    def click_element(self, loc, mark=None):
        """
        点击元素
        """
        ele = self.find_element_presence(loc=loc, mark=mark)
        logger.info("{}在元素{}中输点击".format(mark, loc))
        print("查找出的元素：{}".format(ele))
        try:
            ele.click()
        except:
            logger.exception("点击操作失败")
            self.save_imgs(mark)
            raise

    def save_imgs(self, mark=None):
        current_time = int(datetime.datetime.now())
        img_path = '{}/{}_{}.png'.format(IMAGE_DIR, mark, current_time)
        try:
            self.driver.save_screenshot(img_path)
            logger.info("截屏成功，图片路径为{}".format(img_path))
        except:
            logger.exception("截屏失败")


