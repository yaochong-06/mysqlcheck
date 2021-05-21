select Tabs_StatCollect_7day_ago,Total_tabs,
    concat(round((Total_tabs-Tabs_StatCollect_7day_ago)/Total_tabs,2)*100,'%')
    as Tabs_CollectRate,Inds_StatCollect_7day_ago,Total_inds,
    concat(round((Total_inds-Inds_StatCollect_7day_ago)/Total_inds,2)*100,'%')
    as Inds_CollectRate from (select count(distinct database_name,table_name)
    as Tabs_StatCollect_7day_ago from mysql.innodb_table_stats WHERE database_name not
    in ('information_schema','performance_schema','mysql')
    and last_update < date_sub(current_timestamp(),interval 7 DAY))t1,(select count(distinct database_name,table_name)
    as Total_tabs from mysql.innodb_table_stats where database_name not
    in ('information_schema','performance_schema','mysql'))t2,(select count(distinct database_name,table_name,index_name)
    as Inds_StatCollect_7day_ago from mysql.innodb_index_stats WHERE database_name not
    in ('information_schema','performance_schema','mysql')
    and last_update < date_sub(current_timestamp(),interval 7 DAY))t3,
    (select count(distinct database_name,table_name,index_name)
    as Total_inds from mysql.innodb_index_stats where database_name not
    in ('information_schema','performance_schema','mysql'))t4;