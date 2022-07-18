# – coding: utf-8 --
"""
@Time : 2022/6/22 15:34
@Author : sunny cao
@File : test_data_auth.py
@ToDo : 签名问题，该功能暂未实现
"""
import allure
headers = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：数据管理")
@allure.story("数据详情")
class TestDataAuth(object):
    @allure.title("数据-申请授权")
    @allure.description("数据申请授权")
    def test_data_auth_success(self, get_base_info, get_token, handle_mysql):
        access_token = get_token["data"]["token"]
        base_url, request = get_base_info
        wallet_json = get_token["data"]["walletJson"]
        address = eval(get_token["data"]["walletJson"])["address"]
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        # 获取nonce
        get_nonce_url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=get_nonce_url, method="get", headers=headers)
        nonce = res.json()["data"]["nonce"]

        # 数据授权
        url = base_url + "/data/auth"

        res = request.handle_request(url=url, method="post", )

    # 申请中的数据，再次申请授权
    # 已授权的数据，再次申请授权

