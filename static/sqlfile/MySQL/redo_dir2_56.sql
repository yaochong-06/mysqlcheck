select concat(variable_value,'ib_logfile*') from information_schema.global_variables
where variable_name in ('innodb_log_group_home_dir');