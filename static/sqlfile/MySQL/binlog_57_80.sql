select VARIABLE_NAME, VARIABLE_VALUE
from performance_schema.global_variables
where variable_name in
('log_bin','LOG_BIN_BASENAME','expire_logs_days','binlog_format','log_bin_index','binlog_cache_size','max_binlog_cache_size','max_binlog_size','binlog_row_image');