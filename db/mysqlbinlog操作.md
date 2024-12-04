
### 将binlog解析为sql文件

```sh
 .\mysqlbinlog --start-datetime="2024-04-24 09:45:00" --stop-datetime="2024-04-24 09:50:00" -v --base64-output=decode-rows --skip-gtids=true mysql-bin.000899 > binlog_output.sql  
```

说明：
- `start-datetime`: 开始时间
- `stop-datetime`：结束时间