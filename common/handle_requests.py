# – coding: utf-8 --

from common.handle_log import logger
import requests
import json
import jsonpath
from common.handle_data import HandleFileData


class HandleRequest(object):
    def __init__(self):
        self.session = requests.session()

    def handle_request(self, url, method, params=None, data=None, json=None, **kwargs):
        res = self.session.request(url=url, method=method, data=data, params=params, json=json, **kwargs)
        return res

    def handle_validate(self, expect_result, actual_result, status_code):
        """
        caseinfo
        :param caseinfo:
        :return:
        """
        flag = 0
        if expect_result and isinstance(expect_result, list):
            for expect in expect_result:
                logger.info("期望结果：{0}".format(expect))
                if expect["check"] == "status_code":
                    if status_code != expect["expect"]:
                        flag = flag + 1
                        logger.error("断言失败：{0}: not {1} {2}".format(expect["check"], expect["assert"], expect["expect"]))
                else:
                    if actual_result[expect["check"]] != expect["expect"]:
                        flag = flag + 1
                        logger.error("断言失败：{0}: not {1} {2}".format(expect["check"], expect["assert"], expect["expect"]))
        if flag == 0:
            logger.info("断言成功")
        else:
            raise Exception("断言失败")


if __name__ == '__main__':
    base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['flow_base_url']
    request = HandleRequest()
    respect = {'status': '10000', 'size': 10, 'msg': '成功'}
    url = base_url + "/org/listOrgInfoByTotalData"
    res = request.handle_request(url=url, method="get")
    HandleRequest().handle_assert(res, respect)








