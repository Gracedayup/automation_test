# – coding: utf-8 --

"""
@Time : 2022/6/21 14:43
@Author : sunny cao
@File : test_query_nickname.py
"""
from common.handle_log import logger
import allure


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
@allure.story("查询所有用户昵称")
class TestQueryNickname(object):

    @allure.title("未登录状态，查询所有用户昵称")
    @allure.description("未登录状态，查询所有用户昵称")
    def test_query_nickname_without_login(self, get_token, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/user/queryAllUserNickname"
        headers = {'Content-Type': 'application/json'}
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("登录状态，查询所有用户昵称")
    @allure.description("登录状态，查询所有用户昵称")
    def test_query_nickname_success(self, get_token, get_base_info, handle_mysql):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/user/queryAllUserNickname"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        sql = "SELECT user_id,user_name from t_user where status=%s"
        result = handle_mysql.query_data(sql=sql, param=[1])
        if res.json()["msg"] == "成功":
            assert len(res.json()["data"]) == len(result)



