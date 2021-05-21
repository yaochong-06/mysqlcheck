select Variable_name,Variable_Value from performance_schema.global_status
where Variable_name in ('max_used_connections_time');