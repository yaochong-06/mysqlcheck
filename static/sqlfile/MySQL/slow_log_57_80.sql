select VARIABLE_NAME, VARIABLE_VALUE from performance_schema.global_variables
where variable_name in
('long_query_time','log_queries_not_using_indexes','slow_query_log','slow_query_log_file','min_examined_row_limit','log_slow_admin_statements','log_slow_slave_statements');