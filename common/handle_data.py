# – coding: utf-8 --

from common import project_path
import csv
import os
import yaml
import configparser
import json


class HandleFileData(object):

    def __init__(self, file_path):
        self.file_path = os.path.join(project_path.project_path, file_path)

    def read_csv(self):
        """
        读取csv文件的数据
        :return: csv_content，list形式
        """
        with open(self.file_path, encoding="utf-8") as f:
            csv_content = []
            csv_data = csv.reader(f)
            csv_data_list = list(csv_data)
            csv_title = csv_data_list[0]
            for i in range(1, len(csv_data_list)):
                csv_content.append(dict(zip(csv_title, csv_data_list[i])))
            return csv_content

    def read_yaml(self):
        """
        读取yml文件
        :return: yml文件数据
        """
        with open(self.file_path, encoding="utf-8") as f:
            filedata = yaml.safe_load(f)
            return filedata

    def read_ini(self):
        """
        读取ini文件
        :return: 文件的section
        """
        config = configparser.ConfigParser()
        config.read(self.file_path, encoding="utf-8")
        filedata = config.sections()
        return filedata

    def read_json(self):
        """
        读取json文件
        :return:文件内容
        """
        with open(self.file_path, encoding="utf-8") as f:
            filedata = json.load(f)
        return filedata


if __name__ == '__main__':
    result = HandleFileData(r"test_data\login_test_data.csv").read_csv()
    print(result)


