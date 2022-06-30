# – coding: utf-8 --
"""
@Time : 2022/6/24 12:10
@Author : sunny cao
@File : test_del_bind_org.py
@ToDo : test_005_del_bind_org:目前调用删除接口后，依然存在，故用例failed。
        flow-我的账户-网络节点管理中未展示非公共节点，0.2.0版本提交后需验证
"""
import allure
from common.handle_log import logger
import json

headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：组织管理")
@allure.story("删除用户绑定的组织")
class TestDelBindOrg(object):

    @allure.title("必填项为空，删除用户绑定的组织")
    @allure.description("必填项为空，删除用户绑定的组织")
    def test_001_del_bind_org_without_id(self, get_base_info):
        base_url, request = get_base_info
        url = base_url + "/org/findOrgInfo"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"

    @allure.title("未登录状态，删除存在的组织")
    @allure.description("未登录状态，删除存在的组织")
    def test_002_del_bind_org_without_login(self, get_base_info, handle_mysql, get_token):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/org/delIpPortBind"
        headers = {'Content-Type': 'application/json'}
        get_org_sql = "SELECT o.`identity_id`,oe.`is_public` FROM `dc_org` o join `mo_org_expand` oe on o.`identity_id` = oe.`identity_id` WHERE o.`status` = 1 AND (oe.`is_public` = 1 OR o.`identity_id` IN ( SELECT `identity_id` FROM `mo_org_user` WHERE address=%s))"
        get_data_result = handle_mysql.query_one(sql=get_org_sql, param=[address])
        param = {
            'identityId': get_data_result["identity_id"]
        }
        res = request.handle_request(method="post", url=url, headers=headers, params=param)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("登录状态，删除非该用户绑定的组织")
    @allure.description("登录状态，删除非该用户绑定的组织")
    def test_003_del_unbound_org(self, get_base_info, handle_mysql, get_token):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/org/delIpPortBind"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        get_org_sql = "SELECT o.`identity_id`,oe.`is_public` FROM `dc_org` o join `mo_org_expand` oe on o.`identity_id` = oe.`identity_id` WHERE o.`status` = 1 AND (oe.`is_public` = 0 OR o.`identity_id` IN ( SELECT `identity_id` FROM `mo_org_user` WHERE address!=%s))"
        get_data_result = handle_mysql.query_one(sql=get_org_sql, param=[address])
        print("get_data_result:", get_data_result)
        # 如果能查询出来非当前用户绑定的组织，则调用删除用户绑定组织接口，由于接口响应都是10000，故通过查询数据库数据进行校验
        if get_data_result["identity_id"]:
            param = {
                'identityId': get_data_result["identity_id"]
            }
            res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
            logger.info("接口响应结果：{}".format(res.json()))
            assert res.json()["code"] == 10000
            assert res.json()["msg"] == "成功"
            # 如果接口调用成功，则查询数据库数据，看是否还存在
            if res.json()["code"] == 10000:
                search_org_sql = "SELECT * from mo_org_user WHERE identity_id=%s"
                print("identity_id:", get_data_result["identity_id"])
                sql_param = get_data_result["identity_id"]
                search_result = handle_mysql.query_data(sql=get_org_sql, param=sql_param)
                assert search_result != None

    @allure.title("登录状态，删除公共组织")
    @allure.description("登录状态，删除公共组织")
    def test_004_del_public_org(self, get_base_info, handle_mysql, get_token):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/org/delIpPortBind"
        url = base_url + "/org/delIpPortBind"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        get_org_sql = "SELECT o.`identity_id`,oe.`is_public` FROM `dc_org` o join `mo_org_expand` oe on o.`identity_id` = oe.`identity_id` WHERE o.`status` = 1 AND (oe.`is_public` = 1 OR o.`identity_id` IN ( SELECT `identity_id` FROM `mo_org_user` WHERE address!=%s))"
        public_org_result = handle_mysql.query_one(sql=get_org_sql, param=[address])
        print("public_org_result:", public_org_result)
        if public_org_result["identity_id"]:
            param = {
                'identityId': public_org_result["identity_id"]
            }
            res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
            logger.info("接口响应结果：{}".format(res.json()))
            assert res.json()["code"] == 10000
            assert res.json()["msg"] == "成功"
            # 如果接口调用成功，则查询数据库数据，看是否还存在
            if res.json()["code"] == 10000:
                search_org_sql = "SELECT * from mo_org_user WHERE identity_id=%s"
                print("identity_id:", public_org_result["identity_id"])
                sql_param = public_org_result["identity_id"]
                search_result = handle_mysql.query_data(sql=get_org_sql, param=sql_param)
                assert search_result != None

    @allure.title("登录状态，删除该用户绑定的非公共组织")
    @allure.description("登录状态，删除该用户绑定的非公共组织")
    def test_005_del_bind_org(self, get_base_info, handle_mysql, get_token):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/org/delIpPortBind"
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        get_org_sql = "SELECT o.`identity_id`,oe.`is_public` FROM `dc_org` o join `mo_org_expand` oe on o.`identity_id` = oe.`identity_id` WHERE o.`status` = 1 AND (oe.`is_public` = 0 OR o.`identity_id` IN ( SELECT `identity_id` FROM `mo_org_user` WHERE address=%s))"
        usr_bind_org_data = handle_mysql.query_one(sql=get_org_sql, param=[address])
        print("usr_bind_org_data:", usr_bind_org_data)
        # 如果能查询出来当前用户绑定的组织，则调用删除用户绑定组织接口，由于接口响应都是10000，故通过查询数据库数据进行校验
        if usr_bind_org_data["identity_id"]:
            param = {
                'identityId': usr_bind_org_data["identity_id"]
            }
            res = request.handle_request(method="post", url=url, headers=headers, data=json.dumps(param))
            logger.info("接口响应结果：{}".format(res.json()))
            assert res.json()["code"] == 10000
            assert res.json()["msg"] == "成功"
            # 如果接口调用成功，则查询数据库数据，看是否还存在
            if res.json()["code"] == 10000:
                search_org_sql = "SELECT * from mo_org_user WHERE identity_id=%s"
                print("identity_id:", usr_bind_org_data["identity_id"])
                sql_param = usr_bind_org_data["identity_id"]
                search_result = handle_mysql.query_data(sql=get_org_sql, param=sql_param)
                assert search_result == None
