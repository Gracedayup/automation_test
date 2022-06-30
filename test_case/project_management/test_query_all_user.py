# -*- coding: utf-8 -*-
"""
@Time : 2022/6/28 18:02
@Author : name
@File : test_query_all_user.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("查询项目可筛选的用户数据")
class TestQueryAllUser(object):
    @allure.title("未登录状态，查询项目可筛选的用户数据")
    @allure.description("未登录状态，查询项目可筛选的用户数据")
    def test_001_query_project_all_user_without_login(self, get_base_info, get_token):
        base_url, request = get_base_info
        query_project_all_user_url = base_url + "/project/queryAllUserNickname/30"
        res = request.handle_request(method="get", url=query_project_all_user_url)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    def test_002_query_project_all_user(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        header = {'Content-Type': 'application/json', 'Access-Token': access_token}
        get_user_project_url = base_url + "/project/queryProjectPageList"
        get_user_project_param = {
            "current": 1,
            "size": 10
        }
        get_user_project_res = request.handle_request(method="get", url=get_user_project_url, headers=header,
                                                      params=get_user_project_param)
        print("该用户下的项目数据为：{0}".format(get_user_project_res.json()))
        query_project_all_user_url = base_url + "/project/queryAllUserNickname" + "/" + str(get_user_project_res.json()["data"]["items"][0]["id"])
        get_project_all_user_res = request.handle_request(method="get", url=query_project_all_user_url, headers=header)
        logger.info("接口响应结果：{}".format(get_project_all_user_res.json()))
        assert get_project_all_user_res.json()["code"] == 10000
        assert get_project_all_user_res.json()["msg"] == "成功"

