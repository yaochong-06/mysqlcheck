#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: doc.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
from docxtpl import DocxTemplate
from data import login_ssh, command, get_one, get_info_57_80, get_info_55_56, remove_last_line, get_one_local, \
    command_local, get_info_57_80_local, get_info_55_56_local
import time

'''
生成MySQL巡检doc文档
'''
current_time = time.strftime('%Y-%m-%d %H:%M:%S')
check_time = time.strftime('%Y-%m-%d')


def get_mysql_doc_linux(company_name, engineer_name, customer_name, customer_name2, *args):
    # server_id, mysql_user, mysql_password, mysql_port, business_name, platform, server_user,server_password, server_port,
    # server_id, mysql_user, mysql_password, mysql_port, business_name, platform
    tpl = DocxTemplate('static/tpl/MC_MySQL_tpl.docx')

    print(f"正在巡检{list(*args)[4]}系统, 请耐心等待...")

    if len(list(*args)) == 6:
        version = get_one_local(list(*args[0]), list(*args[1]), list(*args[2]), list(*args[3]), "version")
        if version[0:3] in ['5.5', '5.6']:
            info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
            redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
            user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
            share_set, tablespace_info = get_info_55_56_local(list(*args[0]), list(*args[1]), list(*args[2]),
                                                              list(*args[3]), list(*args[5]))
        elif version[0:3] in ['5.7', '8.0', '10.']:
            info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
            redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
            user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
            share_set, tablespace_info = get_info_57_80_local(list(*args[0]), list(*args[1]), list(*args[2]),
                                                              list(*args[3]), list(*args[5]))
        else:
            print("The version is not support.")
        os_set = command_local("cat /proc/meminfo |grep -E 'Mem|Cache|Swap|Huge'").replace(":", "").replace("kB",
                                                                                                            "").split(
            '\n')
        # 1.1 系统内存参数
        os_param = []
        for os in os_set:
            os = [x for x in os.split(' ') if x != '']
            if os != []:
                os[1] = round(int(os[1]) / 1024, 2)
                os_param.append(os)

        # 1.2 系统磁盘空间使用
        fs_set = command_local("df -hP").split('\n')
        space_param = []
        for space in fs_set[1:]:
            space_tmp = space.split(' ')
            space = [x for x in space_tmp if x != ''][0:6]
            if space != []:
                space[4] = int(space[4].replace('%', ''))
                space_param.append(space)

        context = {'company_name': company_name,
                   'engineer_name': engineer_name,
                   'business_name': list(*args)[4],
                   'c_name': customer_name,
                   'c_name2': customer_name2,
                   'check_time': check_time,
                   # 1.1 系统基础信息
                   'release': remove_last_line(command_local('cat /etc/redhat-release')),
                   'hostname': remove_last_line(command_local('hostname')),
                   'open_files': remove_last_line(command_local("""ulimit -a | grep files | awk '{print $4}'""")),
                   'max_user_processes': remove_last_line(
                       command_local("""ulimit -a | grep processes | awk '{print $5}'""")),

                   # 'hostname':command_local("hostname").replace("\n",""),

                   # 1.2 系统内存参数
                   'os_param': os_param,
                   # 1.3 系统CPU参数
                   # 物理CPU个数
                   'p_cpu_num': remove_last_line(
                       command_local("cat /proc/cpuinfo |grep 'physical id'|sort |uniq|wc -l")),
                   # 逻辑CPU个数
                   'l_cpu_num': remove_last_line(command_local("cat /proc/cpuinfo |grep 'processor'|wc -l")),
                   # CPU核心数
                   'cpu_cores': remove_last_line(
                       command_local("cat /proc/cpuinfo |grep 'cores'|uniq|awk '{print $4}'")),
                   # 每个物理CPU的核数
                   'core_per_p': remove_last_line(command_local("grep 'core id' /proc/cpuinfo | sort -u | wc -l")),
                   # CPU 主频
                   'cpu_clock_speed': remove_last_line(
                       command_local("cat /proc/cpuinfo | grep MHz | uniq | awk -F: '{print $2}'")),
                   # watchdog
                   'watchdog': remove_last_line(command_local("ps -ef | grep watchdogd | grep -v grep | wc -l")),

                   # 1.4 系统磁盘空间使用
                   'space_param': space_param,

                   # 1.5 数据库基本配置
                   'version': version,
                   'mysql_role': mysql_role,
                   'info_mysql': info_mysql,
                   # 1.6 数据库字符串信息
                   'lang_set': lang_set,
                   # 2.1 数据库资源
                   'sessions': sessions,
                   # 2.2 数据库内存参数设置
                   'memory_set': memory_set,
                   # 2.3数据库网络参数
                   'net_set': net_set,

                   'get_dirs': get_dirs,
                   'get_db_dirs': get_db_dirs,
                   'binlog': binlog,
                   'bin_dir': bin_dir,
                   'bin_set': bin_set,
                   'bin_cache': bin_cache,
                   # 3.5
                   'redolog': redolog,
                   'redo_set': redo_set,
                   'redo_size': redo_size,
                   # 3.6 undo文件设置
                   'undofile': undofile,
                   'null_user': null_user,
                   # 4.1 binlog
                   'bin_log': bin_log,
                   'redo_log': redo_log,
                   'general_log': general_log,
                   'slow_log': slow_log,
                   'user_grant_privs': user_grant_privs,
                   'all_priv': all_priv,
                   'super_priv': super_priv,
                   'repl_priv': repl_priv,
                   'big_tables': big_tables,
                   'big_index': big_index,
                   'have_no_primary_key': have_no_primary_key,
                   'gather_info': gather_info,
                   'repl_setting': repl_setting,
                   'repl_status': repl_status,
                   'err': err,
                   'log_err': log_err,
                   'share_set': share_set,
                   'tablespace_info': tablespace_info,
                   }

        tpl.render(context)
        tpl.save(f'./{list(*args)[0]}-{list(*args)[3]}-{list(*args)[4]}.docx')

    elif len(list(*args)) == 9:
        version = get_one(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8], list(*args)[1],
                          list(*args)[2], list(*args)[3], "version")
        if version[0:3] in ['5.5', '5.6', '10.']:
            info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
            redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
            user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
            share_set, tablespace_info = get_info_55_56(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                        list(*args)[1], list(*args)[2], list(*args)[3], list(*args)[5])
        elif version[0:3] in ['5.7', '8.0']:
            info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
            redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
            user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
            share_set, tablespace_info = get_info_57_80(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                        list(*args)[1], list(*args)[2], list(*args)[3], list(*args)[5])
        else:
            print("The version is not support.")
        os_set = command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                         "cat /proc/meminfo |grep -E 'Mem|Cache|Swap|Huge'").replace(":", "").replace("kB", "").split(
            '\n')
        os_param = []
        for os in os_set:
            os = [x for x in os.split(' ') if x != '']
            if os != []:
                os[1] = round(int(os[1]) / 1024, 2)
                os_param.append(os)

        # 1.2 系统磁盘空间使用
        # server_id, mysql_user, mysql_password, mysql_port, business_name, platform, server_user,server_password, server_port,
        fs_set = command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8], "df -hP").split('\n')
        space_param = []
        for space in fs_set[1:]:
            space_tmp = space.split(' ')
            space = [x for x in space_tmp if x != ''][0:6]
            if space != []:
                space[4] = int(space[4].replace('%', ''))
                space_param.append(space)

        # 1.1 系统内存参数

        context = {'company_name': company_name,
                   'engineer_name': engineer_name,
                   'business_name': list(*args)[4],
                   'c_name': customer_name,
                   'c_name2': customer_name2,
                   'check_time': check_time,
                   # 1.1 系统基础信息
                   'release': remove_last_line(
                       login_ssh(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                 'cat /etc/redhat-release')),
                   'hostname': remove_last_line(
                       login_ssh(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8], 'hostname')),
                   'open_files': remove_last_line(
                       login_ssh(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                 """ulimit -a | grep files | awk '{print $4}'""")),
                   'max_user_processes': remove_last_line(
                       login_ssh(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                 """ulimit -a | grep processes | awk '{print $5}'""")),
                   # 1.2 系统内存参数
                   'os_param': os_param,
                   # 1.3 系统CPU参数
                   # 物理CPU个数
                   'p_cpu_num': remove_last_line(command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                         "cat /proc/cpuinfo |grep 'physical id'|sort |uniq|wc -l")),
                   # 逻辑CPU个数
                   'l_cpu_num': remove_last_line(command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                         "cat /proc/cpuinfo |grep 'processor'|wc -l")),
                   # CPU核心数
                   'cpu_cores': remove_last_line(command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                         "cat /proc/cpuinfo |grep 'cores'|uniq|awk '{print $4}'")),
                   # 每个物理CPU的核数
                   'core_per_p': remove_last_line(
                       command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                               "grep 'core id' /proc/cpuinfo | sort -u | wc -l")),
                   # CPU 主频
                   'cpu_clock_speed': remove_last_line(
                       command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                               "cat /proc/cpuinfo | grep MHz | uniq | awk -F: '{print $2}'")),
                   # watchdog
                   'watchdog': remove_last_line(command(list(*args)[0], list(*args)[6], list(*args)[7], list(*args)[8],
                                                        "ps -ef | grep watchdogd | grep -v grep | wc -l")),

                   # 1.4 系统磁盘空间使用
                   'space_param': space_param,

                   # 1.5 数据库基本配置
                   'version': version,
                   'mysql_role': mysql_role,
                   'info_mysql': info_mysql,
                   # 1.6 数据库字符串信息
                   'lang_set': lang_set,
                   # 2.1 数据库资源
                   'sessions': sessions,
                   # 2.2 数据库内存参数设置
                   'memory_set': memory_set,
                   # 2.3数据库网络参数
                   'net_set': net_set,

                   'get_dirs': get_dirs,
                   'get_db_dirs': get_db_dirs,
                   'binlog': binlog,
                   'bin_dir': bin_dir,
                   'bin_set': bin_set,
                   'bin_cache': bin_cache,
                   # 3.5
                   'redolog': redolog,
                   'redo_set': redo_set,
                   'redo_size': redo_size,
                   # 3.6 undo文件设置
                   'undofile': undofile,
                   'null_user': null_user,
                   # 4.1 binlog
                   'bin_log': bin_log,
                   'redo_log': redo_log,
                   'general_log': general_log,
                   'slow_log': slow_log,
                   'user_grant_privs': user_grant_privs,
                   'all_priv': all_priv,
                   'super_priv': super_priv,
                   'repl_priv': repl_priv,
                   'big_tables': big_tables,
                   'big_index': big_index,
                   'have_no_primary_key': have_no_primary_key,
                   'gather_info': gather_info,
                   'repl_setting': repl_setting,
                   'repl_status': repl_status,
                   'err': err,
                   'log_err': log_err,
                   'share_set': share_set,
                   'tablespace_info': tablespace_info,
                   }

        tpl.render(context)
        tpl.save(f'./{list(*args)[0]}-{list(*args)[3]}-{list(*args)[4]}.docx')


