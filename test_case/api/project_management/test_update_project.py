# – coding: utf-8 --# – coding: utf-8 --
"""
@Time : 2022/6/27 18:10
@Author : sunny cao
@File : test_update_project.py
"""
import allure
import time
import json
from common.handle_log import logger
from base import project_management
headers = project_management.headers
url = project_management.update_project_url

@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("修改项目")
class TestUpdateProject(object):

    @allure.title("未登录状态，修改项目")
    @allure.description("未登录状态，修改项目")
    def test_001_update_project_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/updateProject"
        header = {'Content-Type': 'application/json'}
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"
    
    @allure.title("必填项为空，修改项目")
    @allure.description("必填项为空，修改项目")
    def test_002_update_project_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        param = {
            "projectDesc": "",
            "projectName": "",
            "projectTempId": 0
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004
        assert res.json()["msg"] == "project name can not be empty"

    @allure.title("成功修改项目")
    @allure.description("成功修改项目")
    def test_003_update_project_success(self, handle_mysql):
        # 查询当前登录用户拥有管理员权限的项目id
        _, project_ids = project_management.query_user_project(1)
        project_name = "test" + str(int(time.time()))
        print(f"当前登录用户拥有的管理员权限的项目id为：{project_ids[0]}")
        param = {
            "id": project_ids[0],
            "projectDesc": "",
            "projectName": project_name
        }
        # 更新项目名称
        res = project_management.request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        # 查询数据库中数据，是否变更
        query_sql = "SELECT * FROM t_project WHERE id=%s"
        query_result = handle_mysql.query_one(sql=query_sql, param=project_ids[0])
        assert query_result["project_name"] == project_name

    @allure.title("修改项目-项目名已存在")
    @allure.description("修改项目-项目名已存在")
    def test_004_update_exist_project(self, handle_mysql):
        # 查询当前登录用户拥有管理员权限的项目id
        _, project_ids = project_management.query_user_project(1)
        # 如果只有一个项目，则先进行新增项目后，再进行更新操作；否则，直接进行更新操作
        if len(project_ids) < 2:
            for i in range(2):
                project_management.add_project()
                time.sleep(1)
        # 查询当前用户下拥有管理员权限的项目数据
        query_project_sql = "SELECT tp.id,tp.project_name FROM t_project tp LEFT JOIN t_project_member tpm on tp.id=tpm.project_id WHERE tpm.user_id=%s AND tpm.role=1 and tp.`status`=1"
        query_project_result = handle_mysql.query_data(sql=query_project_sql, param=[project_management.user_id])
        param = {
            "id": query_project_result[0]["id"],
            "projectDesc": "",
            "projectName": query_project_result[1]["project_name"],
        }
        print("传入的参数：{}".format(param))
        res = project_management.request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20009
        assert res.json()["msg"] == "项目名称已存在"

    @allure.title("修改当前用户下无权限操作的项目")
    @allure.description("修改当前用户下无权限操作的项目")
    def test_005_update_project_without_permission(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        update_project_url = base_url + "/project/updateProject"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        project_name = "test" + str(int(time.time()))
        # 查询该用户下只有查看权限的项目
        user_id = get_token["data"]["id"]
        query_sql = "SELECT * FROM t_project_member WHERE `role`=3 and user_id=%s"
        result = handle_mysql.query_one(sql=query_sql, param=[user_id])
        param = {
                "id": result["project_id"],
                "projectDesc": "",
                "projectName": project_name
            }
        print("传入的参数：{}".format(param))
        res = request.handle_request(method="post", url=update_project_url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20009
        assert res.json()["msg"] == "您不是当前项目管理员，无操作权限！"
