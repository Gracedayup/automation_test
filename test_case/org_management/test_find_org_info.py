# – coding: utf-8 --
"""
@Time : 2022/6/24 11:54
@Author : sunny cao
@File : test_find_org_info.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：组织管理")
@allure.story("查询当前用户绑定的组织列表")
class TestFindOrgInfo(object):
    @allure.title("必填项为空，查询组织详细信息")
    @allure.description("必填项为空，查询组织详细信息")
    def test_001_get_org_info_without_id(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/findOrgInfo"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"

    @allure.title("查询组织详细信息")
    @allure.description("询组织详细信息")
    def test_002_et_org_info_success(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/findOrgInfo"
        param = {
            'identityId': 'test'
        }
        res = request.handle_request(url=url, method="get", params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"



