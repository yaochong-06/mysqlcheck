select VARIABLE_NAME, VARIABLE_VALUE from performance_schema.global_variables
where variable_name in
('port','pid_file','socket','server_id','innodb_page_size','innodb_file_per_table','default_storage_engine','transaction_isolation','autocommit',
'innodb_file_format','tmpdir','CHARACTER_SET_SERVER','COLLATION_SERVER','CHARACTER_SET_DATABASE','COLLATION_CONNECTION','skip_name_resolve',
 'innodb_doublewrite','innodb_fast_shutdown');