#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/12/4'
#   motto:  'Good memory as bad written'

import paramiko
import getpass


def ssh_clients(hostname=None, port=22, username=None, password=None, command=None, nbytes=4096):
    client = paramiko.Transport((hostname, port))
    client.connect(username=username, password=password)

    stdout_data = []
    stderr_data = []
    session = client.open_channel(kind='session')
    session.exec_command(command)
    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
            break
    print "\033[31m*********************\033[0m"
    print '\033[32mExit status is: \033[0m', session.recv_exit_status()
    print "\033[31m*********************\033[0m"
    print ''.join(stdout_data)
    print ''.join(stderr_data)
    session.close()
    client.close()


if __name__ == '__main__':
    host_list = ['172.31.1.160', '172.31.1.101', '10.90.6.21']
    print "\033[31m     **********IPaddress List**********      \033[0m"
    for index, value in enumerate(host_list):
        print index, value
    chose_ip = raw_input("\033[32mPlease Connection Host IP Or Host Name:\033[0m").strip()
    if chose_ip.isdigit():
        chose_ip = int(chose_ip)
        hostname = host_list[chose_ip]
    username = raw_input("\033[32mPlease Input Will Connection Host User:\033[0m").strip()
    password = getpass.getpass("\033[32mEnter You Password:\033[0m").strip()
    if len(username) == 0 and len(password) == 0:
        username = 'root'
        password = 'comall2014'
    command = raw_input("\033[32mPlease Input Will Running Command:\033[0m").strip()
    ssh_clients(hostname=hostname, username=username, password=password, command=command)
    print "\033[32m--------------------SSH_Connection Info--------------------\033[0m"
    print "\033[32m|    **********SSH_Connection-->Host:%s\033[0m" % hostname
    print "\033[32m|    **********SSH_Connection-->User:%s\033[0m" % username
    print "\033[32m|    **********SSH_Connection-->Passwd:%s\033[0m" % password
    print "\033[32m|    **********SSH_Connection-->RunCMD:%s\033[0m" % command
    print "\033[32m--------------------SSH_Connection END--------------------\033[0m"
