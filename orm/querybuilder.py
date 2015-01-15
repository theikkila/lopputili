import orm
import dbwords


#(date text, trans text, symbol text, qty real, price real
def createTable(db, model):
	field_names = orm.getfields(model)
	fields = []
	for field_name in field_names:
		f = getattr(model, field_name)
		ft = orm.fieldtype(field_name, model)
		sqtype = dbwords.gettype(db, ft) % getattr(model, field_name).meta
		field = field_name + " " + sqtype
		fields.append(field)
	return 'CREATE TABLE {table} ({fields})'.format(table=model.tableName(), fields=", ".join(fields))
	