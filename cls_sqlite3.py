import sqlite3
class DataBase(sqlite3.Connection):
	def __init__(self, filename):
		self.filename = filename
		self.db = sqlite3.Connection(self.filename)
		self.cursor = self.db.cursor()
	
	def create(self, table, **kwargs):
		var = ["{} {}".format(key.strip(), value.strip().upper()) for key, value in kwargs.items()]
		self.cursor.execute("CREATE TABLE IF NOT EXISTS {t}({v})".format(t=table, v=', '.join(var)))
		self.db.commit()
	
	def delete(self, table):
		self.cursor.execute("DROP TABLE {t}".format(t=table))
		self.db.commit()
	
	def log(self, table, **kwargs):
		keys = []
		for key in kwargs.keys():
			keys.append(key.strip())
		values = []
		for value in kwargs.values():
			values.append(value.strip())
		self.cursor.execute("INSERT INTO {t} ({k}) VALUES ({v})".format(t=table, k=', '.join(keys), v=', '.join(values)))
		self.db.commit()
	def search(self, table, **kwargs):
		assert len(kwargs) == 1
		for var, crit in kwargs.items():
			self.cursor.execute("SELECT * FROM {t} WHERE {v} {c}".format(t=table, v=var.strip(), c=crit.strip()))
			break
		for request in self.cursor.fetchall():
			yield request
	def search_with_and(self, table, **kwargs):
		assert len(kwargs) > 1
		crit = ["{v} {c}".format(v=key.strip(), c=value.strip()) for key, value in kwargs.items()]
		self.cursor.execute("SELECT * FROM {t} WHERE {c}".format(t=table, c=' AND '.join(crit)))
		for request in self.cursor.fetchall():
			yield request
	def search_with_or(self, table, **kwargs):
		assert len(kwargs) > 1
		crit = ["{v} {c}".format(v=key.strip(), c=value.strip()) for key, value in kwargs.items()]
		self.cursor.execute("SELECT * FROM {t} WHERE {c}".format(t=table, c=' OR '.join(crit)))
		for request in self.cursor.fetchall():
			yield request
