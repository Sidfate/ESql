import re

"""
@class: Grammar 
@version: 1.0
@author: sidfate
@desc: MySQL grammar class
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

	def compileSelect(self, query):
		sql = []
		if not query.fields:
			query.fields = "*"
		for component in self.selectComponents: 
			if eval("query."+component):
				method = "compile"+component.capitalize()
				sql.append(eval("self."+method+"(query, query."+component+")"))
		return self.concatenate(" ", sql)

	def compileFields(self, query, fields):
		distinct = "distinct " if query.distinct is True else "";
		fields = self.compileColumns(fields)
		return "select "+distinct+fields
	
	def compileColumns(self, fields):
		return self.concatenate(",", fields)

	def compileTables(self, query, tables):
		if not isinstance(tables, list) or len(tables)==0:
			return ""
		return "from "+self.concatenate(",", tables)

	
	def compileGroups(self, query, groups):
		return "group by "+self.concatenate(",", groups)

	"""
	def compileHavings(self, query):
		pass
	"""

	def compileOrders(self, query, orders):
		sql = []
		for order in orders:
			sql.append(order['sort']+" "+order['way'])
		return "order by "+self.concatenate(",", sql)

	def compileLimits(self, query, limit):
		return "limit "+str(limit['offset'])+","+str(limit['num'])

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

	def whereBasic(self, query, where):
		return where['field']+" "+where['operator']+" "+str(where['value'])

	def whereIn(self, query, where):
		_in = "not in" if where['not'] is True else "in"
		return where['field']+" "+_in+" ('"+self.concatenate("','", where['value'])+"')"  

	def whereBetween(self, query, where):
		_between =  "not between" if where['not'] is True else "between"
		return where['field']+" "+_between+" "+self.concatenate(" and ", where['value'])

	def whereNull(self, query, where):
		_null = "not null" if where['not'] is True else "null"
		return where['field']+" is "+_null

	def whereRaw(self, query, where):
		return where['sql']

	def concatenate(self, glue, pieces):
		return glue.join(str(i) for i in pieces)
