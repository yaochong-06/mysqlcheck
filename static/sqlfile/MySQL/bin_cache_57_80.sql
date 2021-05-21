select variable_name,variable_value from performance_schema.global_status
        where variable_name in ('Binlog_cache_disk_use','Binlog_cache_use');