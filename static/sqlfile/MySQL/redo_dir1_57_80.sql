select concat(variable_value,'ib_logfile*') from performance_schema.global_variables
            where variable_name in ('datadir');