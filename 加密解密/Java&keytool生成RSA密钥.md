# Java&keytool生成RSA密钥

### 一.Keytool生成KeyStore文件

```sh
--  生成密码仓库test.store  
keytool -genkey -v -alias test -dname "CN=test,OU=HE,O=CUI,L=SHENGZHEN,ST=GUANGDONG,C=CN" -keyalg RSA -keysize 2048 -keypass 5201314 -keystore test.store -storepass 5201314 -validity 10000 -storetype JCEKS  
--  导出证书test.crt  
keytool -exportcert -alias test -file test.crt -keystore test.store -storepass 5201314 -rfc -storetype JCEKS  
```

**参数**：

- CN: 名字与姓氏    
- OU : 组织单位名称        
- O ：组织名称  
- L : 城市或区域名称  
- E : 电子邮件        
- ST: 州或省份名称  
- C: 单位的两字母国家代码