tags: #db #oracle

### 1、创建自增主键

- 创建序列
```
--创建序列
create sequence seq_tb_batch_file

minvalue 1

nomaxvalue

start with 1

increment by 1

nocycle   --一直累加，不循环

--nocache;  --不缓存

cache 10 --缓存10条
```
- 创建触发器

```
--创建触发器，如果insert语句没有传ID自动递增
CREATE OR REPLACE TRIGGER tr_tb_payment_batch_files 

BEFORE INSERT ON payment_batch_files FOR EACH ROW WHEN (new.id is null)

begin

select seq_tb_batch_file.nextval into :new.id from dual;

end;
```

### 2、查看数据库版本信息

```sql
select * from v$version;
--或
select banner from sys.v_$version;
```

 结果如下：
    BANNER
 1 Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Prod
 2 PL/SQL Release 10.2.0.1.0 - Production
 3 CORE 10.2.0.1.0 Production
 4 TNS for 32-bit Windows: Version 10.2.0.1.0 - Production
 5 NLSRTL Version 10.2.0.1.0 - Production

- 例如：Oracle 9.0.1.1.2 
   　　
   　　9：版本号 
      　　0：新特性版本号 
      　　1（第一个）：维护版本号 
      　　1（第二个）：普通的补丁设置号码 
      　　2：非凡的平台补丁设置号码

### 3、命令行操作

- 登陆

  ```sh
  $ sqlplus
  $ SQL>sys as sysdba
  ```

- 查看所有表空间

  ```sql
  select * from Dba_Tablespaces;
  ```

- 删除表空间

  ```sql
  drop tablespace TBS_SXSSC_AZ14 including contents and datafiles cascade constraints;
  ```

  其中，`TBS_SXSSC_AZ14`是要删除的表空间名称

### 4、查看oracle会话

```sql
select session_id from v$locked_object;

SELECT sid, serial#, username, osuser FROM v$session where sid IN (select session_id from v$locked_object);

--将上面锁定的会话关闭：
ALTER SYSTEM KILL SESSION '2092,10026';

ALTER SYSTEM KILL SESSION '201,34383';
ALTER SYSTEM KILL SESSION '2099,58703';
```

