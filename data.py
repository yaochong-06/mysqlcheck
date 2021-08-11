#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time    : 2021/1/12 下午3:49
# @Author  : yaochong/Chongzi
# @FileName: data.py
# @Software: PyCharm
# @Blog    ：https://github.com/yaochong-06/ ; http://blog.itpub.net/29990276
import os, time, paramiko, pymysql, redis


# 获得redis脚本执行结果



def get_sqltext(filename):
    try:
        file_f = open('static/sqlfile/MySQL/' + filename + '.sql', 'r', encoding='utf-8')
        file_contents = file_f.read()
        file_f.close()
    except Exception as re:
        print(re)
    return file_contents


# 删除文件最后一行
def remove_last_line(s):
    return s[:s.rfind('\n')]


# 获得mysql脚本执行结果
def get_mysql_result(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                     sqlfile):
    try:

        # 打开数据库连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, password=mysql_password)
        cursor = connection.cursor()
        sql_text = get_sqltext(sqlfile)
        rows = cursor.execute(sql_text)
        # 获得当前sql的列名
        title = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            # 生成二维列表
            result_list.append(list(row))

        # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
        list_mysql_result_dict = []
        for i in result_list:
            tmp_dict = dict(zip(title, i))
            list_mysql_result_dict.append(tmp_dict)
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        cursor.close()
        connection.close()
        return list_mysql_result_dict


def get_mysql_result_local(server_id, mysql_user, mysql_password, mysql_port, sqlfile):
    try:

        # 打开数据库连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, password=mysql_password)
        cursor = connection.cursor()
        sql_text = get_sqltext(sqlfile)
        rows = cursor.execute(sql_text)
        # 获得当前sql的列名
        title = [i[0] for i in cursor.description]
        rows = cursor.fetchall()
        result_list = []
        for row in rows:
            # 生成二维列表
            result_list.append(list(row))

        # 将二维嵌套列表[['name','age'],['tom','11']]转换为列表包含字典[{'name':'tom','age':'11'}]
        list_mysql_result_dict = []
        for i in result_list:
            tmp_dict = dict(zip(title, i))
            list_mysql_result_dict.append(tmp_dict)
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        cursor.close()
        connection.close()
        return list_mysql_result_dict


def command(server_id, server_user, server_password, server_port, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 跳过了远程连接中选择‘是’的环节,
        ssh.connect(server_id, server_port, server_user, server_password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # 返回结果
        out = str(stdout.read(), 'gbk')
        return out
    except Exception as re:
        print(f"请确认主机{server_id}、端口是否连通{server_port}...")
        print(re)
    finally:
        ssh.close()


# local command
def command_local(cmd):
    # 返回结果
    out = os.popen(cmd, 'r', 100).read()
    return out


def login_ssh(server_id, server_user, server_password, server_port, scripts):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 跳过了远程连接中选择‘是’的环节,
        ssh.connect(server_id, server_port, server_user, server_password)
        stdin, stdout, stderr = ssh.exec_command(scripts)
        # 返回结果
        out = str(stdout.read(), 'utf-8')
        return out
    except Exception as re:
        print(f"请确认主机{server_id}、端口是否连通{server_port}...")
        print(re)
    finally:
        ssh.close()


def get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port, sqlfile):
    try:
        conn = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                               charset='utf8')
        cursor = conn.cursor()
        sql_text = get_sqltext(sqlfile)
        cursor.execute(sql_text)

        res = list(cursor.fetchall())
        res.sort()
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")

    finally:
        cursor.close()
        conn.close()
        return res


def get_all_local(server_id, mysql_user, mysql_password, mysql_port, sqlfile):
    try:
        conn = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                               charset='utf8')
        cursor = conn.cursor()
        sql_text = get_sqltext(sqlfile)
        cursor.execute(sql_text)

        res = list(cursor.fetchall())
        res.sort()
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")

    finally:
        cursor.close()
        conn.close()
        return res


def get_all_nosort(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                   sqlfile):
    try:
        # 创建连接
        conn = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                               charset='utf8')
        cursor = conn.cursor()
        sql_text = get_sqltext(sqlfile)
        # 执行SQL，并返回收影响行数
        cursor.execute(sql_text)
        res = list(cursor.fetchall())
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        # 关闭游标
        cursor.close()
        conn.close()
        return res


def get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, sqlfile):
    try:
        # 创建连接
        conn = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                               charset='utf8')
        cursor = conn.cursor()
        sql_text = get_sqltext(sqlfile)
        # 执行SQL，并返回收影响行数
        cursor.execute(sql_text)
        res = list(cursor.fetchall())
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        # 关闭游标
        cursor.close()
        conn.close()
        return res


