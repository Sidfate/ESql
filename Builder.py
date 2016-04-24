import MySQLdb
import MySQLdb.cursors
from Grammar import Grammar

"""
@class: Builder 
@version: 1.0
@author: sidfate
@desc: MySQL builder class
"""
class Builder:
	config = {}
	__conn = None
	__cur = None
	wheres = []
	orders = []
	tables = []
	fields = []
	groups = []
	havings = []
	limits  = {}
	distinct = False

	def __init__(self, config):
		self.config = config
		self.__conn = MySQLdb.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'], charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
		self.__cur = self.__conn.cursor()
		self.grammar = Grammar()
	
	def __del__(self):
		self.__cur.close()
		self.__conn.commit()
		self.__conn.close()

	def table(self, table):
		self.tables.append(table)
		return self

	def order(self, sort, way="asc"):
		if isinstance(sort, dict):
			for k, v in sort.items():
				self.orders.append({'sort': k, 'way': v})
		else:
			self.orders.append({'sort': sort, 'way': way.lower()})
		return self

	def select(self, fields=['*'], *args):
		if isinstance(fields, list):
			self.fields = fields
		else:
			fList = list(args)
			fList.append(fields)
			self.fields = fList
		return self

	def distinct(self):
		self.distinct = True
		return self

	def limit(self, offset, num=0):
		self.limits = {'num': offset, 'offset': 0} if num==0 else {'offset': offset, 'num': num}
		return self

	def where(self, field, operator=None, value=None, boolean='and'):
		if not value:
			value = operator
			operator = '='
			
		whereType = 'basic'
		self.wheres.append({'field': field, 'value': value, 'operator': operator, 'boolean': boolean, 'type': whereType})
		return self

	def orWhere(self, field, operator=None, value=None):
		return self.where(field, operator, value, 'or')

	def whereBetween(self, field, value, boolean='and', isNot=False):
		if not isinstance(value, list):
			value = list(value)
		whereType = 'between'
		self.wheres.append({'field': field, 'value': value, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	def orwhereBetween(self, field, value):
		return self.whereBetween(field, value, 'or')

	def whereNotBetween(self, field, value):
		return self.whereBetween(field, value, 'and', True)

	def orWhereNotBetween(self, field, value):
		return self.whereBetween(field, value, 'or', True)

	def whereIn(self, field, value, boolean='and', isNot=False):
		if not isinstance(value, list):
			value = list(value)
		whereType = 'in'
		self.wheres.append({'field': field, 'value': value, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	def orWhereIn(self, field, value):
		return self.whereIn(field, value, 'or')

	def whereNotIn(self, field, value):
		return self.whereIn(field, value, 'and', True)

	def orWhereNotIn(self, field, value):
		return self.whereIn(field, value, 'or', True)

	def whereNull(self, field, boolean='and', isNot=False):
		whereType = 'null'
		self.wheres.append({'field': field, 'boolean': boolean, 'not': isNot, 'type': whereType})
		return self

	def orWhereNull(self, field):
		return self.whereNull(field, 'or')

	def whereNotNull(self, field):
		return self.whereNull(field, 'and', True)

	def orWhereNotNull(self, field):
		return self.whereNull(field, 'or', True)
	
	def whereRaw(self, where, boolean='and'):
		whereType = 'raw'
		self.wheres.append({'sql': where, 'boolean': boolean, 'type': whereType})
		return self

	def orWhereRaw(self, where):
		return self.whereRaw(where, 'or')

	def groupBy(self, *args):
		args = list(args)
		for item in args:  
   			self.groups += item if isinstance(item, list) else [item]

   		self.groups = list(set(self.groups))
   		return self

   	def having(self, field, operator=None, value=None, boolean='and'):
   		whereType = 'basic'
		self.havings.append({'field': field, 'value': value, 'operator': operator, 'boolean': boolean, 'type': whereType})
		return self

	def orHaving(self, field, operator=None, value=None):
		return self.having(field, operator, value, 'or')


	"""
	def join(self):
		return self.whereNull(field, 'or')

	def leftJoin(self):
		pass
	"""

	# get all of results
	def get(self):
		return self.__executeSelect()

	# get the first column of results
 	def first(self):
		results = self.__executeSelect()
		return results[0] if len(results) != 0 else results

	# get the field from the first column of results
	def pluck(self, field):
		self.fields = [field]
		results = self.__executeSelect()
		return results[0][field] if len(results) != 0 else None

	# get list of the field from results
	def lists(self, field):
		pass	

	def count(self):
		return self.aggregate(self.count.__name__, '*')

	def max(self, field):
		return self.aggregate(self.max.__name__, field)

	def min(self, field):
		return self.aggregate(self.min.__name__, field)

	def avg(self, field):
		return self.aggregate(self.avg.__name__, field)

	def sum(self, field):
		return self.aggregate(self.sum.__name__, field)

	def aggregate(self, func, field):
		self.fields = [func+"("+field+") as "+func]
		results = self.__executeSelect()
		return results[0][func] if len(results) != 0 else 0

	# mysql cursor executes sql and returns results
	def __executeSelect(self):
		sql = self.__toSql()
		res = self.__cur.execute(sql)      
		return self.__cur.fetchall() 

	def __toSql(self):
		return self.grammar.compileSelect(self)


