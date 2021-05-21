select concat(VARIABLE_VALUE,'ibdata*') from information_schema.global_variables
 where variable_name in ('datadir');