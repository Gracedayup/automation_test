# – coding: utf-8 --


from common.handle_data import HandleFileData
from common.handle_log import logger
from common.handle_requests import HandleRequest
from base.get_token import GetToken
import pytest
import allure


token = GetToken()
header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：用户管理")
class TestUserManagement(object):

    @allure.story("用户登录")
    @pytest.mark.parametrize("caseinfo", HandleFileData(r"test_data\api\user_management\login_test_data.csv").read_csv())
    def test_login_flow(self, caseinfo, get_base_info):
        allure.dynamic.title(caseinfo["case_no"] + caseinfo["case_name"])
        allure.dynamic.description(caseinfo["case_name"])

        base_url, request = get_base_info
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




