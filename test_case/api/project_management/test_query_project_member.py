# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 17:42
@Author : name
@File : test_query_project_member.py
"""
from common.handle_log import logger
import allure
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("查询项目成员列表")
class TestQueryProjectMember(object):

    @allure.title("未登录状态，查询项目成员列表")
    @allure.description("未登录状态，查询项目成员列表")
    def test_001_query_project_member_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/queryProjMemberPageList"
        res = request.handle_request(method="get", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("成功查询项目成员列表")
    @allure.description("成功查询项目成员列表")
    def test_002_query_project_member(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        get_project_list_url = base_url + "/project/queryProjectPageList"
        get_project_member = base_url + "/project/queryProjMemberPageList"
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 查询该用户下的项目
        project_list_param = {
            "current": 1,
            "size": 10
        }
        get_user_project_res = request.handle_request(method="get", url=get_project_list_url, headers=headers,
                                                      params=project_list_param)
        get_project_member_param = {
            "current": 1,
            "size": 10,
            "projectId": get_user_project_res.json()["data"]["items"][0]["id"]
        }
        get_project_member_res = request.handle_request(method="get", url=get_project_member, headers=headers, params=get_project_member_param)
        logger.info("接口响应结果：{}".format(get_project_member_res.json()))
        assert get_project_member_res.json()["code"] == 10000
        assert get_project_member_res.json()["msg"] == "成功"



