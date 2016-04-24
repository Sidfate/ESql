
------------------[version 1.0]------------------

mysql 类 1.0版
[点链式调用方式]


[1].select: 字段选择
参数:
	(1)list
		db.select(['id', 'name'])
	(2)不定参数
		db.select('id', 'name')
	
复杂形式
	db.select('(select name from user where id=1) as username')
ps:复杂形势下将不保护字段与表名


[2].order: 排序
参数:
	(1)单个字段排序
		db.order('time', 'desc')
	(2)多字段排序(dict形式)
		db.order({'time':'desc', 'name':'asc'})

[3].table: 表名选择
参数:
	(1)
		db.table('user')


[4].limit: 返回数量限制
参数:
	(1)单个参数
		db.limit(2)
	(2)多个参数
		db.limit(1, 2)

[5].distinct: 去重
参数:
	(1)
		db.distinct()

查询条件
[6].where: 查询条件
参数:
	(1)
		db.where('id', 1)
	(2)
		db.where('id', '>', 1)
	(3)
		db.where('man', 1).where('id', '>', 1, 'or') 不推荐，推荐使用下面的orWhere替代

[7].orWhere: 查询条件 or 连接
参数:
	(1)
		db.where('man', 1).orWhere('id', '>', 1)

[8].whereBetween: between 条件
参数:
	(1)
		db.whereBetween('id', [1, 100])

[9].whereIn: in 条件
参数:
	(1)
		db.whereIn('id', [1, 2, 3])

[10].whereNull: is null 条件
参数:
	(1)
		db.whereNull('name')

分组与选择
[11].groupBy & having: 分组
参数:
	(1)支持多个参数，参数可以为list
		db.gourpBy('a', 'b', 'c')
		db.groupBy(['a', 'b', 'c'])
		db.groupBy('count').having('count', '>', 100)


结果返回形式
[12].get: 获取所有结果集

[13].first: 获取结果集的第一条数据

[14].pluck: 获取结果集第一条数据的指定字段
	db.where('id', 3).pluk('name')

[15].lists: 获取结果集中指定字段的list
	db.whereBetween('id', [1, 100]).lists('name')

聚合方法
[16].count
	db.table('user').count()
[18].min
	db.table('user').min('age')
[19].max
	db.table('user').max('age')
[20].avg
	db.table('user').avg('age')
[17].sum
	db.table('user').sum('age')