
#### 表操作

#### 重命名

```sql
 rename table login_account_user_mapping to login_account_user_mapping_240823
```


### 写入操作

#### 忽略错误

```sql
insert ignore into login_account_user_mapping_111 (id, account_id, user_id , enterprise_id, is_admin, is_delete , gmt_created , gmt_modified) select id, account_id, user_id , enterprise_id, is_admin, is_delete , gmt_created , gmt_modified from login_account_user_mapping where is_delete = 2
```