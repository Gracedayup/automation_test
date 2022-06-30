# – coding: utf-8 --
"""
@Time : 2022/6/22 12:19
@Author : sunny cao
@File : test_data_list.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：数据管理")
@allure.story("数据列表")
class TestDataPageList(object):
    @allure.title("未登录状态，查询所有数据")
    @allure.description("查询所有已发布数据")
    def test_get_all_data(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/data/pageList"
        res = request.handle_request(method="get", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        sql = "SELECT count(*) FROM dc_meta_data WHERE status = %s"
        result = handle_mysql.query_data(sql=sql, param=[2])
        if res.json()["msg"] == "成功":
            assert res.json()["data"]["total"] == result[0]["count(*)"]
            assert res.json()["data"]["size"] == 10

    @allure.title("关键字查询已发布的数据")
    @allure.description("关键字查询已发布的数据")
    def test_get_data_by_keywords(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/data/pageList"
        param = {
            'current': 1,
            'dataName': 'part'
        }
        res = request.handle_request(method="get", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"





