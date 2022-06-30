# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 15:10
@Author : name
@File : test_add_project_member.py
"""
import json
import pytest
from common.handle_log import logger
import allure
import time
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("新增项目成员")
class TestAddProjectMember(object):

    @allure.title("未登录状态，新增项目成员")
    @allure.description("未登录状态，新增项目成员")
    def test_001_add_project_member_without_login(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/project/addProjMember"
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("projectId为空，新增项目成员")
    @allure.description("projectId为空，新增项目成员")
    def test_002_add_project_member_without_projectId(self, get_base_info, get_token):
        base_url, request = get_base_info
        url = base_url + "/project/addProjMember"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        user_id = get_token["data"]["id"]
        param = {
            "projectId": 0,
            "role": 1,
            "userId": user_id
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004
        assert res.json()["msg"] == "project id must more than zero"

    @allure.title("role为空，新增项目成员")
    @allure.description("role为空，新增项目成员")
    def test_003_add_project_member_without_role(self, get_base_info, get_token):
        base_url, request = get_base_info
        url = base_url + "/project/addProjMember"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        user_id = get_token["data"]["id"]
        param = {
            "projectId": 19,
            "userId": user_id
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004
        assert res.json()["msg"] == "{project.member.role.NotNull}"

    def test_004_add_project_member_without_userId(self, get_base_info, get_token):
        base_url, request = get_base_info
        url = base_url + "/project/addProjMember"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        param = {
            "projectId": 19,
            "role": 1
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004
        assert res.json()["msg"] == "{user.id.NotNull}"

    @allure.title("成功新增项目成员")
    @allure.description("成功新增项目成员")
    def test_005_add_project_member_success(self, get_base_info, get_token, handle_mysql):
        # 调用接口，查询当前用户下的项目
        base_url, request = get_base_info
        add_project_member_url = base_url + "/project/addProjMember"
        get_project_list_url = base_url + "/project/queryProjectPageList"
        get_project_member_url = base_url + "/project/queryAllUserNickname"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        project_list_param = {
            "current": 1,
            "size": 10
        }
        get_user_project_res = request.handle_request(method="get", url=get_project_list_url, headers=headers, params=project_list_param)
        project_id_list = []
        project_data = get_user_project_res.json()["data"]["items"]
        # 查询role为1的项目数据
        for index, element in enumerate(project_data):
            if element["role"] == 1:
                project_id_list.append(element["id"])
        # 调用接口，查询当前项目可筛选的用户
        get_project_users = request.handle_request(method="get",
                                                   url=(get_project_member_url + "/" + str(project_id_list[0])),
                                                   headers=headers)
        #调用新增项目接口
        project_member_param = {
            "projectId": project_id_list[0],
            "role": 1,
            "userId": get_project_users.json()["data"][0]["id"]
        }
        res = request.handle_request(method="post", url=add_project_member_url, headers=headers, data=json.dumps(project_member_param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"

    @allure.title("新增已存在的项目成员")
    @allure.description("新增已存在的项目成员")
    def test_006_add_exist_project_member(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        add_project_member_url = base_url + "/project/addProjMember"
        get_project_list_url = base_url + "/project/queryProjectPageList"
        get_project_member_url = base_url + "/project/queryProjMemberPageList"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询该用户下role为1的项目数据
        project_list_param = {
            "current": 1,
            "size": 10
        }
        get_user_project_res = request.handle_request(method="get", url=get_project_list_url, headers=headers, params=project_list_param)
        project_id_list = []
        project_data = get_user_project_res.json()["data"]["items"]
        for index, element in enumerate(project_data):
            if element["role"] == 1:
                project_id_list.append(element["id"])
        # 调用接口，查询当前项目下已添加的成员
        project_member_param = {
            "current": 1,
            "projectId": project_id_list[0],
            "size": 10
        }
        project_member = request.handle_request(method="get", url=get_project_member_url, headers=headers, params=project_member_param)
        # 调用接口，再次添加已存在的成员
        add_project_member_param = {
            "projectId": project_id_list[0],
            "role": 1,
            "userId": project_member.json()["data"]["items"][0]["userId"]
        }
        add_project_member_res = request.handle_request(method="post", url=add_project_member_url, headers=headers, data=json.dumps(add_project_member_param))
        logger.info("接口响应结果：{}".format(add_project_member_res.json()))
        assert add_project_member_res.json()["code"] == 20009
        assert add_project_member_res.json()["msg"] == "成员角色已存在"

