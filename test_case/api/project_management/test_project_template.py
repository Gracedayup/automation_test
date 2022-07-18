# – coding: utf-8 --# – coding: utf-8 --
"""
@Time : 2022/6/27 15:10
@Author : sunny cao
@File : test_query_project_list.py
"""
from common.handle_log import logger
import allure

header = {'Content-Type': 'application/json'}


@allure.epic("项目名称：Jugo接口自动化测试项目")
@allure.feature("模块名称：项目管理")
@allure.story("项目模板")
class TestProjectTemplate(object):

    @allure.title("查询项目模板列表")
    @allure.description("查询项目模板列表")
    def test_001_project_template(self, get_base_info, handle_mysql):
        base_url, request = get_base_info
        url = base_url + "/projectTemplate/list"
        res = request.handle_request(url=url, method="get")
        logger.info("接口响应结果：{}".format(res.json()))
        assert res.json()["code"] == 10000
        assert res.json()["msg"] == "成功"
        if res.json()["code"] == 10000:
            qurey_sql = "SELECT * FROM t_project_temp"
            result =  handle_mysql.query_data(sql=qurey_sql)
            print("result:", result)
            # 检查返回的数据条数
            assert len(res.json()["data"]) == len(result)
