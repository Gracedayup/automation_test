# – coding: utf-8 --
"""
@Time : 2022/6/24 11:17
@Author : sunny cao
@File : test_org_list.py
"""

import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：组织管理")
@allure.story("查询当前用户绑定的组织列表")
class TestOrgList(object):
    @allure.title("未登录状态，查询当前用户绑定的组织信息")
    @allure.description("未登录状态，查询当前用户绑定的组织信息")
    def test_001_get_org_list_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/list"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("登录状态，查询当前用户绑定的组织信息")
    @allure.description("登录状态，查询当前用户绑定的组织信息")
    def test_002_get_org_list(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/org/list"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            value_one = res.json()["data"][0]
            # 查看接口响应的结果中是否有包含字段
            expect_key = ["nodeName", "identityId", "identityIp"]
            for i in range(0, len(expect_key)):
                value = dict(value_one).get(expect_key[i])
                assert value != None


