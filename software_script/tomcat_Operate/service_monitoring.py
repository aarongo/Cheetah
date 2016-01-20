#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import smtplib
from email.mime.text import MIMEText
import httplib
import logging


class Status_Email(object):
    def send_mail(self, smtp_server, user, postfix, send_list, sub, content):  # 发件人,邮箱后缀,收件人,主题,内容
        me = "172.31.1.101" + "<" + user + "@" + postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content, _subtype='html', _charset='gb2312')  # 创建一个实例，这里设置为html格式邮件
        msg['Subject'] = sub  # 设置主题
        msg['From'] = me
        msg['To'] = ";".join(send_list)
        try:
            s = smtplib.SMTP()
            s.connect(smtp_server, 25)  # 连接smtp服务器
            s.login(user, password)  # 登陆服务器
            s.sendmail(me, send_list, msg.as_string())  # 发送邮件
            s.close()
            return True
        except Exception, err:
            print str(err)
            return False

    # get Tomcat status code
    def get_status_code(self, host, path="/"):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status

        except StandardError:
            return None


if __name__ == '__main__':
    Mail = Status_Email()

    # set check urls
    host = "172.31.1.101" + ":8090"
    urls = "/mobile/api/user/login"
    # set check usrl --->end
    # set email parameter
    send_list = ["772603656@qq.com"]
    smtp_server = "smtp.126.com"  # 设置服务器
    user = "lonnyliu@126.com"  # 用户名
    password = "clzyzykcvryzqtzh"  # 口令
    postfix = "126.com"  # 发件箱的后缀
    sub = "Tomcat_Status"
    message = "Tomcat Mobile Troubleshoot service problems!!!! "
    # set email parameter -->end
    # if Mail.get_status_code(host, urls) != 200:
    #     if Mail.send_mail(smtp_server, user, postfix, send_list, sub, message):
    #         print "发送成功"
    #     else:
    #         print "发送失败"
    # else:
    #     print "\033[32mTomcat Mobile Is Normal\033[0m"
    log_filename = 'send_mail.log'
    log_format = ' [%(asctime)s]   %(message)s'
    logging.basicConfig(format=log_format, datafmt='%Y-%m-%d %H:%M:%S %p', level=logging.DEBUG, filename=log_filename)
    if Mail.send_mail(smtp_server, user, postfix, send_list, sub, message):
        logging.debug(message + "发送邮件")
        print "发送成功"
    else:
        print "发送失败"
