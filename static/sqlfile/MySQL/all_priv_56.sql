select user,host,Grant_priv,password_expired from mysql.user
        where Select_priv='Y' and Insert_priv='Y' and Update_priv='Y' and Delete_priv='Y'
            and Create_priv='Y' and Drop_priv='Y' and Reload_priv='Y' and Shutdown_priv='Y'
                and Process_priv='Y' and File_priv='Y' and References_priv='Y' and Index_priv='Y'
                    and Alter_priv='Y' and Show_db_priv='Y' and Super_priv='Y' and Create_tmp_table_priv='Y'
                        and Lock_tables_priv='Y' and Execute_priv='Y' and Repl_slave_priv='Y' and Repl_client_priv='Y'
                            and Create_view_priv='Y' and Show_view_priv='Y' and Create_routine_priv='Y'
                                and Alter_routine_priv='Y' and Create_user_priv='Y'
                                    and Event_priv='Y' and Trigger_priv='Y' and Create_tablespace_priv='Y';