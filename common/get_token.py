"""
@Time : 2022/6/16 10:58
@Author : sunny cao
@File : get_token.py
"""
import os
import base64
import json
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

        :return:登录接口返回的结果
        """
        login = GetToken()
        login.recognize_text()
        res = login.login_flow()
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

    def recognize_text(self):
        """
        识别验证码图片中的字符
        :return:None
        """
        login = GetToken()
        image_base64, self.verify_code_key = login.get_verify_code()
        image = login.b64_convert_image(image_base64)
        self.text = ImageConvertText().image_convert_text3(image)

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

    def b64_convert_image(self, image_base64):
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
        return image_url







