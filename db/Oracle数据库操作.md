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