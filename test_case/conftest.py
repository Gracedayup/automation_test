# – coding: utf-8 --
import pytest
from common.handle_requests import HandleRequest
from common.handle_data import HandleFileData
from base.get_token import GetToken
from db.operation_mysql import OperationMysql


@pytest.fixture(scope="session", autouse=True)
def get_token():
    result = GetToken().get_token().json()
    return result


@pytest.fixture(scope="session", autouse=True)
def get_base_info():
    base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['flow_base_url']
    request = HandleRequest()
    return base_url, request

@pytest.fixture(scope="session", autouse=False)
def handle_mysql():
    print("初始化mysql数据库连接")
    config_data = HandleFileData("config\config.yml").read_yaml()
    mysql_info = config_data["database"]
    db = OperationMysql(host=mysql_info["host"], port=mysql_info["port"], user=mysql_info["username"],
                   password=mysql_info["password"], database=mysql_info["database"])

    yield db
    print("关闭数据库连接")
    db.close_db()


if __name__ == '__main__':
    handle_mysql()