def get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port, sqlfile):
    try:
        # 创建连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                                     charset='utf8')
        cursor = connection.cursor()
        sql_text = get_sqltext(sqlfile)
        # 执行SQL，并返回收影响行数
        cursor.execute(sql_text)
        res = cursor.fetchone()[0]
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        # 关闭游标和连接
        cursor.close()
        connection.close()
        return res


def get_one_local(server_id, mysql_user, mysql_password, mysql_port, sqlfile):
    try:
        # 创建连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, passwd=mysql_password,
                                     charset='utf8')
        cursor = connection.cursor()
        sql_text = get_sqltext(sqlfile)
        # 执行SQL，并返回收影响行数
        cursor.execute(sql_text)
        res = cursor.fetchone()[0]
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        # 关闭游标和连接
        cursor.close()
        connection.close()
        return res


def get_user_priv(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                  sql_text):
    try:

        # 打开数据库连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, password=mysql_password)
        cursor = connection.cursor()
        rows = cursor.execute(sql_text)
        rows = cursor.fetchall()
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        cursor.close()
        connection.close()
        return rows


def get_user_priv_local(server_id, mysql_user, mysql_password, mysql_port, sql_text):
    try:

        # 打开数据库连接
        connection = pymysql.connect(host=server_id, port=int(mysql_port), user=mysql_user, password=mysql_password)
        cursor = connection.cursor()
        rows = cursor.execute(sql_text)
        rows = cursor.fetchall()
    except Exception as re:
        print(re)
        print(f"连接创建失败,请检查当前MySQL用户名:{mysql_user}、密码:{mysql_password}、IP:{server_id}、端口:{mysql_port}等权限信息是否正确")
        print(f"{sql_text}...")
    finally:
        cursor.close()
        connection.close()
        return rows


