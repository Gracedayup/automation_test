# – coding: utf-8 --# – coding: utf-8 --
"""
@Time : 2022/6/27 17:10
@Author : sunny cao
@File : test_add_project.py
"""
import json
import pytest
from common.handle_log import logger
import allure
import time
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("新增项目")
class TestAddProject(object):

    @allure.title("未登录状态，新增项目")
    @allure.description("未登录状态，新增项目")
    def test_001_add_project_without_login(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/project/addProject"
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("必填项为空，新增项目")
    @allure.description("必填项为空，新增项目")
    def test_002_add_project_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        url = base_url + "/project/addProject"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        param = {
            "projectDesc": "",
            "projectName": "",
            "projectTempId": 0
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004
        assert res.json()["msg"] == "project name can not be empty"

    @allure.title("成功新增项目")
    @allure.description("成功新增项目")
    @pytest.mark.run(order=0)
    def test_003_add_project_success(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/project/addProject"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        project_name = "test" + str(int(time.time()))
        param = {
            "projectDesc": "",
            "projectName": project_name,
            "projectTempId": 0
        }
        res = request.handle_request(method="post", url=url, headers=headers, data= json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            # 检查数据库中是否已正确录入
            query_sql = "SELECT * FROM t_project WHERE project_name=%s"
            result = handle_mysql.query_data(sql=query_sql, param=[project_name])
            assert len(result) !=None

    @allure.title("新增项目-项目名已存在")
    @allure.description("新增项目-项目名已存在")
    def test_004_add_exist_project(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/project/addProject"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        user_id = get_token["data"]["id"]
        # 查询该用户已创建的项目数据
        query_sql = "SELECT * FROM t_project WHERE status=1 and user_id=%s"
        result = handle_mysql.query_one(sql=query_sql, param=[user_id])
        param = {
            "projectDesc": "",
            "projectName": result["project_name"],
            "projectTempId": 0
        }        
        res = request.handle_request(method="post", url=url, headers=headers, data= json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20009
        assert res.json()["msg"] == "项目名称已存在"
