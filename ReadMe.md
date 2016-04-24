
------------------[version 1.0]------------------

#优雅的 mysql 1.0版


###select: 字段选择
+ 参数:
	- (1)list
	<br><code>db.select(['id', 'name'])</code>
	- (2)不定参数
	<br><code>db.select('id', 'name')</code>
	
+ 复杂形式:
	db.select('(select name from user where id=1) as username')
ps:复杂形势下将不保护字段与表名


###order: 排序
+ 参数:
	- (1)单个字段排序
	<br><code>db.order('time', 'desc')</code>
	- (2)多字段排序(dict形式)
	<br><code>db.order({'time':'desc', 'name':'asc'})</code>
		
###table: 表名选择
+ 参数:
	- (1)
	<br><code>db.table('user')</code>

###limit: 返回数量限制
+ 参数:
	- (1)单个参数
	<br><code>db.limit(2)</code>
	- (2)多个参数
	<br><code>db.limit(1, 2)</code>
		
###distinct: 去重
+ 参数:
	- (1)
	<br><code>db.distinct()</code>
		
##查询条件
###where: 查询条件
+ 参数:
	- (1)
	<br><code>db.where('id', 1)</code>
	- (2)
	<br><code>db.where('id', '>', 1)</code>

###orWhere: 查询条件 or 连接
+ 参数:
	- (1)
	<br><code>db.where('man', 1).orWhere('id', '>', 1)</code>
	
###whereBetween: between 条件
+ 参数:
	- (1)
	<br><code>db.whereBetween('id', [1, 100])</code>	

###whereIn: in 条件
+ 参数:
	- (1)
	<br><code>db.whereIn('id', [1, 2, 3])</code>
		
###whereNull: is null 条件
+ 参数:
	- (1)
	<br><code>db.whereNull('name')</code>
		
##分组与选择
###groupBy & having: 分组
+ 参数:
	- (1)支持多个参数，参数可以为list
	<br><code>db.table('user')
		db.gourpBy('a', 'b', 'c')
		db.groupBy(['a', 'b', 'c'])
		db.groupBy('count').having('count', '>', 100)
	</code>


##结果返回形式
###get: 获取所有结果集

###first: 获取结果集的第一条数据

###pluck: 获取结果集第一条数据的指定字段
	db.where('id', 3).pluk('name')

###lists: 获取结果集中指定字段的list
	db.whereBetween('id', [1, 100]).lists('name')

##聚合方法
###count
	db.table('user').count()
###min
	db.table('user').min('age')
###max
	db.table('user').max('age')
###avg
	db.table('user').avg('age')
###sum
	db.table('user').sum('age')