def get_info_55_56(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                   platform):
    # mysql参数
    info_mysql = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "info_mysql_56")
    info_mysql = [(c[0].lower(), c[1]) for c in info_mysql]
    # 字符集参数
    lang_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "lang_set_56")
    lang_set = [(c[0].lower(), c[1], c[2]) for c in lang_set]

    # 数据库角色
    mysql_role = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "mysql_role_56")
    if mysql_role == []:
        mysql_role = ['master', 'master']
    if mysql_role[0][1] != 'Binlog Dump' and mysql_role[0][0] == 'system user':
        mysql_role = 'Slave'
    else:
        mysql_role = 'Master'
    # 连接数
    # max_used_connections 系统自从启动以来,最大连接数

    sessions_res = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                           "sessions_res_56")

    sessions = []
    for s in sessions_res:
        s = list(s)
        s[0] = s[0].lower()
        sessions.append(s)
    sessions.sort()

    sessions.append(['max_connections_time', '/'])
    sessions = [(c[0].lower(), c[1]) for c in sessions]

    # 内存参数
    memory_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "memory_set_56")
    query_cache_type = \
        get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                "query_cache_type_56")[0]
    memory_set.append(query_cache_type)
    memory_set = [(c[0].lower(), c[1]) for c in memory_set]

    # 网络参数
    net_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "net_set_56")

    # 空间管理
    dirs = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                   "dirs_56")
    dirs = [(c[0].lower(), c[1]) for c in dirs]
    try:
        get_dirs = []
        for dir in dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command(server_id, server_user, server_password, server_port,
                               "du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command(server_id, server_user, server_password, server_port,
                               'cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF BASEDIR.")
        get_dirs = []
        pass
    # 共享文件空间
    innodb_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "innodb_dir_56")
    try:
        if innodb_dir == '':
            share_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "share_dir1_56")
        else:
            share_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "share_dir2_56")

        # share_size = command("du -sh %s|awk '{print $1}'"%share_dir).replace("\n","")
        share_size = command(server_id, server_user, server_password, server_port, "du -sh %s" % share_dir).split('\n')
        share_set = []
        for space in share_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                share_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF SHARE_DATA_SPACE.")
        share_dirs = []
        pass

    # 各数据库大小
    db_dirs = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "db_dirs_56")
    try:
        get_db_dirs = []
        for dir in db_dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command(server_id, server_user, server_password, server_port,
                               "du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command(server_id, server_user, server_password, server_port,
                               'cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_db_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF DATABASE_SPACE.")
        get_db_dirs = []
        pass

    # 表空间文件
    per_table = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "per_table_56")
    if per_table == 'ON':
        tablespace_info = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user,
                                         mysql_password, mysql_port, "tablespace_info_56")
    else:
        tablespace_info = ''

    # 日志文件设置
    logbin = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                     "logbin_56")
    if logbin == 'ON':
        binlog = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "binlog_56")
        bin_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "bin_dir_56")
        cmd = "ls -lh --time-style '+%%Y/%%m/%%d %%H:%%M:%%S' %s|awk '{print $8,$6,$7,$5}'" % bin_dir
        bin_size = command(server_id, server_user, server_password, server_port, cmd).split("\n")
        bin_set = []
        for space in bin_size:
            space = [x for x in space.split(' ') if x != '']
            if space != []:
                bin_set.append(space)

        bin_cache = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                            mysql_port, "bin_cache_56")
        bin_cache = [(c[0].lower(), c[1]) for c in bin_cache]
        binlog = binlog[3:6] + binlog[0:3] + binlog[6:]
        binlog = [(c[0].lower(), c[1]) for c in binlog]

    else:
        binlog = ''
        bin_dir = ''
        bin_size = ''
        bin_set = ''
        bin_cache = ''
    # redo
    redolog = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "redolog_56")
    redolog = [[c[0].lower(), c[1]] for c in redolog]
    redolog[1][1] = int(redolog[1][1])
    redolog[0][1] = int(redolog[0][1])
    try:
        if redolog[2][1] == './':
            redo_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "redo_dir1_56")
        else:
            redo_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "redo_dir2_56")
        redo_size = command(server_id, server_user, server_password, server_port, "du -sh %s" % redo_dir).split('\n')
        redo_set = []
        for space in redo_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                redo_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF REDO.")
        redo_size = ''
        redo_set = []
        pass

    undofile = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "undofile_56")
    undofile = [(c[0].lower(), c[1]) for c in undofile]

    # 4 日志设置

    bin_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "bin_log_56")
    # 4.2
    redo_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "redo_log_56")

    # 4.3
    general_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "general_log_56")
    general_log = [(c[0].lower(), c[1]) for c in general_log]
    slow_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "slow_log_56")
    slow_log = [slow_log[2], slow_log[0], slow_log[1], slow_log[3], slow_log[4], slow_log[5], slow_log[6]]
    slow_log = [(c[0].lower(), c[1]) for c in slow_log]

    # 安全用户检查

    # 6.1 用户权限
    user_grant_privs = []
    priv_res = get_user_priv(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                             mysql_port,
                             """SELECT DISTINCT CONCAT('show grants for ''',user,'''@''',host,''';') AS query FROM mysql.user 
                             where user not in ('mysql.sys','mysql.session') and host <> '';""")

    for i in priv_res:
        user_grant_privs.append(
            get_user_priv(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          list(i)[0]))

    # 用户/密码为空 主机名为空(终端不限)
    null_user = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "null_user_56")
    null_user = [('用户名', '访问终端', '密码串', '密码过期')] + null_user

    # 若有输出，提示：以上用户或密码为空，或主机名为空(终端不限)，建议合理创建用户，提高用户安全级别！
    '''
    # 用户名密码相同
    same_user = get_all(server_id,server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,"select user,host,password,password_expired from mysql.user where password=password(user);")
    same_user = [('用户名', '访问终端', '密码串', '密码过期')] + same_user

    # 若有输出，提示：用户名密码相同，建议重新设置密码，提高用户安全级别！
    '''
    # 6.2 权限管理
    all_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "all_priv_56")

    all_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + all_priv

    super_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "super_priv_56")
    super_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + super_priv

    repl_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "repl_priv_56")
    repl_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + repl_priv

    # 大型表格
    big_tables = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "big_tables_56")

    # 大型索引
    big_index = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "big_index_56")

    # 无主键的表
    have_no_primary_key = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                  mysql_port, "have_no_primary_key_56")

    # 表索引统计信息
    gather_info = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "gather_info_56")[0]

    # 7主从复制和配置
    repl_setting = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                           "repl_setting_56")
    repl_status = get_mysql_result(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                   mysql_port, "repl_status_56")

    # 数据库错误日志检查

    check_log = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "check_log_56")

    if check_log == './':
        log_err = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "log_err2_56")
    else:
        log_err = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "log_err2_56")

    if log_err != 'NULL':
        date_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 60 * 24 * 30))
        row_num = command(server_id, server_user, server_password, server_port,
                          "cat -n %s|grep -w '%s'|head -n 1|awk '{print $1}'" % (log_err, date_time)).split('\n')[0]
        if row_num == '':
            err = command(server_id, server_user, server_password, server_port,
                          "tail -10000  %s|grep 'ERROR'" % (log_err)).split('\n')
        else:
            row_num = row_num
            err = command(server_id, server_user, server_password, server_port,
                          "tail -n +%s  %s|grep 'ERROR'" % (log_err, row_num)).split('\n')
        if err == ['']:
            err = ['最近数据库无报错。']
    else:
        err = ['最近数据库无报错。']
    return info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
           redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
           user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, share_set, tablespace_info