def get_mysql_doc_remote_rds(company_name, engineer_name, customer_name, customer_name2, server_id, server_user,
                             server_password, server_port, mysql_user, mysql_password, mysql_port, business_name,
                             platform):
    tpl = DocxTemplate('static/tpl/MC_MySQLRDS_tpl.docx')

    print(f"正在巡检{business_name}系统, 请耐心等待...")

    version = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "version")
    if version[0:3] in ['5.5', '5.6', '10.']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_55_56(server_id, server_user, server_password, server_port, mysql_user,
                                                    mysql_password, mysql_port, platform)
    elif version[0:3] in ['5.7', '8.0']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_57_80(server_id, server_user, server_password, server_port, mysql_user,
                                                    mysql_password, mysql_port, platform)
    else:
        print("The version is not support.")

    context = {'company_name': company_name,
               'engineer_name': engineer_name,
               'business_name': business_name,
               'c_name': customer_name,
               'c_name2': customer_name2,
               'check_time': check_time,
               # 1.1 系统基础信息
               'release': remove_last_line(
                   login_ssh(server_id, server_user, server_password, server_port, 'cat /etc/redhat-release')),
               'hostname': remove_last_line(
                   login_ssh(server_id, server_user, server_password, server_port, 'hostname')),
               'open_files': remove_last_line(
                   login_ssh(server_id, server_user, server_password, server_port,
                             """ulimit -a | grep files | awk '{print $4}'""")),
               'max_user_processes': remove_last_line(
                   login_ssh(server_id, server_user, server_password, server_port,
                             """ulimit -a | grep processes | awk '{print $5}'""")),

               # 1.5 数据库基本配置
               'version': version,
               'mysql_role': mysql_role,
               'info_mysql': info_mysql,
               # 1.6 数据库字符串信息
               'lang_set': lang_set,
               # 2.1 数据库资源
               'sessions': sessions,
               # 2.2 数据库内存参数设置
               'memory_set': memory_set,
               # 2.3数据库网络参数
               'net_set': net_set,

               'get_dirs': get_dirs,
               'get_db_dirs': get_db_dirs,
               'binlog': binlog,
               'bin_dir': bin_dir,
               'bin_set': bin_set,
               'bin_cache': bin_cache,
               # 3.5
               'redolog': redolog,
               'redo_set': redo_set,
               'redo_size': redo_size,
               # 3.6 undo文件设置
               'undofile': undofile,
               'null_user': null_user,
               # 4.1 binlog
               'bin_log': bin_log,
               'redo_log': redo_log,
               'general_log': general_log,
               'slow_log': slow_log,
               'user_grant_privs': user_grant_privs,
               'all_priv': all_priv,
               'super_priv': super_priv,
               'repl_priv': repl_priv,
               'big_tables': big_tables,
               'big_index': big_index,
               'have_no_primary_key': have_no_primary_key,
               'gather_info': gather_info,
               'repl_setting': repl_setting,
               'repl_status': repl_status,
               'err': err,
               'log_err': log_err,
               'share_set': share_set,
               'tablespace_info': tablespace_info,
               }

    tpl.render(context)
    tpl.save(f'./{server_id}-{mysql_port}-{business_name}.docx')


