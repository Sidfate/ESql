
# 优雅的 Esql 1.0正式版

### 简介
python 操作 mysql 的模块有 MySQLdb，但是该模块其操作和返回都不够简介明了，因此封装了一个更为优雅的 mysql 操作类

### 调用方式
	from Builder import Builder as MySQL
	db = MySQL(config)

#### config - 数据库连接配置
- host   主机名
- user   用户名
- passwd 密码
- db     数据库名
- prefix 表前缀

### 优雅的链式操作
##### 查询操作
	db.table('user').select(['id', 'name']).where('id', '>', 2).whereNotNull('name').order('id', 'desc').limit(4).get()

其所生成的语句:
	<br><code>select id, name from user where id > 2 and name is not null order by id desc limit 4</code><br>
返回的结果集形式为元组，单条数据为字典形式

##### 插入操作
	data = {
		'name': 'sid',
		'age': 10
	}
	db.table('user').insert(data)

其所生成的语句:
	<br><code>insert into user (name, age) values ('sid', '10')</code><br>
返回结果为影响的行数

##### 更新操作
	data = {
		'name': 'sid',
		'age': 10
	}
	db.table('user').where('id', 2).update(data)

其所生成的语句:
	<br><code>update user set name='sid', age='10' where id = 2</code><br>
返回结果为影响的行数

##### 删除操作
	db.table('user').where('id', 2).delete()

其所生成的语句:
	<br><code>delete from user where id = 2</code><br>
返回结果为影响的行数	

### 文档
[Wiki](https://github.com/Sidfate/Py-MySQL/wiki)