def get_info_57_80(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                   platform):
    # mysql参数
    # skip_name_resolve 建议开启
    info_mysql = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         'info_mysql_57_80')

    # 数据库字符串信息
    lang_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "lang_set_57_80")
    # 数据库角色
    mysql_role = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "mysql_role_57_80")
    if mysql_role == []:
        mysql_role = ['master', 'master']
    if mysql_role[0][1] != 'Binlog Dump' and mysql_role[0][0] == 'system user':
        mysql_role = 'Slave'
    else:
        mysql_role = 'Master'

    # 连接数
    sessions_res = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                           "sessions_res_80")
    max_connections_time = \
        get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                "max_connections_time_57_80")[0]

    sessions = []
    for s in sessions_res:
        s = list(s)
        s[0] = s[0].lower()
        sessions.append(s)
    sessions.sort()
    max_connections_time = [a.lower() for a in max_connections_time]
    sessions.append(max_connections_time)

    # 内存参数
    memory_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "memory_set_57_80")
    query_cache_type = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "query_cache_type_57_80")
    if len(memory_set) == 3:
        memory_set.append(['query_cache_type', '/'])
        memory_set.append(['query_cache_size', '/'])
    else:
        memory_set.append(query_cache_type[0])

    # 网络参数
    net_set = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "net_set_57_80")

    # 空间管理
    dirs = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                   "dirs_57_80")
    try:
        get_dirs = []
        for dir in dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command(server_id, server_user, server_password, server_port,
                               "du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command(server_id, server_user, server_password, server_port,
                               'cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF BASEDIR.")
        get_dirs = []
        pass
    # 共享文件空间
    innodb_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "innodb_dir_57_80")
    try:
        if innodb_dir == '':
            share_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "share_dir1_57_80")
        else:
            share_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "share_dir2_57_80")
        # share_size = command("du -sh %s|awk '{print $1}'"%share_dir).replace("\n","")
        share_size = command(server_id, server_user, server_password, server_port, "du -sh %s" % share_dir).split('\n')
        share_set = []
        for space in share_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                share_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF SHARE_DATA_SPACE.")
        share_dirs = []
        pass

    # 各数据库大小
    db_dirs = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "db_dirs_57_80")
    try:
        get_db_dirs = []
        for dir in db_dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command(server_id, server_user, server_password, server_port,
                               "du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command(server_id, server_user, server_password, server_port,
                               'cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_db_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF DATABASE_SPACE.")
        get_db_dirs = []
        pass

    # 表空间文件
    per_table = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "per_table_57_80")
    if per_table == 'ON':
        tablespace_info = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user,
                                         mysql_password, mysql_port, "tablespace_info_57_80")
    else:
        tablespace_info = ''

    # 日志文件设置
    logbin = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                     "logbin_57_80")
    if logbin == 'ON':
        binlog = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "binlog_57_80")
        bin_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "bin_dir_57_80")
        cmd = "ls -lh --time-style '+%%Y/%%m/%%d %%H:%%M:%%S' %s|awk '{print $8,$6,$7,$5}'" % bin_dir
        bin_size = command(server_id, server_user, server_password, server_port, cmd).split("\n")
        bin_set = []
        for space in bin_size:
            space = [x for x in space.split(' ') if x != '']
            if space != []:
                bin_set.append(space)

        bin_cache = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                            mysql_port, "bin_cache_57_80")
        bin_cache = [(c[0].lower(), c[1]) for c in bin_cache]
        binlog = binlog[3:6] + binlog[0:3] + binlog[6:]
    else:
        binlog = ''
        bin_dir = ''
        bin_size = ''
        bin_set = ''
        bin_cache = ''
    # redo
    redolog = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "redolog_57_80")
    redolog = [list(redolog[1]), list(redolog[0]), list(redolog[2])]
    redolog[1][1] = int(redolog[1][1])
    redolog[0][1] = int(redolog[0][1])

    try:
        if redolog[2][1] == './':
            redo_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "redo_dir1_57_80")
        else:
            redo_dir = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "redo_dir2_57_80")
        redo_size = command(server_id, server_user, server_password, server_port, "du -sh %s" % redo_dir).split('\n')
        redo_set = []
        for space in redo_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                redo_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF REDO.")
        redo_size = ''
        redo_set = []
        pass

    undofile = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "undofile_57_80")

    # 4.日志设置
    # 4.1
    bin_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                      "bin_log_57_80")

    redo_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "redo_log_57_80")

    # 4.3 general log

    general_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "general_log_57_80")

    slow_log = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "slow_log_57_80")
    slow_log = [slow_log[2], slow_log[0], slow_log[1], slow_log[3], slow_log[4], slow_log[5], slow_log[6]]

    # 安全用户检查
    # 用户/密码为空 主机名为空(终端不限)

    # 6.1 用户权限
    user_grant_privs = []
    priv_res = get_user_priv(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                             mysql_port,
                             """SELECT DISTINCT CONCAT('show grants for ''',user,'''@''',host,''';') AS query FROM mysql.user
                             where user not in ('mysql.sys','mysql.session') and host <> '';""")
    for i in priv_res:
        user_grant_privs.append(
            get_user_priv(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          list(i)[0]))

    null_user = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "null_user_57_80")
    null_user = [('用户名', '访问终端', '密码串', '密码过期', '用户锁定')] + null_user

    # 若有输出，提示：以上用户或密码为空，或主机名为空(终端不限)，建议合理创建用户，提高用户安全级别！
    '''
    # 用户名密码相同

    same_user = get_all(server_id,server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,"select user,host,authentication_string,password_expired,account_locked \
        from mysql.user where authentication_string=password(user);")
    same_user = [('用户名', '访问终端', '密码串', '密码过期', '用户锁定')] + same_user

    # 若有输出，提示：用户名密码相同，建议重新设置密码，提高用户安全级别！
    '''
    # 6.2 权限管理
    all_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                       "all_priv_57_80")
    all_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + all_priv

    super_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                         "super_priv_57_80")
    super_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + super_priv

    repl_priv = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "repl_priv_57_80")
    repl_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + repl_priv

    # 大型表格
    big_tables = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                mysql_port, "big_tables_57_80")

    # 大型索引
    big_index = get_all_nosort(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                               mysql_port, "big_index_57_80")

    # 表无索引
    have_no_primary_key = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                  mysql_port, "have_no_primary_key_57_80")

    # 表索引统计信息
    gather_info = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "gather_info_57_80")[0]

    # 7主从复制和配置
    repl_setting = get_all(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                           "repl_setting_57_80")
    repl_status = get_mysql_result(server_id, server_user, server_password, server_port, mysql_user, mysql_password,
                                   mysql_port, "repl_status_80")

    # 数据库错误日志检查
    check_log = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                        "check_log_57_80")
    if check_log == './':
        log_err = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "log_err2_57_80")
    else:
        log_err = get_one(server_id, server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,
                          "log_err1_57_80")

    if log_err != 'NULL':
        date_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 60 * 24 * 30))
        row_num = command(server_id, server_user, server_password, server_port,
                          "cat -n %s|grep -w '%s'|head -n 1|awk '{print $1}'" % (log_err, date_time)).split('\n')[0]
        if row_num == '':
            err = command(server_id, server_user, server_password, server_port,
                          "tail -10000  %s|grep 'ERROR'" % (log_err)).split('\n')
        else:
            row_num = row_num
            err = command(server_id, server_user, server_password, server_port,
                          "tail -n +%s  %s|grep 'ERROR'" % (log_err, row_num)).split('\n')

        if err == ['']:
            err = ['最近数据库无报错。']
    else:
        err = ['最近数据库无报错。']
    return info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
           redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
           user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, share_set, tablespace_info


