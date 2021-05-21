select b,concat(a,b) as OBJECTS from
((select VARIABLE_VALUE as a from performance_schema.global_variables
where variable_name in ('datadir'))t1,(select schema_name as b from information_schema.SCHEMATA
where schema_name not in ('information_schema','performance_schema','mysql','sys'))t2);