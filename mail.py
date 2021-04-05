#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def SendEmail(subject, content="content"):
    #设置服务器所需信息
    #qq邮箱服务器地址
    mail_host = 'smtp.qq.com'
    #qq用户名
    mail_user = '903204149@qq.com'
    #密码(部分邮箱为授权码) 
    mail_pass = 'bpwvgahtqmoqbbif'
    #邮件发送方邮箱地址
    sender = '903204149@qq.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['huangyukun2012@163.com', 'hykhyy@qq.com']

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题
    message['Subject'] = subject
    #发送方信息
    message['From'] = sender
    #接受方信息
    message['To'] = receivers[0]

    for i in range(2):
        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP() 
            #连接到服务器
            #smtpObj.connect(mail_host,25)
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass)
            #发送
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            #退出
            smtpObj.quit()
            return True
        except smtplib.SMTPException as e:
            print('error',e) #打印错误
    return False


