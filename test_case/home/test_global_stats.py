# – coding: utf-8 --
"""
@Time : 2022/6/27 11:25
@Author : sunny cao
@File : test_global_stats.py
"""

from cgitb import reset
import allure
from common.handle_log import logger
import json
import pytest
import math

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：首页")
@allure.story("首页-查询全网资源概况")
class TestGlobalStats(object):
    @allure.title("查询全网资源概况")
    @allure.description("查询全网资源概况")
    def test_001_get_global_stats(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/home/globalStats"
        res = request.handle_request(method="get", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            value_one = res.json()["data"]
            # 查看接口响应的结果中是否有包含字段
            expect_key = ["totalOrgCount", "powerOrgCount", "dataFileSize", "usedDataFileSize"
                        , "taskCount", "partnerCount", "totalCore", "totalMemory","totalBandwidth"]
            for i in range(0, len(expect_key)):
                value = dict(value_one).get(expect_key[i])
                assert value != None
            # 检查响应结果数据的正确性
            qurey_sql = "select total_org_count, power_org_count, data_file_size, used_data_file_size, task_count, partner_count, total_core, total_memory, total_bandwidth from v_global_stats"
            result = handle_mysql.query_data(sql=qurey_sql)
            assert res.json()["data"]["powerOrgCount"] == result[0]["power_org_count"]
            assert res.json()["data"]["dataFileSize"] == result[0]["data_file_size"]
            assert res.json()["data"]["totalMemory"] == result[0]["total_memory"]
            assert res.json()["data"]["totalBandwidth"] == result[0]["total_bandwidth"]