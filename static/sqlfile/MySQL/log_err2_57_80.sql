select concat(datadir,substring(log_error,3)) as err_log_path
from
     (select variable_value as datadir from performance_schema.global_variables where variable_name='datadir') t1,
    (select variable_value as log_error from performance_schema.global_variables where variable_name='log_error') t2;