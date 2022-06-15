import re
import socket
import threading

from urllib.parse import unquote
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText


# 定义函数将请求体字符串转化为字典格式
def msg_to_dict(msg):
    lst = msg.split('&')

    mdt = defaultdict(list)
    for i in lst:
        j = i.split('=')
        print(unquote(j[1]))  # urllib.parse中的unquote方法将请求体信息中的中文加密信息（含有%）解码为中文字符。
        mdt.setdefault('%s' % j[0], []).append(unquote(j[1]))
    return mdt


def sendmail(mail_type, mail_sender, password, mail_receiver, mail_subject, mail_content):
    if mail_type == 'qq':
        mail_host = "smtp.qq.com"
    elif mail_type == '163':
        mail_host = 'smtp.163.com'
    else:
        mail_host = 'smtp.126.com'

    msg = MIMEText(mail_content, 'plain', 'utf-8')
    msg['Subject'] = mail_subject
    msg['From'] = mail_sender
    msg['To'] = mail_receiver

    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_sender, password)
        server.sendmail(mail_sender, mail_receiver, msg.as_string())
        server.quit()
        print('邮件发送成功')
    except smtplib.SMTPException:
        print("Error: 邮件发送错误")


def service_client(new_socket):
    """为这个客户端返回数据"""
    # 1.接受浏览器发送过来的请求，即http请求
    # GET/HTTP/1.1
    # ...
    request = new_socket.recv(1024).decode("utf-8")
    # print(request)
    request_lines = request.splitlines()

    # GET (提取出:index.html file_name)
    file_name = ""
    ret = re.match(r"[^/]+(/)+([^ ]*)", request_lines[0])
    if ret:
        file_name = ret.group(2)

    try:
        f = open(file_name, "rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"
        response += "-------file not found-----"
        new_socket.send(response.encode("utf-8"))
    else:
        # 2.返回http格式的数据给浏览器
        response = "http/1.1 200 OK\r\n\r\n"
        # 2.1准备发送给浏览器的数据---header
        # 2.2准备发送给浏览器的数据---body
        html_content = f.read()
        f.close()
        # 发送header和body
        new_socket.send(response.encode("utf-8"))
        new_socket.send(html_content)

    mdt = msg_to_dict(request_lines[-1])

    mail_type = mdt['mailtype'][0]
    sender = mdt['sender'][0]
    password = mdt['password'][0]
    receiver = mdt['receiver'][0]
    subject = mdt['subject'][0]
    content = mdt['content'][0]
    sendmail(mail_type, sender, password, receiver, subject, content)

    # 3.关闭套接字
    new_socket.close()


def main():
    """用来完成整体控制"""
    # 1.创建套接字

    print("创建一个新的套接字")
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 2.绑定
    tcp_server_socket.bind(("", 7890))
    # 3.变为监听套接字
    tcp_server_socket.listen(128)
    # 4.等待新客户端的链接
    print("server is ready to serve...")

    while True:
        new_socket, client_addr = tcp_server_socket.accept()
        # 5.为这个客户端服务(分配一个线程)
        print("分配了一个线程")
        t = threading.Thread(target=service_client, args=(new_socket,))
        print(t.name)
        t.start()

    # 关闭套接字
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
