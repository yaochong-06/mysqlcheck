select a.TABLE_SCHEMA,a.TABLE_NAME from
(select TABLE_SCHEMA,TABLE_NAME from information_schema.tables where TABLE_SCHEMA not in ('mysql','information_schema','performance_schema','sys')) a
left join
(select TABLE_SCHEMA,TABLE_NAME from information_schema.statistics where index_name = 'primary' and TABLE_SCHEMA not in ('mysql','information_schema','performance_schema','sys')) b
on a.TABLE_SCHEMA=b.TABLE_SCHEMA
       and a.TABLE_NAME=b.TABLE_NAME
where b.TABLE_NAME is null;