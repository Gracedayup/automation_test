# – coding: utf-8 --

from common.handle_log import logger
import allure

header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
@allure.story("获取Nonce")
class TestGetNonce(object):

    @allure.title("未登录状态，获取Nonce")
    @allure.description("未登录状态，获取Nonce")
    def test_get_nonce_without_login(self, get_token, get_base_info):
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.title("获取Nonce，输入不存在的address")
    @allure.description("获取Nonce，输入不存在的address")
    def test_get_nonce_address_not_exit(self, get_token, get_base_info):
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        url = base_url + "/user/getNonce/" + address + "111"
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"

    @allure.title("输入正确信息，获取Nonce")
    @allure.description("输入正确信息，获取Nonce")
    def test_get_nonce_success(self, get_token, get_base_info):
        base_url, request = get_base_info
        address = eval(get_token["data"]["walletJson"])["address"]
        access_token = get_token["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"

