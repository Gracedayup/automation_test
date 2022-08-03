# coding=utf-8

import os
import base64
import json
import time
from common.handle_requests import HandleRequest
from common.handle_data import HandleFileData
from common.project_path import project_path
from utils.image_convert_text import ImageConvertText
from common.handle_log import logger


class GetToken(object):
    def __init__(self):
        self.request = HandleRequest()
        self.filedata = HandleFileData(f"config/config.yml").read_yaml()
        self.url = self.filedata["server"]["flow_base_url"]
        self.login_url = self.filedata["server"]["login_url"]
        self.headers = {'Content-Type': 'application/json;charset=UTF-8'}
        self.username = self.filedata["account"]["flow_username"]
        self.password = self.filedata["account"]["flow_password"]
        self.verify_code = ""
        self.verify_code_key = ""

    def get_token(self):
        """

        :return:
        """
        retry_time = 0
        res = self.verify_and_login()
        while retry_time < 3:
            if res.status_code != 200 or res.json()['code'] != 10000:
                logger.error("------------请求失败，重试第{0}次-------------".format(retry_time + 1))
                res = self.verify_and_login()
                retry_time += 1
                time.sleep(1)
            else:
                break
        return res

    def verify_and_login(self):
        """
        使用识别的验证码登录平台
        :return: 登录响应结果
        """
        image_base64, self.verify_code_key = self.get_verify_code()
        image = self.recognize_text(image_base64)
        res = self.login_flow()
        logger.info("响应结果：{0}".format(res.text))
        return res

    def login_flow(self):
        """
        flow平台登录接口
        :return:登录接口返回的结果
        """
        login_url = self.url + self.login_url
        data = {
                "password": self.password,
                "userName": self.username,
                "verifyCodeKey": self.verify_code_key,
                "verifyCodeValue": self.text
                }
        logger.info("发送的data:{0}".format(data))
        res = self.request.handle_request(url=login_url, method="post", data=json.dumps(data), headers=self.headers)
        return res

    def get_verify_code(self):
        """
        请求验证码接口
        :return:接口响应结果：image_base64, verify_code_key
        """
        url = str(self.url) + "/user/getVerifyCode"
        res = self.request.handle_request(url=url, method="get")
        image_base64 = str(res.json()["data"]["imageBase64"]).split("base64,")[1]
        self.verify_code_key = res.json()["data"]["verifyCodeKey"]
        return image_base64, self.verify_code_key

    def recognize_text(self, image_base64):
        """
        image base64转换为jpg文件
        :param image_base64:image base64
        :return:图片文件
        """
        convert_filename = "verifycode.jpg"
        verifycode_file = os.path.join(project_path, "verifycode")
        image_url = os.path.join(verifycode_file, convert_filename)
        if not os.path.exists(verifycode_file):
            os.mkdir(verifycode_file)
        with open(file=image_url, mode="wb") as f:
            f.write(base64.b64decode(image_base64))
        self.text = ImageConvertText().image_convert_text(image_url)
        return self.text


if __name__ == '__main__':
    token = GetToken()
    # image_base64, _ = token.get_verify_code()
    # print(token.recognize_text(image_base64))
    result = token.get_token()
    print("登录接口返回信息，{0}".format(result.json()))