def get_info_55_56_local(server_id, mysql_user, mysql_password, mysql_port, platform):
    # mysql参数
    info_mysql = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "info_mysql_56")
    info_mysql = [(c[0].lower(), c[1]) for c in info_mysql]
    # 字符集参数
    lang_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "lang_set_56")
    lang_set = [(c[0].lower(), c[1], c[2]) for c in lang_set]

    # 数据库角色
    mysql_role = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "mysql_role_56")
    if mysql_role == []:
        mysql_role = ['master', 'master']
    if mysql_role[0][1] != 'Binlog Dump' and mysql_role[0][0] == 'system user':
        mysql_role = 'Slave'
    else:
        mysql_role = 'Master'
    # 连接数
    # max_used_connections 系统自从启动以来,最大连接数

    sessions_res = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "sessions_res_56")

    sessions = []
    for s in sessions_res:
        s = list(s)
        s[0] = s[0].lower()
        sessions.append(s)
    sessions.sort()

    sessions.append(['max_connections_time', '/'])
    sessions = [(c[0].lower(), c[1]) for c in sessions]

    # 内存参数
    memory_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "memory_set_56")
    query_cache_type = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "query_cache_type_56")[0]
    memory_set.append(query_cache_type)
    memory_set = [(c[0].lower(), c[1]) for c in memory_set]

    # 网络参数
    net_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "net_set_56")

    # 空间管理
    dirs = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "dirs_56")
    dirs = [(c[0].lower(), c[1]) for c in dirs]
    try:
        get_dirs = []
        for dir in dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command_local("du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command_local('cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF BASEDIR.")
        get_dirs = []
        pass
    # 共享文件空间
    innodb_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "innodb_dir_56")
    try:
        if innodb_dir == '':
            share_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "share_dir1_56")
        else:
            share_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "share_dir2_56")

        # share_size = command("du -sh %s|awk '{print $1}'"%share_dir).replace("\n","")
        share_size = command_local("du -sh %s" % share_dir).split('\n')
        share_set = []
        for space in share_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                share_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF SHARE_DATA_SPACE.")
        share_dirs = []
        pass

    # 各数据库大小
    db_dirs = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "db_dirs_56")
    try:
        get_db_dirs = []
        for dir in db_dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command_local("du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command('cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_db_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF DATABASE_SPACE.")
        get_db_dirs = []
        pass

    # 表空间文件
    per_table = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "per_table_56")
    if per_table == 'ON':
        tablespace_info = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, "tablespace_info_56")
    else:
        tablespace_info = ''

    # 日志文件设置
    logbin = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "logbin_56")
    if logbin == 'ON':
        binlog = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "binlog_56")
        bin_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "bin_dir_56")
        cmd = "ls -lh --time-style '+%%Y/%%m/%%d %%H:%%M:%%S' %s|awk '{print $8,$6,$7,$5}'" % bin_dir
        bin_size = command_local(cmd).split("\n")
        bin_set = []
        for space in bin_size:
            space = [x for x in space.split(' ') if x != '']
            if space != []:
                bin_set.append(space)

        bin_cache = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "bin_cache_56")
        bin_cache = [(c[0].lower(), c[1]) for c in bin_cache]
        binlog = binlog[3:6] + binlog[0:3] + binlog[6:]
        binlog = [(c[0].lower(), c[1]) for c in binlog]

    else:
        binlog = ''
        bin_dir = ''
        bin_size = ''
        bin_set = ''
        bin_cache = ''
    # redo
    redolog = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "redolog_56")
    redolog = [[c[0].lower(), c[1]] for c in redolog]
    redolog[1][1] = int(redolog[1][1])
    redolog[0][1] = int(redolog[0][1])
    try:
        if redolog[2][1] == './':
            redo_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "redo_dir1_56")
        else:
            redo_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "redo_dir2_56")
        redo_size = command_local("du -sh %s" % redo_dir).split('\n')
        redo_set = []
        for space in redo_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                redo_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF REDO.")
        redo_size = ''
        redo_set = []
        pass

    undofile = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "undofile_56")
    undofile = [(c[0].lower(), c[1]) for c in undofile]

    # 4 日志设置

    bin_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "bin_log_56")
    # 4.2
    redo_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "redo_log_56")
    # 4.3
    general_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "general_log_56")
    general_log = [(c[0].lower(), c[1]) for c in general_log]
    slow_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "slow_log_56")
    slow_log = [slow_log[2], slow_log[0], slow_log[1], slow_log[3], slow_log[4], slow_log[5], slow_log[6]]
    slow_log = [(c[0].lower(), c[1]) for c in slow_log]

    # 安全用户检查

    # 6.1 用户权限
    user_grant_privs = []
    priv_res = get_user_priv_local(server_id, mysql_user, mysql_password, mysql_port,
                                   """SELECT DISTINCT CONCAT('show grants for ''',user,'''@''',host,''';') AS query FROM mysql.user
                                   where user not in ('mysql.sys','mysql.session') and host <> '';""")

    for i in priv_res:
        user_grant_privs.append(get_user_priv_local(server_id, mysql_user, mysql_password, mysql_port, list(i)[0]))

    # 用户/密码为空 主机名为空(终端不限)
    null_user = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "null_user_56")
    null_user = [('用户名', '访问终端', '密码串', '密码过期')] + null_user

    # 若有输出，提示：以上用户或密码为空，或主机名为空(终端不限)，建议合理创建用户，提高用户安全级别！
    '''
    # 用户名密码相同
    same_user = get_all_local(server_id,server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,"select user,host,password,password_expired from mysql.user where password=password(user);")
    same_user = [('用户名', '访问终端', '密码串', '密码过期')] + same_user

    # 若有输出，提示：用户名密码相同，建议重新设置密码，提高用户安全级别！
    '''
    # 权限管理
    all_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "all_priv_56")
    all_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + all_priv

    super_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "super_priv_56")
    super_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + super_priv

    repl_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "repl_priv_56")
    repl_priv = [('用户名', '访问终端', '权限可传递', '密码过期')] + repl_priv

    # 大型表格
    big_tables = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, "big_tables_56")

    # 大型索引
    big_index = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, "big_index_56")

    # 无主键的表
    have_no_primary_key = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "have_no_primary_key_56")

    # 表索引统计信息
    gather_info = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "gather_info_56")[0]

    # 7主从复制和配置
    repl_setting = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "repl_setting_56")
    repl_status = get_mysql_result_local(server_id, mysql_user, mysql_password, mysql_port, "repl_status_56")

    # 数据库错误日志检查

    check_log = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "check_log_56")
    if check_log == './':
        log_err = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "log_err2_56")
    else:
        log_err = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "log_err2_56")

    if log_err != 'NULL':
        date_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 60 * 24 * 30))
        row_num = command_local("cat -n %s|grep -w '%s'|head -n 1|awk '{print $1}'" % (log_err, date_time)).split('\n')[
            0]
        if row_num == '':
            err = command_local("tail -10000  %s|grep 'ERROR'" % (log_err)).split('\n')
        else:
            row_num = row_num
            err = command_local("tail -n +%s  %s|grep 'ERROR'" % (log_err, row_num)).split('\n')
        if err == ['']:
            err = ['最近数据库无报错。']
    else:
        err = ['最近数据库无报错。']
    return info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
           redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
           user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, share_set, tablespace_info


