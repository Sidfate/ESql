
------------------[version 1.0]------------------

#优雅的 mysql 1.0版

##SELECTS
###table: 表名选择
	db.table('user')

###get: 获取所有结果集
	db.table('user').get()

###first: 获取结果集的第一条数据
	db.table('user').first()

###pluck: 获取结果集第一条数据的指定字段
	db.table('user').pluck('name')

###lists: 获取结果集中指定字段的list
	db.table('user').lists('name')

###select: 字段选择
    db.table('user').select(['id', 'name']).get()
	db.table('user').select('id', 'name').get()
	
**复杂形式:**

	db.table('user').select('(select name from user where id=1) as username').get()
**注意:复杂形势下将不保护字段与表名**

###order: 排序
	db.table('user').order('time', 'desc').get()
	db.table('user').order({'time':'desc', 'name':'asc'}).get()

###limit: 返回数量限制
	db.table('user').limit(2).get()
	db.table('user').limit(1, 2).get()
		
###distinct: 去重
	db.table('user').distinct().get()
		
##查询条件
###where: 查询条件
	db.where('id', 1)
	db.where('id', '>', 1)

###orWhere: 查询条件 or 连接
	db.where('man', 1).orWhere('id', '>', 1)
	
###whereBetween: between 条件
	db.whereBetween('id', [1, 100])

###whereNotBetween: not between 条件
	db.whereNotBetween('id', [1, 100])

###whereIn: in 条件
	db.whereIn('id', [1, 2, 3])
		
###whereNull: is null 条件
	db.whereNull('name')
		
###groupBy & having: 分组
	db.table('user').gourpBy('a', 'b', 'c')
	db.table('user').groupBy(['a', 'b', 'c'])
	db.table('user').groupBy('count').having('count', '>', 100)

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