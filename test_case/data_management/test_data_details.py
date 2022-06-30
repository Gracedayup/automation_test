# – coding: utf-8 --
"""
@Time : 2022/6/22 15:24
@Author : sunny cao
@File : test_data_details.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：数据管理")
@allure.story("数据详情")
class TestDataDetails(object):

    @allure.title("查询数据文件信息")
    @allure.description("根据元数据ID，查询数据文件信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_data_details(self, get_base_info, handle_mysql):

        base_url, request = get_base_info
        url = base_url + "/data/getDataFile"
        get_data_sql = "SELECT * FROM dc_meta_data WHERE status = %s"
        get_data_result = handle_mysql.query_one(sql=get_data_sql, param=[2])
        param = {
            'metaDataId': get_data_result["meta_data_id"]
        }
        res = request.handle_request(url=url, method="get", params=param, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["msg"] == "成功":
            res.json()["data"]["identityId"] == get_data_result["identity_id"]
            res.json()["data"]["size"] == get_data_result["size"]
            res.json()["data"]["rows"] == get_data_result["rows"]
            res.json()["data"]["columns"] == get_data_result["columns"]

    @allure.title("元数据ID为空，查询数据文件信息")
    @allure.description("元数据ID为空，查询数据文件信息")
    def test_get_data_details_without_id(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/data/getDataFile"
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20001
        assert res.json()["msg"] == "metadata id can not be empty"
