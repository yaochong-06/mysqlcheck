select user,command from information_schema.PROCESSLIST
where command='Binlog Dump' or USER='system user';