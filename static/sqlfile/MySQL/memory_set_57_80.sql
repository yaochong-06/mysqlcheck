select VARIABLE_NAME, floor(VARIABLE_VALUE/1024/1024) M
from performance_schema.global_variables where variable_name
in ('bulk_insert_buffer_size','innodb_buffer_pool_size','innodb_log_buffer_size','query_cache_size');