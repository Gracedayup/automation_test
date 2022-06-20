# coding=utf-8

import pytest
import os

if __name__ == '__main__':
    pytest.main(["-vs", "--alluredir=temp"])
    os.system("allure generate ./temp -o ./report --clean-alluredir")
