select VARIABLE_NAME, VARIABLE_VALUE
from information_schema.global_variables
where variable_name in ('log_output','general_log','general_log_file');