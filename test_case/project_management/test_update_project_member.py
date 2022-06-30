# -*- coding: utf-8 -*-
"""
@Time : 2022/6/29 10:03
@Author : name
@File : test_update_project_member.py
"""
import json
import allure
from base import project_management
from common.handle_log import logger

header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("修改项目成员")
class TestUpdateProjectMember(object):
    @allure.title("未登录状态，修改项目成员")
    @allure.description("未登录状态，修改项目成员")
    def test_001_update_project_member_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/updateProjMember"
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("必填项为空，修改项目成员")
    @allure.description("必填项为空，修改项目成员")
    def test_002_update_project_member_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/project/updateProjMember"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        param = {
            "id": "",
            "role": "",
            "userId": 0
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20004

    @allure.title("成功修改项目成员")
    @allure.description("成功修改项目成员")
    def test_003_update_project_member_success(self):
        # 查询该用户下的项目
        res, project_id_list = project_management.query_user_project(1)
        # 查询项目下的项目成员信息
        query_project_res = project_management.query_project_member_list(project_id_list[0])
        # 判断该项目下的成员信息，如果有多个项目成员，则变更项目成员信息，否则，先新增项目成员，再变更
        if len(query_project_res.json()["data"]["items"]) > 1:
            # 如果有多个，则变更项目成员信息
            update_res = project_management.update_project_member(id=query_project_res.json()["data"]["items"][0]["memberId"],
                                                     role=2, user_id=query_project_res.json()["data"]["items"][0]["userId"])
            logger.info("接口响应结果：{}".format(update_res.json()))
            assert update_res.json()["code"] == 10000
            assert update_res.json()["msg"] == "成功"
        else:
            # 如果只有一个，则先新增项目成员，再变更项目成员信息
            project_users_res = project_management.query_project_users(project_id_list[0])
            print("查询当前项目可以筛选的用户：{0}".format(project_users_res.json()))
            project_management.add_project_member(project_id=project_id_list[0], user_id=project_users_res.json()["data"][0]["id"], role=2)
            re_query_project_res = project_management.query_project_member_list(project_id_list[0])
            # 修改项目成员
            update_res = project_management.update_project_member(
                id=re_query_project_res.json()["data"]["items"][0]["memberId"],
                role=2, user_id=re_query_project_res.json()["data"]["items"][0]["userId"])
            logger.info("接口响应结果：{}".format(update_res.json()))
            assert update_res.json()["code"] == 10000
            assert update_res.json()["msg"] == "成功"

    @allure.title("修改项目成员-当前用户下无权限操作的项目")
    @allure.description("修改项目成员-当前用户下无权限操作的项目")
    def test_004_update_project_member_without_permission(self, handle_mysql):
        user_id = project_management.user_id
        query_project_sql = "SELECT * FROM t_project_member WHERE project_id not in (SELECT project_id FROM t_project_member WHERE user_id=%s)"
        query_project_result = handle_mysql.query_one(sql=query_project_sql, param=[user_id])
        res = project_management.update_project_member(id=query_project_result["id"],
                                                 role=2, user_id=query_project_result["user_id"])
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] != 10000






