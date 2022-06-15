"""
# -*- coding = utf-8 -*-
#!/usr/bin/env python
# @Project : multiMailServer
# @File : sendMail.py
# @Author : ycy
# @time : 2022/6/15 17:09
# @Software : PyCharm Professional
"""
import smtplib
from email.mime.text import MIMEText


def sendmail(mail_type, mail_sender, password, mail_receiver, mail_subject, mail_content):
    # 判断用户选择的邮箱类型，选择smtp服务器
    if mail_type == 'qq':
        mail_host = "smtp.qq.com"
    elif mail_type == '163':
        mail_host = 'smtp.163.com'
    else:
        mail_host = 'smtp.126.com'

    # 发送纯文本格式的邮件
    msg = MIMEText(mail_content, 'plain', 'utf-8')
    msg['Subject'] = mail_subject  # 发送邮件的主题
    msg['From'] = mail_sender  # 发送地址
    msg['To'] = mail_receiver  # 收件地址

    try:
        server = smtplib.SMTP_SSL(mail_host, 465)  # 建立连接
        server.login(mail_sender, password)  # login()方法用来登录SMTP服务器
        server.sendmail(mail_sender, mail_receiver, msg.as_string())  # 发送邮件
        server.quit()
        print('邮件发送成功')
    except smtplib.SMTPException:
        print("Error: 邮件发送错误")
