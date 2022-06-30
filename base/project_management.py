# -*- coding: utf-8 -*-
"""
@Time : 2022/6/29 14:12
@Author : name
@File : project_management.py
"""

import json
import random
import time
from base.get_token import GetToken
from common.handle_requests import HandleRequest
from common.handle_data import HandleFileData

login_result = GetToken().get_token().json()
request = HandleRequest()
user_id = login_result["data"]["id"]
access_token = login_result["data"]["token"]
address = eval(login_result["data"]["walletJson"])["address"]
base_url = HandleFileData(r"config\config.yml").read_yaml()['server']['flow_base_url']
headers = {'Content-Type': 'application/json', 'Access-Token': access_token}

add_project_url = base_url + "/project/addProject"
update_project_url = base_url + "/project/updateProject"
query_project_list_url = base_url + "/project/queryProjectPageList"
add_project_member_url = base_url + "/project/addProjMember"
query_project_member_list_url = base_url + "/project/queryProjMemberPageList"
update_project_member_url = base_url + "/project/updateProjMember"
delete_project_member_url = base_url + "/project/deleteProjMember"
batch_delete_project_member_url = base_url + "/project/deleteProjMemberBatch"


def add_project():
    project_name = "test" + str(int(time.time()))
    param = {
        "projectDesc": "",
        "projectName": project_name,
        "projectTempId": 0
    }
    res = request.handle_request(method="post", url=add_project_url, headers=headers, data=json.dumps(param))
    return project_name, res

def query_user_project(role=None):
    """
    查询当前登录用户的项目数据
    :param role: 项目成员角色
    :return:res 调用查询用户项目接口返回结果, project_id_list 该用户拥有指定角色的项目数据
    """
    project_id_list = []
    param = {
        "current": 1,
        "size": 10
    }
    res = request.handle_request(method="get", url=query_project_list_url, headers=headers, params=param)
    project_data = res.json()["data"]["items"]
    # 如果role不为空，则返回所有的结果
    if role:
        for index, element in enumerate(project_data):
            if element["role"] == role:
                project_id_list.append(element["id"])
    else:
        for index, element in enumerate(project_data):
            project_id_list.append(element["id"])

    return res, project_id_list

def query_project_users(project_id):
    """
    查询当前项目可以筛选的项目
    :param project_id:项目id
    :return:查询当前项目筛选的用户接口响应结果
    """
    query_project_all_user_url = base_url + "/project/queryAllUserNickname/" + "/" + str(project_id)
    res = request.handle_request(method="get", url=query_project_all_user_url, headers=headers)
    print("查询当前项目可以筛选的用户：{0}".format(res.json()))
    return res

def add_project_member(project_id, user_id, role):
    """
    新增项目成员
    :param project_id: 项目id
    :param user_id: 用户id
    :param role: 项目成员角色
    :return: 新增项目成员接口的响应结果
    """
    param = {
        "projectId": project_id,
        "role": role,
        "userId": user_id
    }
    res = request.handle_request(method="post", url=add_project_member_url, headers=headers, data=json.dumps(param))
    print("添加项目成员：{0}".format(res.json()))
    return res

def query_project_member_list(project_id):
    param = {
        "current": 1,
        "projectId": project_id,
        "size": 10
    }
    res = request.handle_request(method="get", url=query_project_member_list_url, headers=headers, params=param)
    return res

def update_project_member(id, role, user_id):
    param = {
        "id": id,
        "role": role,
        "userId": user_id
    }
    res = request.handle_request(method="post", url=update_project_member_url, headers=headers, data=json.dumps(param))

    return res

def delete_project_member(project_member_id):
    param = {
        "projMemberId": project_member_id
    }
    res = request.handle_request(method="post", url=delete_project_member_url, headers=headers, data=json.dumps(param))
    return res

def batch_delete_project_member(project_member_ids):
    """
    批量删除项目成员
    :param project_member_id_list: project_member_id数组
    :return: 接口响应结果
    """
    if isinstance(project_member_ids, list):
        ids = ','.join(str(i) for i in project_member_ids)
    else:
        ids = str(project_member_ids)
    param = {
        "projMemberIds": ids
    }
    res = request.handle_request(method="post", url=batch_delete_project_member_url, headers=headers, data=json.dumps(param))
    return res

a = [68, 70]
batch_delete_project_member(a)
