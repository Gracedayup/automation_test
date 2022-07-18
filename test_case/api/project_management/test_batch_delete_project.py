# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 14:31
@Author : name
@File : test_batch_delete_project.py
"""

import json
from common.handle_log import logger
import allure
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("批量删除项目")
class TestBatchDeleteProject(object):
    @allure.title("未登录状态，批量删除项目")
    @allure.description("未登录状态，批量删除项目")
    def test_001_batch_delete_project_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/deleteProjectBatch"
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("成功批量删除项目")
    @allure.description("成功批量删除项目")
    def test_002_batch_delete_project_success(self, get_base_info, get_token, handle_mysql):
        # 删除用于自动化测试的数据，project_name以test开头
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/project/deleteProjectBatch"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询该用户下的项目
        user_id = get_token["data"]["id"]
        query_sql = 'select a.id as id,a.project_name as projectName,a.project_desc as projectDesc,a.create_time as createTime,b.role as role,(select u.user_name from t_user u where u.status = 1 and u.id = a.user_id) as userName from t_project a, t_project_member b where a.id = b.project_id and b.user_id =%s and project_name like "test%%" and b.role=1'
        project_result = handle_mysql.query_data(sql=query_sql, param=[user_id])
        if project_result:
            project_id = []
            for i in range(0, len(project_result)):
                project_id.append(project_result[i]["id"])
            ids = ','.join(str(i) for i in project_id)
            param = {
                "ids": ids
            }
            res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
            logger.info("接口响应结果：{}".format(res.json()))
            assert res.json()["code"] == 10000

    @allure.title("批量删除当前用户下无权限操作的项目")
    @allure.description("批量删除当前用户下无权限操作的项目")
    def test_003_batch_delete_project_without_permission(self, get_base_info, get_token, handle_mysql):
        # 删除用于自动化测试的数据，project_name以test开头
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/project/deleteProjectBatch"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询该用户下的项目
        user_id = get_token["data"]["id"]
        query_sql = 'select a.id as id,a.project_name as projectName,a.project_desc as projectDesc,a.create_time as createTime,b.role as role,(select u.user_name from t_user u where u.status = 1 and u.id = a.user_id) as userName from t_project a, t_project_member b where a.id = b.project_id and b.user_id =%s and project_name like "test%%" and b.role!=1'
        project_result = handle_mysql.query_data(sql=query_sql, param=[user_id])
        if project_result:
            project_id = []
            for i in range(0, len(project_result)):
                project_id.append(project_result[i]["id"])
            ids = ','.join(str(i) for i in project_id)
            param = {
                "ids": ids
            }
            res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
            logger.info("接口响应结果：{}".format(res.json()))
            assert res.json()["code"] == 20009



