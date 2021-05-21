select user,host,authentication_string,password_expired,account_locked
from mysql.user where user='' or host='' or host='%' or authentication_string='';