import re

"""
@class: Grammar 
@version: 1.0
@author: sidfate
@desc: compile mysql query
"""
class Grammar:
	selectComponents = (
		'fields',
		'tables',
		'wheres',
		'groups',
		'havings',
		'orders',
		'limits',
	)

	"""
	Compile a insert sql.
	@param  Builder query
	@param  dict    values
	@return string 
	"""
	def compileInsert(self, query, values):
		table = self.wrapTables(query.tables)
		columns = self.concatenate(",", values.keys())
		parameters = self.concatenate("','", values.values())
		return "insert into "+table+" ("+columns+") values ('"+parameters+"')"

	"""
	Compile a update sql.
	@param  Builder query
	@param  dict    values
	@return string 
	"""
	def compileUpdate(self, query, values):
		table = self.wrapTables(query.tables)
		columns = []
		if isinstance(values, dict):
			for k, v in values.items():
				columns.append(k+"='"+str(v)+"'")
		columns = self.concatenate(",", columns)
		return "update "+table+" set "+columns+" "+self.compileWheres(query, query.wheres)

	"""
	Compile a delete sql.
	@param  Builder query
	@return string 
	"""
	def compileDelete(self, query):
		table = self.wrapTables(query.tables)
		return "delete from "+table+" "+self.compileWheres(query, query.wheres)

	"""
	Compile a select sql.
	@param  Builder query
	@return string 
	"""
	def compileSelect(self, query):
		sql = []
		if not query.fields:
			query.fields = "*"
		for component in self.selectComponents: 
			if eval("query."+component):
				method = "compile"+component.capitalize()
				sql.append(eval("self."+method+"(query, query."+component+")"))
		return self.concatenate(" ", sql)

	"""
	Compile the select fields into a sql.
	@param  Builder query
	@param  list    fields
	@return string 
	"""
	def compileFields(self, query, fields):
		distinct = "distinct " if query.distinct is True else "";
		fields = self.compileColumns(fields)
		return "select "+distinct+fields
	
	"""
	Compile the fields into a sql.
	@param  Builder query
	@param  list    fields
	@return string 
	"""
	def compileColumns(self, fields):
		return self.concatenate(",", fields)

	"""
	Compile the from tables into a sql.
	@param  Builder query
	@param  list    tables
	@return string 
	"""
	def compileTables(self, query, tables):
		if not isinstance(tables, list) or len(tables)==0:
			return ""
		return "from "+self.concatenate(",", tables)
	
	"""
	Compile the tables into a sql.
	@param  list    tables
	@return string 
	"""	
	def wrapTables(self, tables):
		if not isinstance(tables, list) or len(tables)==0:
			return ""
		return self.concatenate(",", tables)

	"""
	Compile the group by into a sql.
	@param  Builder query
	@param  list    groups
	@return string 
	"""
	def compileGroups(self, query, groups):
		return "group by "+self.concatenate(",", groups)

	"""
	Compile the having into a sql.
	def compileHavings(self, query):
		pass
	"""

	"""
	Compile the order by into a sql.
	@param  Builder query
	@param  list    orders
	@return string 
	"""
	def compileOrders(self, query, orders):
		sql = []
		for order in orders:
			sql.append(order['sort']+" "+order['way'])
		return "order by "+self.concatenate(",", sql)

	"""
	Compile the limit into a sql.
	@param  Builder query
	@param  dict    limit
	@return string 
	"""
	def compileLimits(self, query, limit):
		return "limit "+str(limit['offset'])+","+str(limit['num'])

	"""
	Compile the where into a sql.
	@param  Builder query
	@param  list    wheres
	@return string 
	"""
	def compileWheres(self, query, wheres):
		sql = []
		for where in wheres:
			method = "where"+where['type'].capitalize()
			sql.append(where['boolean']+" "+eval("self."+method)(query, where))

		if len(sql) == 0:
			return ''
		regex = re.compile("^and |^or ")
		sql, number = re.subn(regex, '', self.concatenate(" ", sql))
		return "where "+sql

	"""
	Compile the basic where into a sql.
	@param  Builder query
	@param  dict  where
	@return string 
	"""
	def whereBasic(self, query, where):
		return where['field']+" "+where['operator']+" '"+str(where['value'])+"'"

	"""
	Compile the where in into a sql.
	@param  Builder query
	@param  dict  where
	@return string 
	"""
	def whereIn(self, query, where):
		_in = "not in" if where['not'] is True else "in"
		return where['field']+" "+_in+" ('"+self.concatenate("','", where['value'])+"')"  

	"""
	Compile the where between into a sql.
	@param  Builder query
	@param  dict  where
	@return string 
	"""
	def whereBetween(self, query, where):
		_between =  "not between" if where['not'] is True else "between"
		return where['field']+" "+_between+" "+self.concatenate(" and ", where['value'])

	"""
	Compile the where null into a sql.
	@param  Builder query
	@param  dict  where
	@return string 
	"""
	def whereNull(self, query, where):
		_null = "not null" if where['not'] is True else "null"
		return where['field']+" is "+_null

	"""
	Compile the basic where into a sql.
	@param  Builder query
	@param  dict  where
	@return string 
	"""
	def whereRaw(self, query, where):
		return where['sql']

	"""
	Concatenate the pieces with glue to a string.
	@param  string glue
	@param  list   pieces
	@return string 
	"""
	def concatenate(self, glue, pieces):
		return glue.join(str(i) for i in pieces)
