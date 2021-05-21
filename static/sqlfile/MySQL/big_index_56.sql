select distinct a.table_schema,
                a.table_name,
                a.index_name,
                round(b.INDEX_LENGTH/1024/1024,2) as index_size
from information_schema.STATISTICS a,information_schema.TABLES b
where a.table_schema not in ('information_schema','performance_schema','mysql','sys')
  and a.table_schema=b.table_schema
  and a.table_name=b.table_name
order by 4 desc limit 5;