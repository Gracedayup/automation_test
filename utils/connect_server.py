"""
@Time : 2022/6/2 16:09
@Author : sunny cao
@File : connect_server.py
"""
import paramiko
import os
import time


class ConnectServer(object):
    '''
    :param ip:服务器ip
    :param username: 用户名
    :param password:密码
    :param port:端口
    '''
    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.port = port

    def connect(self):
        transport = paramiko.Transport(self.ip, self.port)
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        """
        上传本地文件到服务器
        :param local_path:本地文件路径
        :param target_path:目标地址
        :return: None
        """
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        """
        下载服务器文件到本地
        :param remote_path:服务器文件
        :param local_path:本地地址
        :return:
        """
        #os.makedirs(local_path)
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def run_cmd(self, command):
        """
        执行shell命令
        :param command:命令
        :return:结果
        """
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        return result


if __name__ == '__main__':
    ssh = ConnectServer(ip="10.1.1.40", username="juzix", password="123456")
    ssh.connect()

    # 测试执行ssh脚本
    cmd = "cat /home/juzix/keyfile.json"
    cmd_result = ssh.run_cmd(cmd)
    print(cmd_result)

    # 测试下载文件
    downlod_remote_path = "/home/juzix/keyfile.json"
    downlod_local_path = "downloads/"+str(time.time())+".json"
    ssh.download(downlod_remote_path, downlod_local_path)

    # 测试上传文件
    upload_local_path = "downloads/1654162533.7210567.json"
    upload_remote_path = "/home/juzix/test/test.json"
    ssh.upload(upload_local_path, upload_remote_path)
    # 关闭连接
    ssh.close()


