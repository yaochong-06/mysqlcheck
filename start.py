#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: start.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
from doc import get_mysql_doc_remote_linux, get_mysql_doc_remote_win, get_mysql_doc_local_linux, get_mysql_doc_local_win
from datetime import datetime
from data import command, command_local


def get_server_info(company_name, engineer_name, customer_name, customer_name2):
    res = open("static/server.info", encoding='utf-8').readlines()

    # 将server.info 密码文件转化成list
    for line in res:
        if not line.startswith('#'):
            info_list = line.lstrip('\n').rstrip('\n').replace('\n', ' ').replace('\t', ' ').split(' ')
            while '' in info_list:
                info_list.remove('')

            # Linux平台远程
            if len(info_list) == 9 and info_list[8] == 'Linux':
                get_mysql_doc_remote_linux(company_name, engineer_name, customer_name, customer_name2, info_list[0],
                                           info_list[1], info_list[2], info_list[3], info_list[4], info_list[5],
                                           info_list[6], info_list[7], info_list[8])
            # Windows平台远程
            elif len(info_list) == 9 and info_list[8] == 'Windows':
                get_mysql_doc_remote_win(company_name, engineer_name, customer_name, customer_name2, info_list[0],
                                         info_list[1], info_list[2], info_list[3], info_list[4], info_list[5],
                                         info_list[6], info_list[7] ,info_list[8])
            # Linux平台本地
            elif len(info_list) == 6 and info_list[5] == 'Linux' > 0:
                get_mysql_doc_local_linux(company_name, engineer_name, customer_name, customer_name2, info_list[0],
                                          info_list[1], info_list[2], info_list[3], info_list[4], info_list[5])
            # windows本地
            elif len(info_list) == 6 and info_list[5] == 'Windows':
                get_mysql_doc_local_win(company_name, engineer_name, customer_name, customer_name2, info_list[0],
                                        info_list[1], info_list[2], info_list[3], info_list[4], info_list[5])


def main():
    btime = datetime.now()

    company_name = ''
    engineer_name = ''
    customer_name = ''
    flag_company_name = '2'
    flag_engineer_name = '2'
    flag_customer_name = '2'
    flag_customer_name2 = '2'
    try:
        while company_name == '' or flag_company_name == '2':
            company_name = input("请输入本次巡检客户名称:")
            print("当前客户名称:", company_name)
            flag_company_name = input("确认选择1/重新输入选择2:")
        while engineer_name == '' or flag_engineer_name == '2':
            engineer_name = input("请输入本次巡检工程师姓名:")
            print("当前巡检工程师姓名:", engineer_name)
            flag_engineer_name = input("确认选择1/重新输入选择2:")
        while customer_name == '' or flag_customer_name == '2':
            customer_name = input("请输入客户第一对接人姓名:")
            print("客户第一对接人姓名:", customer_name)
            flag_customer_name = input("确认选择1/重新输入选择2:")
        while flag_customer_name == '2':
            customer_name2 = input("请输入客户第二对接人姓名，没有请回车：")
            print("客户第二对接人姓名:", customer_name2)
            flag_customer_name2 = input("确认选择1/重新输入选择2:")

        get_server_info(company_name, engineer_name, customer_name, customer_name2)

    except Exception as re:
        print(re)
    finally:
        etime = datetime.now()
        print(f"本次巡检完成，耗时{(etime - btime).seconds}秒")


if __name__ == '__main__':
    main()
