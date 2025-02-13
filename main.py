# encoding: utf-8
import os
import json

import paramiko
import requests

CONFIGS = os.environ["CONFIGS"]
def execute_ssh_commands(hostname, port, username, password, commands):
    """
    连接到SSH服务器并执行多条命令。
    :param hostname: SSH服务器的主机名或IP地址
    :param port: SSH服务器的端口号，默认是22
    :param username: 登录SSH服务器的用户名
    :param password: 登录SSH服务器的密码
    :param commands: 要在远程服务器上执行的命令列表
    :return: 命令的输出和错误信息
    """
    try:
        # 创建SSH客户端对象
        ssh = paramiko.SSHClient()

        # 自动添加主机密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接到SSH服务器
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        # 将命令列表组合成一个字符串，每条命令之间用分号分隔
        command_string = commands

        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command_string)

        # 获取命令输出和错误信息
        output = stdout.read().decode()
        error = stderr.read().decode()

        # 关闭SSH连接
        ssh.close()

        # 返回输出和错误信息
        return output, error

    except Exception as e:
        return None, str(e)


def startApp():
    hostname = CONFIGS.get("HOSTNAME")
    port = int(CONFIGS.get("PORT", "22"))

    username = CONFIGS.get("USERNAME")
    password = CONFIGS.get("PASSWORD")
    commands = CONFIGS.get("COMMAND")

    output, error = execute_ssh_commands(hostname, port, username, password, commands)

    if error:
        print("Error:", error)
    else:
        print("Output:", output)


# 示例调用
if __name__ == "__main__":
    print(os.environ["secrets.HOSTNAME"])
    # url = CONFIGS.get("URL")
    # resp = requests.request("get", url)
    #
    # if resp.status_code == 200:
    #     print("状态正常")
    # else:
    #     print("状态异常：" + str(resp.status_code))
    #
    # if resp.status_code == 502:
    #     print("前往启动服务")
    #     startApp()
