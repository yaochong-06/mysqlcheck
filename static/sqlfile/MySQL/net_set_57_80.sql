select VARIABLE_NAME, VARIABLE_VALUE from information_schema.global_variables
where variable_name in
('wait_timeout','interactive_timeout','max_allowed_packet',
 'net_read_timeout','net_write_timeout','net_buffer_length','connect_timeout','skip_name_resolve','skip_networking');