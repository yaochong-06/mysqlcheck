select VARIABLE_NAME, VARIABLE_VALUE
    from information_schema.global_variables where variable_name
    in ('query_cache_type');