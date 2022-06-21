# coding=utf-8

import pytest
import os

if __name__ == '__main__':
    # 运行包含指定关键字的用例(-k )
    # pytest.main(["-vs", "--alluredir=temp", "-k", "nickname"])
    pytest.main(["-vs", "--alluredir=temp"])
    os.system("allure generate ./temp -o ./report --clean")
