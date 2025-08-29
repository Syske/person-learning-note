tags: #db #hikari

- 在配置application.yml时，对hikari的配置会有这样一个字段validationQuery。
- validationQuery是用来验证数据库连接的查询语句，这个查询语句必须是至少返回一条数据的SELECT语句。每种数据库都有各自的验证语句。





DataBase   |  validationQuery
--|--
hsqldb   |  select 1 from INFORMATION_SCHEMA.SYSTEM_USERS
Oracle   |  select 1 from dual
DB2   |  select 1 from sysibm.sysdummy1
MySql   |  select 1
Microsoft SqlServer   |  select1
postgresql  |   select version()
ingres  |   select 1
derby   |  values 1
H2   |gi  select 1