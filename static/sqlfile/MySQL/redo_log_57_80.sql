select VARIABLE_NAME, VARIABLE_VALUE from performance_schema.global_variables
where variable_name in ('innodb_flush_log_at_trx_commit');