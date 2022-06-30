# – coding: utf-8 --
"""
@Time : 2022/6/24 12:10
@Author : sunny cao
@File : test_add_org.py
"""
import allure
from common.handle_log import logger
import json
import pytest

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：组织管理")
@allure.story("我的账户-网络节点管理，添加组织新节点")
class TestAddOrg(object):
    @allure.title("未登录状态，添加用户绑定的组织")
    @allure.description("未登录状态，添加用户绑定的组织")
    def test_001_add_org_without_login(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/addIpPortBind"
        param = {
            "identityIp": "192.168.0.1",
            "identityPort": 8234
        }
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"
        
    
    @allure.title("登录状态，添加不可用的组织")
    @allure.description("登录状态，添加不可用的组织")
    def test_002_add_unavailable_org(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/org/addIpPortBind"
        param = {
            "identityIp": "192.168.0.1",
            "identityPort": 8234
        }
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20009
        assert res.json()["msg"] == "连接组织节点服务不可达"

    @allure.title("登录状态，必填项为空，添加组织")
    @allure.description("登录状态，必填项为空，添加组织")
    def test_003_add_org_without_requirement_param(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/org/addIpPortBind"
        param = {
            "identityIp": "192.168.0.1"
        }
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"
    
    @allure.title("登录状态，成功添加组织")
    @allure.description("登录状态，成功添加组织")
    def test_004_add_org_success(self, get_base_info, get_token):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        url = base_url + "/org/addIpPortBind"
        param = {
            "identityIp": "10.1.1.46",
            "identityPort": 10033
        }
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"

    @allure.title("登录状态，添加已存在的组织")
    @allure.description("登录状态，添加已存在的组织")
    def test_005_add_exist_org(self, get_base_info, get_token, handle_mysql):
        base_url, request = get_base_info
        access_token = get_token["data"]["token"]
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/org/addIpPortBind"
        get_org_sql = "SELECT o.`identity_id`,oe.`is_public`, oe.identity_ip, oe.identity_port FROM `dc_org` o join `mo_org_expand` oe on o.`identity_id` = oe.`identity_id` WHERE o.`status` = 1 AND (oe.`is_public` = 0 OR o.`identity_id` IN ( SELECT `identity_id` FROM `mo_org_user` WHERE address=%s))"
        usr_bind_org_data = handle_mysql.query_one(sql=get_org_sql, param=[address])
        param = {
            "identityIp": usr_bind_org_data["identity_ip"],
            "identityPort": usr_bind_org_data["identity_port"]
        }   
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        # 接口响应10000，无法判断是否重复添加，需对数据进行校验(是否只存在一条数据)
        result = handle_mysql.query_data(sql=get_org_sql, param=[address])
        assert len(result) == 1
         