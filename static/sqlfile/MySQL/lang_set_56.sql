select SCHEMA_NAME,DEFAULT_CHARACTER_SET_NAME,DEFAULT_COLLATION_NAME
from information_schema.SCHEMATA where SCHEMA_NAME not in('information_schema','performance_schema','mysql','sys');