select concat(VARIABLE_VALUE,'*')
from performance_schema.global_variables where variable_name in ('log_bin_basename');