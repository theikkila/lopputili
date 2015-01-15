
data_types_sqlite = {
    'AutoField': 'integer',
    'BinaryField': 'BLOB',
    'BooleanField': 'bool',
    'CharField': 'varchar(%(max_length)s)',
    'DateField': 'date',
    'DateTimeField': 'datetime',
    'DecimalField': 'decimal',
    'DurationField': 'bigint',
    'FloatField': 'real',
    'IntegerField': 'integer',
    'BigIntegerField': 'bigint',
    'NullBooleanField': 'bool',
    'OneToOneField': 'integer',
    'PositiveIntegerField': 'integer unsigned',
    'PositiveSmallIntegerField': 'smallint unsigned',
    'SmallIntegerField': 'smallint',
    'TextField': 'text',
    'TimeField': 'time',
    'UUIDField': 'char(32)'
}

operators_sqlite = {
    'exact': '= %s',
    'iexact': "LIKE %s ESCAPE '\\'",
    'contains': "LIKE %s ESCAPE '\\'",
    'icontains': "LIKE %s ESCAPE '\\'",
    'regex': 'REGEXP %s',
    'iregex': "REGEXP '(?i)' || %s",
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': "LIKE %s ESCAPE '\\'",
    'endswith': "LIKE %s ESCAPE '\\'",
    'istartswith': "LIKE %s ESCAPE '\\'",
    'iendswith': "LIKE %s ESCAPE '\\'",
}

data_types_postgres = {
    'AutoField': 'serial',
    'BinaryField': 'bytea',
    'BooleanField': 'boolean',
    'CharField': 'varchar(%(max_length)s)',
    'DateField': 'date',
    'DateTimeField': 'timestamp with time zone',
    'DurationField': 'interval',
    'FloatField': 'double precision',
    'IntegerField': 'integer',
    'BigIntegerField': 'bigint',
    'IPAddressField': 'inet',
    'GenericIPAddressField': 'inet',
    'NullBooleanField': 'boolean',
    'OneToOneField': 'integer',
    'PositiveIntegerField': 'integer',
    'PositiveSmallIntegerField': 'smallint',
    'SmallIntegerField': 'smallint',
    'TextField': 'text',
    'TimeField': 'time',
    'UUIDField': 'uuid'
}

operators_postgres = {
    'exact': '= %s',
    'iexact': '= UPPER(%s)',
    'contains': 'LIKE %s',
    'icontains': 'LIKE UPPER(%s)',
    'regex': '~ %s',
    'iregex': '~* %s',
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': 'LIKE %s',
    'endswith': 'LIKE %s',
    'istartswith': 'LIKE UPPER(%s)',
    'iendswith': 'LIKE UPPER(%s)',
}

def data_types(db):
	if db == "sqlite":
		return data_types_sqlite
	elif db == "postgresql":
		return data_types_postgres


def gettype(db, field):
	return data_types(db)[field]