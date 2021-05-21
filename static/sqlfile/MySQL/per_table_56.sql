select VARIABLE_VALUE from information_schema.global_variables
where variable_name in ('innodb_file_per_table');