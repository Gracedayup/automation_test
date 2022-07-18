# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 10:13
@Author : name
@File : test_query_project_details.py
"""
from common.handle_log import logger
import allure
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("查询项目详情")
class TestQueryProjectDetails(object):

    @allure.title("未登录状态，查询项目详情")
    @allure.description("未登录状态，查询项目详情")
    def test_001_query_project_details_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectDetails"
        res = request.handle_request(method="get", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("必填项为空，查询项目详情")
    @allure.description("必填项为空，查询项目详情")
    def test_002_query_project_details_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectDetails"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="get", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20001
        assert res.json()["msg"] == "project.id.notNull"

    @allure.title("成功查询项目详情")
    @allure.description("成功查询项目详情")
    def test_003_query_project_details_success(self, get_base_info, get_token, handle_mysql):
        # 查询数据库中该用户的项目id
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectDetails"
        access_token = get_token["data"]["token"]
        user_id = get_token["data"]["id"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        query_project_sql = "SELECT * FROM t_project WHERE status=1 and user_id=%s"
        query_project_result = handle_mysql.query_one(sql=query_project_sql, param=[user_id])
        # 调用查询项目详情接口
        param = {
            "id": query_project_result["id"]
        }
        res = request.handle_request(method="get", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        # 检查接口响应结果是否与数据库记录保持一致
        if res.json()["code"] == 10000:
           assert res.json()['data']["projectName"] == query_project_result["project_name"]
           assert res.json()["data"]["projectDesc"] == query_project_result["project_desc"]

    @allure.title("查询无权限查看的项目详情")
    @allure.description("查询无权限查看的项目详情")
    def test_004_query_project_details_without_permission(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectDetails"
        access_token = get_token["data"]["token"]
        user_id = get_token["data"]["id"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        query_sql = "SELECT * FROM t_project_member WHERE project_id not in (SELECT project_id FROM t_project_member WHERE user_id=%s)"
        query_project_result = handle_mysql.query_one(sql=query_sql, param=[user_id])
        param = {
            "id": query_project_result["id"]
        }
        res = request.handle_request(method="get", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] != 10000
        assert res.json()["msg"] != "成功"
