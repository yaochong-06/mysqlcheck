select Variable_name, cast(Variable_Value as signed)
from performance_schema.global_variables
where Variable_name in (''max_connections'', ''max_user_connections'', ''max_connect_errors'')
union all
select Variable_name, cast(Variable_Value as signed)
from performance_schema.global_status
where Variable_name in (''max_used_connections'', ''Threads_connected'', ''Threads_running'');