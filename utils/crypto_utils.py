# – coding: utf-8 --
"""
@Time : 2022/6/23 11:11
@Author : sunny cao
@File : crypto_utils.py
@ToDo : sign_message未完成，目前导入的web3签名方法中对于message有格式要求，需检查flow项目中引入的web3是否为公司改造后的
"""

from base.get_token import GetToken
from common.handle_requests import HandleRequest
from common.handle_data import HandleFileData
from eth_account import Account


class CryptoUtils(object):
    def user_info(self):
        """
        获取用户信息：钱包地址、wallet_json、nonce
        :return:
        """
        result = GetToken().get_token().json()
        address = eval(result["data"]["walletJson"])["address"]
        wallet_json = result["data"]["walletJson"]
        access_token = result["data"]["token"]
        # 调用获取nonce接口
        headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
        base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['flow_base_url']
        request = HandleRequest()
        nonce_url = base_url + "/user/getNonce/" + address
        res = request.handle_request(url=nonce_url, method="get", headers=headers)
        nonce = res.json()["data"]["nonce"]
        print("wallet_json：{0}，address：{1}，nonce：{2}".format(wallet_json, address, nonce))
        return wallet_json, address, nonce

    def get_abi(self, nonce, address):
        """
        获取nonceID和address数据（address数据从get_token的walletJson），组装signMessage
        :return:
        """
        sign_message = {"domain":{"name":"JugoFlow"},"message":{"key":nonce,"address":address},"primaryType":"sign","types":{"EIP712Domain":[{"name":"name","type":"string"}],"sign":[{"name":"key","type":"string"},{"name":"address","type":"string"}]}}
        return str(sign_message)

    def get_decrypt_info(self, wallet_json, password, sign_message):
        """
        解密
        :return:
        """
        priv_key = Account.decrypt(wallet_json, password)
        account = Account.privateKeyToAccount(priv_key)
        key_obj = account._key_obj
        print("key_obj:", key_obj)
        print("priv_key:", priv_key)
        print("account:", account)

        return key_obj, priv_key


    def get_signed_info(self, key_obj, sign_message, priv_key):
        """
        生成签名
        :return:
        """





if __name__ == '__main__':
    crypt = CryptoUtils()
    wallet_json, address, nonce = crypt.user_info()
    sign_message = crypt.get_abi(nonce=nonce, address=address)
    key_obj, priv_key = crypt.get_decrypt_info(wallet_json=wallet_json, password="Aa123456", sign_message=sign_message)


