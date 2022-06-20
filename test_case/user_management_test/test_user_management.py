# – coding: utf-8 --
from common.handle_data import HandleFileData
from common.handle_log import logger
from common.handle_requests import HandleRequest
from base.get_token import GetToken
import pytest
import allure

base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['flow_base_url']
token = GetToken()
header = {'Content-Type': 'application/json'}
request = HandleRequest()


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
class TestUserManagement(object):

    @allure.story("用户登录")
    @pytest.mark.parametrize("caseinfo", HandleFileData(r"test_data\login_test_data.csv").read_csv())
    def test_login_flow(self, caseinfo):
        allure.dynamic.title(caseinfo["case_no"] + caseinfo["case_name"])
        allure.dynamic.description(caseinfo["case_name"])
        url = base_url + str(caseinfo["request_url"])
        image_base64, verify_code_key = token.get_verify_code()
        verify_code = token.recognize_text(image_base64)
        data = caseinfo["data"]
        new_data = str(data).replace("{{verifyCodeKey}}", verify_code_key).replace("{{verifyCodeValue}}", verify_code)
        logger.info("接口传入参数：{0}".format(new_data))
        res = request.handle_request(url=url, data=new_data, method=caseinfo["request_method"],
                                             headers=header)
        logger.info("接口响应：{0}".format(res.text))
        request.handle_validate(expect_result=eval(caseinfo["validate"]), actual_result=res.json(), status_code=res.status_code)

    @allure.story("获取Nonce")
    @allure.title("未登录状态，获取Nonce")
    @allure.description("未登录状态，获取Nonce")
    def test_get_nonce_without_login(self):
        result = token.get_token().json()
        address = result["data"]["walletJson"]
        url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=url, method="get")
        assert res.json()["code"] == 20006
        assert res.json()["msg"] == "用户未登录"

    @allure.story("获取Nonce")
    @allure.title("获取Nonce，输入不存在的address")
    @allure.description("获取Nonce，输入不存在的address")
    def test_get_nonce_address_not_exit(self):
        result = token.get_token().json()
        address = result["data"]["walletJson"]
        access_token = result["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        url = base_url + "/user/getNonce/" + address + "111"
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 30000
        assert res.json()["msg"] == "系统异常，请联系管理台"

    @allure.story("获取Nonce")
    @allure.title("输入正确信息，获取Nonce")
    @allure.description("输入正确信息，获取Nonce")
    def test_get_nonce_success(self):
        result = token.get_token().json()
        address = eval(result["data"]["walletJson"])["address"]
        access_token = result["data"]["token"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=url, method="get", headers=headers)
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"



