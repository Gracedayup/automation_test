# – coding: utf-8 --
"""
@Time : 2022/6/21 16:46
@Author : sunny cao
@File : test_query_user_details.py
"""
import allure
from common.handle_log import logger


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
@allure.story("查询用户详情")
class TestQueryUserDetails(object):

    @allure.title("未登录状态，查询用户详情")
    @allure.description("未登录状态，查询用户详情")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_query_user_details_without_login(self, get_token, get_base_info):
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/user/queryUserDetails"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json'}
        data = {
                "address": address
               }
        res = request.handle_request(method="post", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("登录状态，输入不存在的address")
    @allure.description("登录状态，输入不存在的address")
    def test_query_user_details_address_not_exit(self, get_token, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/user/queryUserDetails"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        data = {
                "address": 123
               }
        res = request.handle_request(method="post", url=url, headers=headers, json=data)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"

    @allure.title("登录状态，查询用户详情")
    @allure.description("登录状态，查询用户详情")
    def test_query_user_details_success(self, get_token, get_base_info):
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/user/queryUserDetails"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        data = {
                "address": address
               }
        res = request.handle_request(method="post", url=url, headers=headers, json=data)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"

