#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com



from requests import ConnectionError
from requests import get
from requests import codes
import datetime


def check_status(url):
    try:
        print u'开始执行Check<---->%s' % datetime.datetime.now().strftime('%H:%M:%S')
        req = get(url, timeout=30)
        if req.status_code == codes.ok:
            print u'结束Check<---->%s' % datetime.datetime.now().strftime('%H:%M:%S')
            return req.status_code
        else:
            print u'结束Check%s' % datetime.datetime.now().strftime('%H:%M:%S')
            return req.status_code
    except ConnectionError as error:
        print u'URL访问超时30s,URL不存在或者网络不可达'
        print u'结束Check<---->%s' % datetime.datetime.now().strftime('%H:%M:%S')


def view_status_info(code):
    u"""
    1 **：请求收到，继续处理
    2 **：操作成功收到，分析、接受
    3 **：完成此请求必须进一步处理
    4 **：请求包含一个错误语法或不能完成
    5 **：服务器执行一个完全有效请求失败
    :param code:
    :return:
    """
    dict_code = {
        '1xx Informational': {
            '100': u'客户必须继续发出请求',
            '101': u'客户要求服务器根据请求转换HTTP协议版本',
            '102': u'服务端正在处理请求'
        },
        '2xx Success': {
            '200': u'该请求成功!!!',
            '201': u'该请求已完成，结果是创建了新的资源',
            '202': u'该请求已被接受为处理，但是该处理尚未完成',
            '203': u'该请求返回信息不确定或不完整',
            '204': u'该请求收到，但返回信息为空',
            '205': u'服务器已完成要求和用户代理应该重置引起发送请求的文档视图',
            '206': u'服务器已经完成了部分用户的GET请求'
        },
        '3xx Redirection': {
            '300': u'请求的资源可在多处得到',
            '301': u'删除请求数据',
            '302': u'在其他地址发现了请求数据',
            '303': u'建议客户访问其他URL或访问方式',
            '304': u'客户端已经执行了GET，但文件未变化',
            '305': u'所请求的资源必须通过位置字段给出的代理来访问',
            '306': u'前一版本HTTP中使用的代码，现行版本中不再使用',
            '307': u'申明请求的资源临时性删除',
        },
        '4xx Client Error': {
            '400': u'错误请求，如语法错误',
            '401': u'请求需要用户验证',
            '402': u'保留有效ChargeTo头响应',
            '403': u'请求被拒绝',
            '404': u'没有发现文件、查询或URl',
            '405': u'在Request-Line中指定的方法不允许',
            '406': u'根据用户发送的Accept，请求资源不可访问',
            '407': u'类似401，用户必须首先在代理服务器上得到授权',
            '408': u'客户端没有在用户指定的时间内完成请求',
            '409': u'请求无法完成，由于与资源的当前状态冲突',
            '410': u'请求的资源不再可用在服务器上',
            '411': u'服务器拒绝用户定义的Content-Length属性请求',
            '412': u'一个或多个请求头字段在当前请求中错误',
            '413': u'请求的资源大于服务器允许的大小',
            '414': u'请求的资源URL长于服务器允许的长度',
            '415': u'请求资源不支持请求项目格式',
            '416': u'请求中包含Range请求头字段，在当前请求资源范围内没有range指示值，请求也不包含If-Range请求头字段',
            '417': u'服务器不满足请求Expect头字段指定的期望值，如果是代理服务器，可能是下一级服务器不能满足请求'
        },
        '5xx Server Error': {
            '500': u'服务器产生内部错误',
            '501': u'服务器不支持请求的函数',
            '502': u'服务器暂时不可用，有时是为了防止发生系统过载',
            '503': u'服务器过载或暂停维修',
            '504': u'网关口过载，服务器使用另一个关口或服务来响应用户，等待时间设定值较长',
            '505': u'服务器不支持或拒绝支请求头中指定的HTTP版本',

        }

    }
    u'''
    遍历多层字典方法
        1.首先遍历整个字典
        2.遍历首次遍历的结果的 value 进行第二次遍历,获取到值
    '''
    for key1, value1 in dict_code.items():
        for key2, value2 in value1.items():
            if int(key2) == code:
                print u'返回状态码为:' + u'\033[32m%s\033[0m' % code + '<---->' + u'状态码检测结果:\033[32m%s\033[0m' % value2


if __name__ == '__main__':
    url = "http://172.31.20.10"
    print u'开始检测url<---->%s' % url
    view_status_info(check_status(url))
