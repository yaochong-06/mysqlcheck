select concat(VARIABLE_VALUE,'ibdata*') from performance_schema.global_variables
where variable_name in ('innodb_data_home_dir');