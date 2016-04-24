
------------------[version 1.0]------------------

#优雅的 mysql 1.0版

###简介
python 操作mysql的模块有MySQLdb，但是该模块其操作和返回都不够简介明了，因此封装了一个更为优雅的mysql操作类

###调用方式
	from Builder import Builder as MySQL
	db = MySQL(config)

####config - 数据库连接配置
- host   主机名
- user   用户名
- passwd 密码
- db     数据库名
- prefix 表前缀

###优雅的查询操作
	db.table('user').select(['id', 'name']).where('id', '>', 2).whereNotNull('name').order('id', 'desc').limit(4).get()

其所生成的语句:
	<br><code>select id, name from user where id > 2 and name is not null order by id desc limit 4</code><br>
数据集的返回形式为元组，单条数据为字典形式