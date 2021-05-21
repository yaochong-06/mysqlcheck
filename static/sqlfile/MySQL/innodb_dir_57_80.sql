select VARIABLE_VALUE from performance_schema.global_variables
where variable_name in ('innodb_data_home_dir');