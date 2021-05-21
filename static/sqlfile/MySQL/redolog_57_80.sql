select VARIABLE_NAME, VARIABLE_VALUE
from performance_schema.global_variables where variable_name
in ('innodb_log_file_size','innodb_log_files_in_group', 'innodb_log_group_home_dir','innodb_mirrored_log_groups');