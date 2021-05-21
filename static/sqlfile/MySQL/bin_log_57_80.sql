select VARIABLE_NAME, VARIABLE_VALUE from performance_schema.global_variables
        where variable_name in ('sync_binlog');