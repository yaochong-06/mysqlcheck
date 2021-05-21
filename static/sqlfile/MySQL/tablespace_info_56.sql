select table_schema,
       table_name,
       concat(table_name,'.ibd') as tbs_file,
       round((data_length+index_length)/1024/1024,2) as tbs_size
from information_schema.tables
where table_schema not in ('information_schema','performance_schema','mysql','sys')
order by 4 desc
limit 5;