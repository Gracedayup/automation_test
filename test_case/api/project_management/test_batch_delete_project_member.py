# -*- coding: utf-8 -*-
"""
@Time : 2022/6/30 12:01
@Author : name
@File : test_batch_delete_project_member.py
"""
import allure
from base import project_management
from common.handle_log import logger

header = {'Content-Type': 'application/json'}
url = project_management.batch_delete_project_member_url


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("批量删除项目成员")
class TestBatchDeleteProjectMember(object):
    @allure.title("未登录状态，批量删除项目成员")
    @allure.description("未登录状态，批量删除项目成员")
    def test_001_batch_delete_project_member_without_login(self, get_base_info):
        base_url, request = get_base_info
        res = request.handle_request(method="post", url=url, headers=header)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("必填项为空，批量删除项目成员")
    @allure.description("必填项为空，批量删除项目成员")
    def test_002_batch_delete_project_member_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="post", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20003
        assert res.json()["msg"] == "参数格式错误"

    @allure.title("成功批量删除项目成员")
    @allure.description("成功批量删除项目成员")
    def test_003_batch_delete_project_member_success(self):
        # 查询该用户下的项目
        res, project_id_list = project_management.query_user_project(1)
        # 查询项目下的项目成员信息
        query_project_res = project_management.query_project_member_list(project_id_list[0])
        # 新增项目成员
        project_users_res = project_management.query_project_users(project_id_list[0])
        project_management.add_project_member(project_id=project_id_list[0],
                                              user_id=project_users_res.json()["data"][0]["id"], role=2)
        # 再次查询项目成员信息后删除
        re_query_project_res = project_management.query_project_member_list(project_id_list[0])
        project_member = re_query_project_res.json()["data"]["items"][0]["memberId"]
        batch_delete_member_res = project_management.batch_delete_project_member(project_member)
        logger.info("接口响应结果：{}".format(batch_delete_member_res.json()))
        assert batch_delete_member_res.json()["code"] == 10000
        assert batch_delete_member_res.json()["msg"] == "成功"

    @allure.title("批量删除项目成员-当前用户下无权限操作的项目")
    @allure.description("批量删除项目成员-当前用户下无权限操作的项目")
    def test_004_delete_project_member_without_permission(self, handle_mysql):
        user_id = project_management.user_id
        query_project_sql = "SELECT * FROM t_project_member WHERE project_id not in (SELECT project_id FROM t_project_member WHERE user_id=%s)"
        query_project_result = handle_mysql.query_one(sql=query_project_sql, param=[user_id])
        res = project_management.batch_delete_project_member(query_project_result["id"])
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] != 10000
