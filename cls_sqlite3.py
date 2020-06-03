import sqlite3 as sql
class DataBase ():
	def __init__(self, name = 'database.db', table = 'users', **var):
		self.name = name
		self.table = table
		variables = []
		for i in var.keys():
			variables.append(i.strip() + ' ' + var[i].strip())
		self.variables = variables
		variables_sqlite3_format = ''
		for i in range(len(variables) - 1):
			variables_sqlite3_format += variables[i] + ', '
		else:
			variables_sqlite3_format += variables[len(variables) - 1]
		self.db = sql.connect(self.name)
		self.cursor = self.db.cursor()
		self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({variables_sqlite3_format})")
	def log(self, **value):
		values_keys_list = []
		values_values_list = []
		for i in value.keys():
			values_keys_list.append(i.strip())
			values_values_list.append(str(value[i]).strip())
		values_keys_sqlite3_format = ''
		values_values_sqlite3_format = ''
		for i in range(len(values_keys_list) - 1):
			values_keys_sqlite3_format += values_keys_list[i] + ', '
			values_values_sqlite3_format += values_values_list[i] + ', '
		else:
			values_keys_sqlite3_format += values_keys_list[len(values_keys_list) - 1]
			values_values_sqlite3_format += values_values_list[len(values_values_list) - 1]
		self.cursor.execute(f"INSERT INTO {self.table} ({values_keys_sqlite3_format}) VALUES ({values_values_sqlite3_format})")
		self.db.commit()
	def search(self, **parametr):
		result = []
		for i in parametr.items():
			try:
				self.cursor.execute(f"SELECT * FROM {self.table} WHERE {i[0]} = '{parametr[i[0]]}'")
			except KeyError:
				pass
			except sql.OperationalError:
				pass
			else:
				result.append(self.cursor.fetchall())
		return result
