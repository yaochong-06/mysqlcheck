select VARIABLE_VALUE
from information_schema.global_variables
where variable_name in ('innodb_data_home_dir');