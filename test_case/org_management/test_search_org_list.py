# – coding: utf-8 --
"""
@Time : 2022/6/23 17:37
@Author : sunny cao
@File : test_search_org_list.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：组织管理")
@allure.story("查询组织列表")
class TestSearchOrg(object):
    @allure.title("查询组织列表-按名称排序")
    @allure.description("查询组织列表-按名称排序")
    def test_001_search_org_by_name(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByName"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10

    @allure.title("查询组织列表-按名称排序，关键字查询")
    @allure.description("查询组织列表-按名称排序，关键字查询")
    def test_002_search_org_by_name(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByName"
        param = {
            'keyword': "org41"
        }
        res = request.handle_request(method="get", url=url, params=param, headers=headers)
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"

    @allure.title("查询组织列表-按数据总数排序")
    @allure.description("查询组织列表-按数据总数排序")
    def test_001_search_org_by_total_data(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByTotalData"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10

    @allure.title("查询组织列表-按数据总数排序-关键字查询")
    @allure.description("查询组织列表-按数据总数排序-关键字查询")
    def test_002_search_org_by_total_data(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByTotalData"
        param = {
            'keyword': 'org'
        }
        res = request.handle_request(url=url, method="get", headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.text))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10

    @allure.title("查询组织列表-按活跃度")
    @allure.description("查询组织列表-按活跃度")
    def test_001_search_org_by_activity(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByActivity"
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.text))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10

    @allure.title("查询组织列表-按活跃度排序-关键字查询")
    @allure.description("查询组织列表-按活跃度排序-关键字查询")
    def test_002_search_org_by_activity(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByActivity"
        param = {
            'size': 2
        }
        res = request.handle_request(url=url, method="get", params=param)
        logger.info("接口响应结果：{}".format(res.text))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 2

    @allure.title("查询组织列表-按算力（内存）排序")
    @allure.description("查询组织列表-按算力（内存）排序")
    def test_001_search_org_by_memory(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByMemory"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.text))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10

    @allure.title("查询组织列表-按算力（内存）排序-关键字查询")
    @allure.description("查询组织列表-按算力（内存）排序-关键字查询")
    def test_002_search_org_by_memory(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/listOrgInfoByMemory"
        param = {
            'keyword': 'org'
        }
        res = request.handle_request(url=url, method="get", params=param)
        logger.info("接口响应结果：{}".format(res.text))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        assert res.json()["data"]["size"] == 10













