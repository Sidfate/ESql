import MySQLdb
import MySQLdb.cursors

"""
@class: Connection 
@version: 1.0
@author: sidfate
@desc: connection MYSQL server and handle operation
"""
class Connection: 
	config = {}
	__conn = None
	__cur = None

	"""
	Connection to MYSQL server.
	@param  dict config
	"""
	def __init__(self, config):
		self.config = config
		self.__conn = MySQLdb.connect(host=config['host'], user=config['user'], passwd=config['passwd'], db=config['db'], charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
		self.__cur = self.__conn.cursor()

	"""
	Disconnection to MYSQL server.
	"""	
	def __del__(self):
		self.__cur.close()
		self.__conn.commit()
		self.__conn.close()

	"""
	Handle select operation.
	@param  string sql
	@return tuple  
	"""	
	def select(self, sql):
		res = self.__cur.execute(sql)      
		return self.__cur.fetchall() 

	"""
	Handle insert operation.
	@param  string sql
	@return int  
	"""	
	def insert(self, sql):
		return self.__cur.execute(sql)

	"""
	Handle update operation.
	@param  string sql
	@return int  
	"""	
	def update(self, sql):
		return self.__cur.execute(sql)

	"""
	Handle delete operation.
	@param  string sql
	@return int  
	"""	
	def delete(self, sql):
		return self.__cur.execute(sql)