#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import time
import smtplib
import logging
from email.mime.text import MIMEText
import sys

LOG_FILENAME = "/var/log/email_python.log"
mail_host = 'custom.python.com'
mail_user = 'sales@python.com'
mail_pass = 'password'
mail_postfix = 'python.com'


def send_mail(to_list, subject, content, format='html'):
    try:
        me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
        msg = MIMEText(content,format,'utf-8')
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['Subject'] = subject
        msg['From'] = me
        msg['to'] = to_list
        s = smtplib.SMTP()
        s.connect(mail_host, "25")
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string().encode('ascii'))
        s.close()
    except Exception, e:
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
        logging.error(time.strftime('%Y-%m-%d %H:%I:%M', time.localtime(time.time())) + e)


if __name__ == "__main__":
    send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
