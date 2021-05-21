select VARIABLE_NAME, VARIABLE_VALUE from performance_schema.global_variables
where variable_name in ('innodb_undo_directory','INNODB_UNDO_LOGS','innodb_undo_tablespaces');