SELECT TABLE_SCHEMA,
       TABLE_NAME,
       round(DATA_LENGTH/1024/1024,2) as table_size
FROM information_schema.TABLES
WHERE table_schema not in ('information_schema','performance_schema','mysql','sys')
ORDER BY 3 DESC limit 5;