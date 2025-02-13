import os

import paramiko
import requests

def execute_ssh_commands(hostname, port, username, password, commands):
    """
    ���ӵ�SSH��������ִ�ж������
    :param hostname: SSH����������������IP��ַ
    :param port: SSH�������Ķ˿ںţ�Ĭ����22
    :param username: ��¼SSH���������û���
    :param password: ��¼SSH������������
    :param commands: Ҫ��Զ�̷�������ִ�е������б�
    :return: ���������ʹ�����Ϣ
    """
    try:
        # ����SSH�ͻ��˶���
        ssh = paramiko.SSHClient()

        # �Զ����������Կ
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # ���ӵ�SSH������
        ssh.connect(hostname=hostname, port=port, username=username, password=password)

        # �������б���ϳ�һ���ַ�����ÿ������֮���÷ֺŷָ�
        command_string = commands

        # ִ������
        stdin, stdout, stderr = ssh.exec_command(command_string)

        # ��ȡ��������ʹ�����Ϣ
        output = stdout.read().decode()
        error = stderr.read().decode()

        # �ر�SSH����
        ssh.close()

        # ��������ʹ�����Ϣ
        return output, error

    except Exception as e:
        return None, str(e)

def startApp():
    hostname = os.environ.get("hostname")
    port = int(os.environ.get("port","22"))

    username = os.environ.get("username")
    password = os.environ.get("password")
    commands = os.environ.get("command")

    output, error = execute_ssh_commands(hostname, port, username, password, commands)

    if error:
        print("Error:", error)
    else:
        print("Output:", output)

# ʾ������
if __name__ == "__main__":
    url = os.environ.get("url")
    resp = requests.request("get",url)

    if resp.status_code == 200:
        print("״̬����")
    else:
        print("״̬�쳣��" + str(resp.status_code))

    if resp.status_code == 502:
        print("ǰ����������")
        startApp()