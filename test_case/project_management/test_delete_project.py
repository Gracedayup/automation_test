# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 11:22
@Author : name
@File : test_delete_project.py
"""
import json
from common.handle_log import logger
import allure
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("删除项目")
class TestDeleteProject(object):
    @allure.title("未登录状态，删除项目")
    @allure.description("未登录状态，删除项目")
    def test_001_delete_project_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/deleteProject"
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("成功删除项目")
    @allure.description("成功删除项目")
    def test_002_delete_project_success(self, get_base_info, get_token, handle_mysql):
        # 删除用于自动化测试的数据，project_name以test开头
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/project/deleteProject"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询该用户下的项目
        user_id = get_token["data"]["id"]
        query_sql = "SELECT id FROM t_project WHERE status=1 and project_name like 'test%%' and user_id=%s"
        project_id = handle_mysql.query_one(sql=query_sql, param=[user_id])
        print("该用户下的项目数据为：{0}".format(project_id))
        param = {
            "id": project_id["id"]
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        # # 数据库中查询数据是否被删除(status=0)
        # if res.json()["code"] == 10000:
        #     sql = "SELECT status FROM t_project where id = %s"
        #     query_result = handle_mysql.query_one(sql=sql, param=[project_id["id"]])
        #     print("删除后查询数据库中的结果为：{}".format(query_result))
        #     assert query_result["status"] == 0

    @allure.title("删除当前用户下无权限操作的项目")
    @allure.description("删除当前用户下无权限操作的项目")
    def test_003_delete_project_without_permission(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/project/deleteProject"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询当前用户无权限的用户
        user_id = get_token["data"]["id"]
        query_project_sql = "select a.id as id,a.project_name as projectName,a.project_desc as projectDesc,a.create_time as createTime,b.role as role,(select u.user_name from t_user u where u.status = 1 and u.id = a.user_id) as userName from t_project a, t_project_member b where a.id = b.project_id and b.user_id !=%s"
        query_project_result = handle_mysql.query_one(sql=query_project_sql, param=[user_id])
        param = {
            "id": query_project_result["id"]
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20009


