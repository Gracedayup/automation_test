# – coding: utf-8 --
"""
@Time : 2022/6/27 11:10
@Author : sunny cao
@File : test_data_trend.py
"""

import allure
from common.handle_log import logger
import json
import pytest

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：首页")
@allure.story("首页-查询全网数据的月走势")
class TestDataTrend(object):
    @allure.title("查询全网数据的月走势")
    @allure.description("查询全网数据的月走势")
    def test_001_search_data_trend(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/home/dataTrend"
        res = request.handle_request(method="get", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            value_one = res.json()["data"][0]
            # 查看接口响应的结果中是否有包含字段
            expect_key = ["statsTime", "totalValue", "incrementValue"]
            for i in range(0, len(expect_key)):
                value = dict(value_one).get(expect_key[i])
                assert value != None