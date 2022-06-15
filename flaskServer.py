"""
# -*- coding = utf-8 -*-
#!/usr/bin/env python
# @Project : multiMailServer
# @File : flaskServer.py
# @Author : ycy
# @time : 2022/6/13 16:19
# @Software : PyCharm Professional
"""
from flask import Flask, render_template, request
from sendMail import sendmail

app = Flask(__name__)


# 建立路由，方法为get和post方法
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':

        # 获取form表单提交的邮件发送数据
        mail_type = request.form.get('mailtype')
        sender = request.form.get('sender')
        password = request.form.get('password')
        receiver = request.form.get('receiver')
        subject = request.form.get('subject')
        content = request.form.get('content')

        if "@" not in sender or receiver:
            return render_template('input_error.html')

        # print(mail_type, sender, password, receiver, subject, content)

        try:
            sendmail(mail_type, sender, password, receiver, subject, content)
            return render_template('success.html')
        except IOError:
            print("发送失败")
            return render_template('fail.html')


if __name__ == '__main__':
    app.run()