def get_info_57_80_local(server_id, mysql_user, mysql_password, mysql_port, platform):
    # mysql参数
    # skip_name_resolve 建议开启
    info_mysql = get_all_local(server_id, mysql_user, mysql_password, mysql_port, 'info_mysql_57_80')

    # 数据库字符串信息
    lang_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "lang_set_57_80")
    # 数据库角色
    mysql_role = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "mysql_role_57_80")
    if mysql_role == []:
        mysql_role = ['master', 'master']
    if mysql_role[0][1] != 'Binlog Dump' and mysql_role[0][0] == 'system user':
        mysql_role = 'Slave'
    else:
        mysql_role = 'Master'

    # 连接数
    sessions_res = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "sessions_res_80")
    max_connections_time = \
        get_all_local(server_id, mysql_user, mysql_password, mysql_port, "max_connections_time_57_80")[0]

    sessions = []
    for s in sessions_res:
        s = list(s)
        s[0] = s[0].lower()
        sessions.append(s)
    sessions.sort()
    max_connections_time = [a.lower() for a in max_connections_time]
    sessions.append(max_connections_time)

    # 内存参数
    memory_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "memory_set_57_80")
    query_cache_type = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "query_cache_type_57_80")
    if len(memory_set) == 3:
        memory_set.append(['query_cache_type', '/'])
        memory_set.append(['query_cache_size', '/'])
    else:
        memory_set.append(query_cache_type[0])

    # 网络参数
    net_set = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "net_set_57_80")

    # 空间管理
    dirs = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "dirs_57_80")
    try:
        get_dirs = []
        for dir in dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command_local("du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command('cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")
            else:
                size = 0
            dir.append(size)
            get_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF BASEDIR.")
        get_dirs = []
        pass
    # 共享文件空间
    innodb_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "innodb_dir_57_80")
    try:
        if innodb_dir == '':
            share_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "share_dir1_57_80")
        else:
            share_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "share_dir2_57_80")
        # share_size = command("du -sh %s|awk '{print $1}'"%share_dir).replace("\n","")
        share_size = command_local("du -sh %s" % share_dir).split('\n')
        share_set = []
        for space in share_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                share_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF SHARE_DATA_SPACE.")
        share_dirs = []
        pass

    # 各数据库大小
    db_dirs = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "db_dirs_57_80")
    try:
        get_db_dirs = []
        for dir in db_dirs:
            dir = list(dir)
            size = ''
            if dir[1] != '' and platform == 'Linux':
                size = command_local("du -sh %s|awk '{print $1}'" % dir[1]).replace("\n", "")
            elif dir[1] != '' and platform == 'Windows':
                size = command_local('cd %s && dir /w  | findstr "文件"' % dir[1]).replace("\n", "").replace(" ", "")

            else:
                size = 0
            dir.append(size)
            get_db_dirs.append(dir)
    except:
        print("ERROR:DO NOT GET INFO OF DATABASE_SPACE.")
        get_db_dirs = []
        pass

    # 表空间文件
    per_table = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "per_table_57_80")
    if per_table == 'ON':
        tablespace_info = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port,
                                               "tablespace_info_57_80")
    else:
        tablespace_info = ''

    # 日志文件设置
    logbin = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "logbin_57_80")
    if logbin == 'ON':
        binlog = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "binlog_57_80")
        bin_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "bin_dir_57_80")
        cmd = "ls -lh --time-style '+%%Y/%%m/%%d %%H:%%M:%%S' %s|awk '{print $8,$6,$7,$5}'" % bin_dir
        bin_size = command_local(cmd).split("\n")
        bin_set = []
        for space in bin_size:
            space = [x for x in space.split(' ') if x != '']
            if space != []:
                bin_set.append(space)

        bin_cache = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "bin_cache_57_80")
        bin_cache = [(c[0].lower(), c[1]) for c in bin_cache]
        binlog = binlog[3:6] + binlog[0:3] + binlog[6:]
    else:
        binlog = ''
        bin_dir = ''
        bin_size = ''
        bin_set = ''
        bin_cache = ''
    # redo
    redolog = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "redolog_57_80")
    redolog = [list(redolog[1]), list(redolog[0]), list(redolog[2])]
    redolog[1][1] = int(redolog[1][1])
    redolog[0][1] = int(redolog[0][1])

    try:
        if redolog[2][1] == './':
            redo_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "redo_dir1_57_80")
        else:
            redo_dir = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "redo_dir2_57_80")
        redo_size = command_local("du -sh %s" % redo_dir).split('\n')
        redo_set = []
        for space in redo_size:
            space = [x for x in space.split('\t') if x != '']
            if space != []:
                redo_set.append(space)
    except:
        print("ERROR:DO NOT GET INFO OF REDO.")
        redo_size = ''
        redo_set = []
        pass

    undofile = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "undofile_57_80")

    # 4.日志设置
    # 4.1
    bin_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "bin_log_57_80")

    redo_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "redo_log_57_80")

    # 4.3 general log

    general_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "general_log_57_80")

    slow_log = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "slow_log_57_80")
    slow_log = [slow_log[2], slow_log[0], slow_log[1], slow_log[3], slow_log[4], slow_log[5], slow_log[6]]

    # 安全用户检查
    # 用户/密码为空 主机名为空(终端不限)

    # 6.1 用户权限
    user_grant_privs = []
    priv_res = get_user_priv_local(server_id, mysql_user, mysql_password, mysql_port,
                                   """SELECT DISTINCT CONCAT('show grants for ''',user,'''@''',host,''';') AS query FROM mysql.user 
                                   where user not in ('mysql.sys','mysql.session') and host <> '';""")
    for i in priv_res:
        user_grant_privs.append(get_user_priv_local(server_id, mysql_user, mysql_password, mysql_port, list(i)[0]))

    null_user = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "null_user_57_80")
    null_user = [('用户名', '访问终端', '密码串', '密码过期', '用户锁定')] + null_user

    # 若有输出，提示：以上用户或密码为空，或主机名为空(终端不限)，建议合理创建用户，提高用户安全级别！
    '''
    # 用户名密码相同

    same_user = get_all_local(server_id,server_user, server_password, server_port, mysql_user, mysql_password, mysql_port,"select user,host,authentication_string,password_expired,account_locked \
        from mysql.user where authentication_string=password(user);")
    same_user = [('用户名', '访问终端', '密码串', '密码过期', '用户锁定')] + same_user

    # 若有输出，提示：用户名密码相同，建议重新设置密码，提高用户安全级别！
    '''
    # 权限管理
    all_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "all_priv_57_80")
    all_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + all_priv

    super_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "super_priv_57_80")
    super_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + super_priv

    repl_priv = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "repl_priv_57_80")
    repl_priv = [('用户名', '访问终端', '权限可传递', '密码过期', '用户锁定')] + repl_priv

    # 大型表格
    big_tables = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, "big_tables_57_80")

    # 大型索引
    big_index = get_all_nosort_local(server_id, mysql_user, mysql_password, mysql_port, "big_index_57_80")

    # 表无索引
    have_no_primary_key = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "have_no_primary_key_57_80")

    # 表索引统计信息
    gather_info = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "gather_info_57_80")[0]

    # 7主从复制和配置
    repl_setting = get_all_local(server_id, mysql_user, mysql_password, mysql_port, "repl_setting_57_80")
    repl_status = get_mysql_result_local(server_id, mysql_user, mysql_password, mysql_port, "repl_status_80")

    # 数据库错误日志检查
    check_log = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "check_log_57_80")
    if check_log == './':
        log_err = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "log_err2_57_80")
    else:
        log_err = get_one_local(server_id, mysql_user, mysql_password, mysql_port, "log_err1_57_80")
    if log_err != 'NULL':
        date_time = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 60 * 24 * 30))
        row_num = command_local("cat -n %s|grep -w '%s'|head -n 1|awk '{print $1}'" % (log_err, date_time)).split('\n')[
            0]
        if row_num == '':
            err = command_local("tail -10000  %s|grep 'ERROR'" % (log_err)).split('\n')
        else:
            row_num = row_num
            err = command_local("tail -n +%s  %s|grep 'ERROR'" % (log_err, row_num)).split('\n')
        if err == ['']:
            err = ['最近数据库无报错。']
    else:
        err = ['最近数据库无报错。']
    return info_mysql, lang_set, mysql_role, sessions, memory_set, net_set, get_dirs, get_db_dirs, binlog, bin_dir, bin_set, bin_cache, \
           redolog, redo_set, redo_size, undofile, null_user, bin_log, redo_log, general_log, slow_log, \
           user_grant_privs, all_priv, super_priv, repl_priv, big_tables, big_index, have_no_primary_key, gather_info, repl_setting, repl_status, err, log_err, share_set, tablespace_info
