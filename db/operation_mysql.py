# – coding: utf-8 --
"""
@Time : 2022/6/21 14:56
@Author : sunny cao
@File : operation_mysql.py
"""
import pymysql


class OperationMysql(object):
    def __init__(self, host, user, password, database, charset='uft8', port=3306):
        """
        初始化数据库连接
        :param host:数据库ip
        :param user:用户名
        :param password:密码
        :param database:数据库名
        :param charset:字符集
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.port = port
        self.con = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.con.cursor()

    def get_description(self):
        """
        查询表头信息
        :return: 表头信息 desc
        """
        key = self.cursor.description
        des = []
        for i in key:
            des.append(i[0])
        return des

    def query_data(self, sql, param=None, size=None):
        """

        :param sql:sql语句
        :param param:查询条件
        :param size:数据条数
        :return: 查询结果
        """
        result_list = []
        self.cursor.execute(query=sql, args=param)
        if size:
            result_data = self.cursor.fetchmany(size)
        else:
            result_data = self.cursor.fetchall()
        des = self.get_description()

        for value in result_data:
            result_list.append(dict(zip(des, value)))
        return result_list

    def query_one(self, sql, param=None):
        """

        :param sql:sql语句
        :param param:查询条件
        :return:查询结果
        """
        self.cursor.execute(query=sql, args=param)
        result_data = self.cursor.fetchone()
        des = self.get_description()
        result_list = dict(zip(des, result_data))
        return result_list

    def close_db(self):
        self.cursor.close()
        self.con.close()


if __name__ == '__main__':
    query_project = OperationMysql(host="10.1.1.40", user="root", password="jzy123456", database="db_jugo_flow")
    query_sql = "SELECT * FROM t_project_member WHERE `status`=1 and user_id!=%s"
    param = ["1"]
    result = query_project.query_one(sql=query_sql, param=param)
    print("最终的查询数据", result)

