from common.handle_data import HandleFileData
from common.handle_log import logger
from common import project_path
from common.handle_requests import HandleRequest
import pytest
import allure
import requests
import json


base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['base_url']


class TestLogin(object):
    @pytest.mark.parametrize("caseinfo", HandleFileData(r"test_data\login_test_data.csv").read_csv())
    def test_login(self, caseinfo):
        url = base_url + str(caseinfo['request_url'])
        header = {'Content-Type': 'application/json'}
        logger.info(f'>>>>>>>>>>>>>正在进行第【{caseinfo["case_no"]}】条测试用例<<<<<<<<<<<<<<<')
        logger.info(f'测试标题为>>>>>>>>>>>>>>>>：{caseinfo["case_name"]}')
        logger.info(f'请求方法为>>>>>>>>>>>>>>>>：{caseinfo["request_method"]}')
        logger.info(f'接口地址为>>>>>>>>>>>>>>>>：{url}')
        logger.info(f'测试参数为>>>>>>>>>>>>>>>>：{caseinfo["data"]}')
        res = HandleRequest().handle_request(url=url, data=caseinfo["data"], method=caseinfo["request_method"], headers=header)
        logger.info(f'返回结果>>>>>>>>>>>>>>>>：{res.text}')
        assert res.status_code == 200
        assert res.json()['msg'] == "请求成功!"


