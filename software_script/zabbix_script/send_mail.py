#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com

import smtplib
from email.mime.text import MIMEText
import sys

mail_host = 'custom.python.com'  # 发送邮件服务器
mail_user = 'sales@python.com'  # 发送邮件用户
mail_pass = 'password'  # 发送邮件密码
mail_postfix = 'python.com'  # 发送邮件后缀


def send_mail(to_address, subject, messages, format='plain'):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(messages, format, 'utf-8')
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_address
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_address, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == "__main__":
    if send_mail(sys.argv[1], sys.argv[2], sys.argv[3]):
        print "发送成功"
    else:
        print "发送失败"