def get_mysql_doc_remote_win(company_name, engineer_name, customer_name, customer_name2, server_id, server_user,
                             server_password, server_port, mysql_user, mysql_password, mysql_port, business_name,
                             platform):
    tpl = DocxTemplate('static/tpl/MC_MySQLWIN_tpl.docx')

    print(f"正在巡检{business_name}系统, 请耐心等待...")

    version = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "version")
    if version[0:3] in ['5.5', '5.6']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_55_56(server_id, server_user, server_password, server_port, mysql_user,
                                                    mysql_password, mysql_port, platform)
    elif version[0:3] in ['5.7', '8.0', '10.']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_57_80(server_id, server_user, server_password, server_port, mysql_user,
                                                    mysql_password, mysql_port, platform)
    else:
        print("The version is not support.")
    os_set = command(server_id, server_user, server_password, server_port,
                     remove_last_line('systeminfo | findstr "MB"')).replace(":", "").replace(',', '').replace("虚拟内存 ",
                                                                                                              '虚拟内存').replace(
        "MB", "").split('\n')

    # 1.1 系统内存参数
    os_param = []
    for os in os_set:
        os = [x for x in os.split(' ') if x != '']
        if os != []:
            os[1] = round(int(os[1]), 2)
            os_param.append(os)

    # 1.2 系统磁盘空间使用
    fs_set = command(server_id, server_user, server_password, server_port,
                     '''wmic LOGICALDISK where Description="Local Fixed Disk" get name,size,FreeSpace,FileSystem''').replace(
        '\r', '').split('\n')

    space_param = []
    for space in fs_set[1:]:
        space_tmp = space.split(' ')
        space = [x for x in space_tmp if x != ''][0:4]
        if space != []:
            space[1] = round(int(space[1]) / 1024 / 1024 / 1024, 2)
            space[3] = round(int(space[3]) / 1024 / 1024 / 1024, 2)
            space_param.append(space)

    context = {'company_name': company_name,
               'engineer_name': engineer_name,
               'business_name': business_name,
               'c_name': customer_name,
               'c_name2': customer_name2,
               'check_time': check_time,
               # 1.1 系统基础信息

               'release': remove_last_line(command(server_id, server_user, server_password, server_port, 'ver')),
               'hostname': remove_last_line(command(server_id, server_user, server_password, server_port, 'hostname')),

               # 1.2 系统内存参数
               'os_param': os_param,
               # 1.3 系统磁盘空间使用
               'space_param': space_param,

               # 1.4 数据库基本配置
               'version': version,
               'mysql_role': mysql_role,
               'info_mysql': info_mysql,
               # 1.5 数据库字符串信息
               'lang_set': lang_set,
               # 2.1 数据库资源
               'sessions': sessions,
               # 2.2 数据库内存参数设置
               'memory_set': memory_set,
               # 2.3数据库网络参数
               'net_set': net_set,

               'get_dirs': get_dirs,
               'get_db_dirs': get_db_dirs,
               'binlog': binlog,
               'bin_dir': bin_dir,
               'bin_set': bin_set,
               'bin_cache': bin_cache,
               # 3.5
               'redolog': redolog,
               'redo_set': redo_set,
               'redo_size': redo_size,
               # 3.6 undo文件设置
               'undofile': undofile,
               'null_user': null_user,
               # 4.1 binlog
               'bin_log': bin_log,
               'redo_log': redo_log,
               'general_log': general_log,
               'slow_log': slow_log,
               'user_grant_privs': user_grant_privs,
               'all_priv': all_priv,
               'super_priv': super_priv,
               'repl_priv': repl_priv,
               'big_tables': big_tables,
               'big_index': big_index,
               'have_no_primary_key': have_no_primary_key,
               'gather_info': gather_info,
               'repl_setting': repl_setting,
               'repl_status': repl_status,
               'err': err,
               'log_err': log_err,
               'share_set': share_set,
               'tablespace_info': tablespace_info,
               }

    tpl.render(context)
    tpl.save(f'./{server_id}-{mysql_port}-{business_name}.docx')


