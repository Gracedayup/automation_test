"""
@Time : 2022/6/16 15:59
@Author : sunny cao
@File : test.py
"""
from common.get_token import GetToken
from common.handle_log import logger
res = GetToken().get_token()
if res.json()["code"] != 10000:
    for i in range(0, 3):
        logger.info("-----------第{0}次重试----------------".format(i+1))
        res = GetToken().get_token()
print(res.json())
