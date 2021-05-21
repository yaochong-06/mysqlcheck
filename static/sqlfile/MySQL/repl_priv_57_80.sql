select user,host,Grant_priv,password_expired,account_locked
from mysql.user where Repl_slave_priv='Y' and Repl_client_priv='Y';