def get_mysql_doc_local_win(company_name, engineer_name, customer_name, customer_name2, server_id, mysql_user,
                            mysql_password, mysql_port, business_name, platform):
    tpl = DocxTemplate('static/tpl/MC_MySQLWIN_tpl.docx')

    print(f"正在巡检{business_name}系统, 请耐心等待...")
    version = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "version")
    if version[0:3] in ['5.5', '5.6']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_55_56_local(server_id, mysql_user, mysql_password, mysql_port, platform)
    elif version[0:3] in ['5.7', '8.0', '10.']:
        info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
        redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
        user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, \
        share_set, tablespace_info = get_info_57_80_local(server_id, mysql_user, mysql_password, mysql_port, platform)
    else:
        print("The version is not support.")
    os_set = command_local("cat /proc/meminfo |grep -E 'Mem|Cache|Swap|Huge'").replace(":", "").replace("kB", "").split(
        '\n')

    # 1.1 系统内存参数
    os_param = []
    for os in os_set:
        os = [x for x in os.split(' ') if x != '']
        if os != []:
            os[1] = round(int(os[1]), 2)
            os_param.append(os)

    # 1.2 系统磁盘空间使用
    fs_set = command_local(
        '''wmic LOGICALDISK where Description="Local Fixed Disk" get name,size,FreeSpace,FileSystem''').replace('\r',
                                                                                                                '').split(
        '\n')

    space_param = []
    for space in fs_set[1:]:
        space_tmp = space.split(' ')
        space = [x for x in space_tmp if x != ''][0:4]
        if space != []:
            space[1] = round(int(space[1]) / 1024 / 1024 / 1024, 2)
            space[3] = round(int(space[3]) / 1024 / 1024 / 1024, 2)
            space_param.append(space)

    context = {'company_name': company_name,
               'engineer_name': engineer_name,
               'business_name': business_name,
               'c_name': customer_name,
               'c_name2': customer_name2,
               'check_time': check_time,
               # 1.1 系统基础信息
               # 系统版本
               'release': remove_last_line(command_local('ver')),
               'hostname': remove_last_line(command_local('hostname')),

               # 1.2 系统内存参数
               'os_param': os_param,
               # 1.3 系统CPU参数
               # 物理CPU个数
               'p_cpu_num': remove_last_line(command_local("cat /proc/cpuinfo |grep 'physical id'|sort |uniq|wc -l")),
               # 逻辑CPU个数
               'l_cpu_num': remove_last_line(command_local("cat /proc/cpuinfo |grep 'processor'|wc -l")),
               # CPU核心数
               'cpu_cores': remove_last_line(command_local("cat /proc/cpuinfo |grep 'cores'|uniq|awk '{print $4}'")),
               # 每个物理CPU的核数
               'core_per_p': remove_last_line(command_local("grep 'core id' /proc/cpuinfo | sort -u | wc -l")),
               # CPU 主频
               'cpu_clock_speed': remove_last_line(
                   command_local("cat /proc/cpuinfo | grep MHz | uniq | awk -F: '{print $2}'")),
               # watchdog
               'watchdog': remove_last_line(command_local("ps -ef | grep watchdogd | grep -v grep | wc -l")),

               # 1.4 系统磁盘空间使用
               'space_param': space_param,

               # 1.5 数据库基本配置
               'version': version,
               'mysql_role': mysql_role,
               'info_mysql': info_mysql,
               # 1.6 数据库字符串信息
               'lang_set': lang_set,
               # 2.1 数据库资源
               'sessions': sessions,
               # 2.2 数据库内存参数设置
               'memory_set': memory_set,
               # 2.3数据库网络参数
               'net_set': net_set,

               'get_dirs': get_dirs,
               'get_db_dirs': get_db_dirs,
               'binlog': binlog,
               'bin_dir': bin_dir,
               'bin_set': bin_set,
               'bin_cache': bin_cache,
               # 3.5
               'redolog': redolog,
               'redo_set': redo_set,
               'redo_size': redo_size,
               # 3.6 undo文件设置
               'undofile': undofile,
               'null_user': null_user,
               # 4.1 binlog
               'bin_log': bin_log,
               'redo_log': redo_log,
               'general_log': general_log,
               'slow_log': slow_log,
               'user_grant_privs': user_grant_privs,
               'all_priv': all_priv,
               'super_priv': super_priv,
               'repl_priv': repl_priv,
               'big_tables': big_tables,
               'big_index': big_index,
               'have_no_primary_key': have_no_primary_key,
               'gather_info': gather_info,
               'repl_setting': repl_setting,
               'repl_status': repl_status,
               'err': err,
               'log_err': log_err,
               'share_set': share_set,
               'tablespace_info': tablespace_info,
               }

    tpl.render(context)
    tpl.save(f'./{server_id}-{mysql_port}-{business_name}.docx')
