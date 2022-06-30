# – coding: utf-8 --
"""
@Time : 2022/6/27 16:10
@Author : sunny cao
@File : test_query_project_list.py
"""
import allure
from common.handle_log import logger

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("查询项目列表")
class TestQueryProjectList(object):
    @allure.title("未登录状态，查询项目列表")
    @allure.description("未登录状态，查询项目列表")
    def test_001_query_project_list_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectPageList"
        param = {
            "current": 1,
            "size": 10
        }
        res = request.handle_request(method="get", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("登录状态，必填项为空，查询项目列表")
    @allure.description("登录状态，必填项为空，查询项目列表")
    def test_002_query_project_list_without_requirement_param(self, get_base_info, get_token):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectPageList"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        print("-------headers------------:{}".format(headers))
        res = request.handle_request(method="get", url=url, headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20001
        assert res.json()["msg"] == "{page.number.notBlank}"
    
    @allure.title("登录状态，成功查询项目列表")
    @allure.description("登录状态，成功查询项目列表")
    def test_003_query_project_list_success(self, get_base_info, get_token, handle_mysql):
        access_token = get_token["data"]["token"]
        user_id = get_token["data"]["id"]
        base_url, request = get_base_info
        url = base_url + "/project/queryProjectPageList"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        param = {
            "current": 1,
            "size": 10,
            "projectName": "回归"
        }
        res = request.handle_request(method="get", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            # 检查接口响应的条数是否与数据库中的数据一致
            querey_sql = "select a.id as id,a.project_name as projectName,a.project_desc as projectDesc,a.create_time as createTime,b.role as role,(select u.user_name from t_user u where u.status = 1 and u.id = a.user_id) as userName from t_project a, t_project_member b where a.id = b.project_id and b.user_id = %s and a.project_name LIKE '%%回归%%' and a.status = 1 and b.status = 1 order by a.create_time desc LIMIT 10"
            get_data_result = handle_mysql.query_data(sql=querey_sql, param=[user_id])
            assert len(res.json()["data"]["items"]) == len(get_data_result)