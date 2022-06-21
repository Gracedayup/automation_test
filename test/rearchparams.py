"""
@Time : 2022/6/20 9:45
@Author : sunny cao
@File : rearchparams.py
"""
import re

params = '{"_var":"38.1", "_ct":"101", "token"：${token}, "order-id":${order_id}}'
ru = r'\${(.*?)}'
login_info = {"token": "1223232", "order_id": "2222"}

while re.search(ru, params):
    res = re.search(ru, params)
    params_key = res.group(1)
    print("params_key", params_key)
    print(params_key)
    print(type(login_info))
    params_value = login_info[params_key]
    params = re.sub(ru, params_value, params, 1)

print(params)

