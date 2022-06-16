import requests
import json


class HandleRequest(object):
    def __init__(self):
        self.session = requests.session()

    def handle_request(self, url, method, params=None, data=None, json=None, **kwargs):
        res = self.session.request(url=url, method=method,data=data, params=params, json=json, **kwargs)
        return res
