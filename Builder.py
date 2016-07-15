from Grammar import Grammar
from Connection import Connection

"""
@class: Builder 
@version: 1.0
@author: sidfate
@desc: builder query and execute
"""
class Builder:
	wheres = []
	orders = []
	tables = []
	fields = []
	groups = []
	havings = []
	limits  = {}
	distinct = False

	def __init__(self, config):
		self.connection = Connection(config)
		self.grammar = Grammar()

	"""
	Select the table.
	@param  string table
	@return self 
	"""
	def table(self, table):
		if self.connection.config.has_key('prefix'):
			table = self.connection.config['prefix']+table
		if not table in self.tables:
			self.tables.append(table)
		return self

	"""
	Add an "order by".
	@param  dict|string sort
	@param  string      way
	@return self
	"""
	def order(self, sort, way="asc"):
		if isinstance(sort, dict):
			for k, v in sort.items():
				self.orders.append({'sort': k, 'way': v})
		else:
			self.orders.append({'sort': sort, 'way': way.lower()})
		return self

	"""
	Select the fields.
	@param  tuple args
	@return self
	"""
	def select(self, *args):
		args = list(args)
		if len(args) == 0:
			self.fields = ["*"]
		else:
			for item in args:  
	   			self.fields += item if isinstance(item, list) else [item]

   		self.fields = list(set(self.fields))
		return self

	"""
	Add a "distinct".
	@return self
	"""
	def distinct(self):
		self.distinct = True
		return self

	"""
	Limit the number of results.
	@param  int  offset 
	@param  int  num
	@return self
	"""
	def limit(self, offset, num=0):
		self.limits = {'num': offset, 'offset': 0} if num==0 else {'offset': offset, 'num': num}
		return self

	"""
	Add a basic "where".
	@param  string field
	@param  string operator
	@param  string value
	@param  string boolean
	@return self
	"""
	def where(self, field, operator=None, value=None, boolean='and'):
		if not value:
			value = operator
			operator = '='
			
		whereType = 'basic'
		self.wheres.append({'field': field, 'value': value, 'operator': operator, 'boolean': boolean, 'type': whereType})
		return self

	"""
	Add a "or where".
	@param  string field
	@param  string operator
	@param  string value
	@return self
	"""
	def orWhere(self, field, operator=None, value=None):
		return self.where(field, operator, value, 'or')

	"""
	Add a where between.
	@param  string  field
	@param  string  value
	@param  string  boolean
	@param  boolean isNot
	@return self
	"""
	def whereBetween(self, field, value, boolean='and', isNot=False):
		if not isinstance(value, list):
			value = list(value)
		whereType = 'between'
		self.wheres.append({'field': field, 'value': value, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	"""
	Add a or where between.
	@param  string  field
	@param  string  value
	@return self
	"""
	def orwhereBetween(self, field, value):
		return self.whereBetween(field, value, 'or')

	"""
	Add a where not between.
	@param  string  field
	@param  string  value
	@return self
	"""
	def whereNotBetween(self, field, value):
		return self.whereBetween(field, value, 'and', True)

	"""
	Add a or where not between.
	@param  string  field
	@param  string  value
	@return self
	"""
	def orWhereNotBetween(self, field, value):
		return self.whereBetween(field, value, 'or', True)

	"""
	Add a where in.
	@param  string  field
	@param  string  value
	@param  string  boolean
	@param  boolean isNot
	@return self
	"""
	def whereIn(self, field, value, boolean='and', isNot=False):
		if not isinstance(value, list):
			value = list(value)
		whereType = 'in'
		self.wheres.append({'field': field, 'value': value, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	"""
	Add a or where in.
	@param  string  field
	@param  string  value
	@return self
	"""
	def orWhereIn(self, field, value):
		return self.whereIn(field, value, 'or')

	"""
	Add a where not in.
	@param  string  field
	@param  string  value
	@return self
	"""
	def whereNotIn(self, field, value):
		return self.whereIn(field, value, 'and', True)

	"""
	Add a or where not in.
	@param  string  field
	@param  string  value
	@return self
	"""
	def orWhereNotIn(self, field, value):
		return self.whereIn(field, value, 'or', True)

	"""
	Add a where is null.
	@param  string  field
	@param  string  boolean
	@param  boolean isNot
	@return self
	"""
	def whereNull(self, field, boolean='and', isNot=False):
		whereType = 'null'
		self.wheres.append({'field': field, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	"""
	Add a or where is null.
	@param  string  field
	@return self
	"""
	def orWhereNull(self, field):
		return self.whereNull(field, 'or')

	"""
	Add a where is not null.
	@param  string  field
	@return self
	"""
	def whereNotNull(self, field):
		return self.whereNull(field, 'and', True)

	"""
	Add a or where is not null.
	@param  string  field
	@return self
	"""
	def orWhereNotNull(self, field):
		return self.whereNull(field, 'or', True)
	
	"""
	Add a raw where.
	@param  string  sql
	#param  string  boolean
	@return self
	"""
	def whereRaw(self, sql, boolean='and'):
		whereType = 'raw'
		self.wheres.append({'sql': sql, 'boolean': boolean, 'type': whereType})
		return self

	"""
	Add a or raw where.
	@param  string  sql
	@return self
	"""
	def orWhereRaw(self, sql):
		return self.whereRaw(sql, 'or')

	"""
	Add a group by.
	@param  tuple args
	@return self
	"""
	def groupBy(self, *args):
		args = list(args)
		for item in args:  
   			self.groups += item if isinstance(item, list) else [item]

   		self.groups = list(set(self.groups))
   		return self

   	"""
   	Add a having.
   	@param  string field 
   	@param  string operator
   	@param  string value
   	@param  string boolean
   	@return self
   	"""
   	def having(self, field, operator=None, value=None, boolean='and'):
   		whereType = 'basic'
		self.havings.append({'field': field, 'value': value, 'operator': operator, 'boolean': boolean, 'type': whereType})
		return self
   	"""
   	Add a or having.
   	@param  string field 
   	@param  string operator
   	@param  string value
   	@return self
   	"""
	def orHaving(self, field, operator=None, value=None):
		return self.having(field, operator, value, 'or')

	"""
	Add a raw having.
   	@param  string sql 
   	@param  string boolean
   	@return self
	"""
	def havingRaw(self, sql, boolean='and'):
		whereType = 'raw'
		self.havings.append({'sql': sql, 'boolean': boolean, 'type': whereType})
		return self

	"""
	Add a raw or having.
   	@param  string sql 
   	@return self
	"""
	def orHavingRaw(self, sql):
		return self.havingRaw(sql, 'or')

	"""
	def join(self):
		return self.whereNull(field, 'or')

	def leftJoin(self):
		pass
	"""

	"""
	get all of results
	@return tuple
	"""
	def get(self):
		results = self.connection.select(self.__toSql())
		self.__optEnd()
		return results

	"""
	get the first column of results
	@return dict
	"""
 	def first(self):
		results = self.connection.select(self.__toSql())
		self.__optEnd()
		return results[0] if len(results) != 0 else results

	"""
	get the field from the first column of results
	@param  string field
	@return mixed
	"""
	def pluck(self, field):
		self.fields = [field]
		results = self.connection.select(self.__toSql())
		self.__optEnd()
		return results[0][field] if len(results) != 0 else None

	"""
	get list of the field from results
	"""
	def lists(self, field):
		self.fields = [field]
		results = self.connection.select(self.__toSql())
		self.__optEnd()
		if len(results) == 0:
			return None
		else:
			lists = []
			for item in results:
				lists.append(item[field])
			return lists 
	
	"""
	Return the sum of results of a given field.
	@return numeric
	"""
	def count(self):
		return self.aggregate(self.count.__name__, '*')

	"""
	Return the max of results of a given field.
	@param  string field
	@return numeric
	"""
	def max(self, field):
		return self.aggregate(self.max.__name__, field)

	"""
	Return the min of results of a given field.
	@param  string field
	@return numeric
	"""
	def min(self, field):
		return self.aggregate(self.min.__name__, field)

	"""
	Return the avg of results of a given field.
	@param  string field
	@return numeric
	"""
	def avg(self, field):
		return self.aggregate(self.avg.__name__, field)

	"""
	Return the sum of results of a given field.
	@param  string field
	@return numeric
	"""
	def sum(self, field):
		return self.aggregate(self.sum.__name__, field)

	"""
	Deal aggregate query.
	@param  string func
	@param  string field
	@return numeric
	"""
	def aggregate(self, func, field):
		self.fields = [func+"("+field+") as "+func]
		results = self.connection.select(self.__toSql())
		self.__optEnd()
		return results[0][func] if len(results) != 0 else 0

	"""
	Insert a recode.
	@return boolean
	"""
	def insert(self, values):
		sql = self.grammar.compileInsert(self, values)
		self.__optEnd()
		return self.connection.insert(sql)

	"""
	Get the insert id
	@return int
	"""
	def getInsertId(self):
		return self.connection.getInsertId()

	"""
	Update a record.
	@param  dict    values
	@return boolean
	"""
	def update(self, values):
		sql = self.grammar.compileUpdate(self, values)
		self.__optEnd()
		return self.connection.update(sql)

	"""
	Delete a record.
	@return boolean
	"""
	def delete(self):
		sql = self.grammar.compileDelete(self)
		self.__optEnd()
		return self.connection.delete(sql)

	"""
	Create the select sql 
	@return string
	"""
	def __toSql(self):
		return self.grammar.compileSelect(self)

	"""
	clean up record
	"""
	def __optEnd(self):
		self.wheres = []
		self.orders = []
		self.tables = []
		self.fields = []
		self.groups = []
		self.havings = []
		self.limits  = {}
		self.distinct = False

