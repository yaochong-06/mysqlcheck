select VARIABLE_NAME, VARIABLE_VALUE
from information_schema.global_variables
where variable_name in ('master_info_repository','relay_log_info_repository','gtid_mode','enforce_gtid_consistency'
    ,'log_slave_updates','binlog_format','max_binlog_size','relay_log_recovery','binlog_gtid_simple_recovery'
    ,'slave_skip_errors','slave-parallel-type','slave-parallel-workers','super_read_only','read_only');