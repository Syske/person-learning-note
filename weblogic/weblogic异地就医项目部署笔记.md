### 部署步骤

#### 一、创建相应的文件夹
- 1、以下是项目资源存放路径的结构
```sh
med_ydjy_app.
        ├─app
        │  ├─config
        │  ├─hisapp
        │  ├─hx03app
        │  ├─hxapp
        │  ├─ksydjyapp
        │  └─lib
        ├─hisconfig1
        ├─hisconfig2
        ├─hx03config
        ├─hxconfig1
        ├─hxconfig2
        ├─ksydconfig1
        ├─ksydconfig2
        └─runqian

```
> **文件夹说明:**<br>
——app：项目根目录<br>
——config: 位于app目录下，存放项目发布配置资源文件，各个服务公有的配置，如dao-config.xml<br>
——*app: 位于app目录下，存放各个项目的发布资源，如war<br>
——lib:  位于app目录下，存放项目发布配置资源文件，各个服务公有的jar包<br>
——*config: 与app目录同级，存放各个服务特有的配置文件，如log4j的配置文件
——runqian: 位于app目录下，各个项目公用，存在润乾报表的验证密钥

- 2、 在linux目录/wls创建beafs文件夹，并在beafs文件夹下创建对应的资源文件夹，命令如下：
```
mkdir /wls/beanfs
```
#### 二、上传资源文件
- 对应文件夹上传对应的资源文件

#### 三、在domain上创建服务
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-publish-ydjy-01.png)

#### 四、创建启动脚本，修改StartManager脚本

- 1、进入项目domain根目录，创建服务启动脚本：
```sh
cd /wls/Oracle/Middleware/user_projects/domains/med_ydjy_domain/

touch startAdminServer.sh
```
- 脚本内容：
```sh
#!/bin/sh
nohup sh ./startWebLogic.sh > ./logs/adminserver.log  &
tail -f ./logs/adminserver.log

```
- adminserver默认启动的weblogic，所以后面没有指定服务，下面给大家看下我们自己服务的启动脚本
```sh
#!/bin/sh

DOMAIN_HOME="/wls/Oracle/Middleware/user_projects/domains/med_ydjy_domain"
nohup sh ${DOMAIN_HOME}/bin/startManagedWebLogic.sh ydjyapp1 > ./logs/ydjyapp1.log &
tail -f ./logs/ydjyapp1.log
```
- **说明：** 第一行设置的是domain的路径，第二行指定启动的服务是ydjyapp1，```> ./logs/ydjyapp1.log```表示将启动之后的控制台内容输入到logs/ydjyapp1.log文件中，所以稍后我们要在domain根目录下创建logs文件夹，并在logs文件夹下创建ydjyapp1.log文件，否则启动会报错，后面的```&```保证我们```Ctrl + C```之后，该进程继续在后台运行
- 2、修改startManagedWebLogic.sh脚本<br>
> 该脚本位于项目domain的bin文件夹下，如果你熟悉vi命令，建议直接在控制台编辑，如果不熟悉，可以通过sftp远程连接服务器，以视图形式编辑，下面是该脚本的内容：
```sh
#!/bin/sh

# WARNING: This file is created by the Configuration Wizard.
# Any changes to this script may be lost when adding extensions to this configuration.

# --- Start Functions ---

usage()
{
	echo "Need to set SERVER_NAME and ADMIN_URL environment variables or specify"
	echo "them in command line:"
	echo "Usage: $1 SERVER_NAME {ADMIN_URL}"
	echo "for example:"
	echo "$1 managedserver1 http://10.189.130.88:6201"
}

# --- End Functions ---

# *************************************************************************
# This script is used to start a managed WebLogic Server for the domain in
# the current working directory.  This script can either read in the SERVER_NAME and
# ADMIN_URL as positional parameters or will read them from environment variables that are 
# set before calling this script. If SERVER_NAME is not sent as a parameter or exists with a value
# as an environment variable the script will EXIT. If the ADMIN_URL value cannot be determined
# by reading a parameter or from the environment a default value will be used.
# 
#  For additional information, refer to "Managing Server Startup and Shutdown for Oracle WebLogic Server"
#  (http://download.oracle.com/docs/cd/E23943_01/web.1111/e13708/overview.htm)
# *************************************************************************

#  Set SERVER_NAME to the name of the server you wish to start up.

DOMAIN_NAME="med_ydjy_domain"

ADMIN_URL="http://10.189.131.35:6201"

#  Set WLS_USER equal to your system username and WLS_PW equal  

#  to your system password for no username and password prompt 

#  during server startup.  Both are required to bypass the startup

#  prompt.

WLS_USER=""
export WLS_USER

WLS_PW=""
export WLS_PW

#  Set JAVA_OPTIONS to the java flags you want to pass to the vm. i.e.: 

#  set JAVA_OPTIONS=-Dweblogic.attribute=value -Djava.attribute=value

JAVA_OPTIONS="-Dweblogic.security.SSL.trustedCAKeyStore="/wls/Oracle/Middleware/wlserver_10.3/server/lib/cacerts" ${JAVA_OPTIONS}"
export JAVA_OPTIONS

#  Set JAVA_VM to the java virtual machine you want to run.  For instance:

#  set JAVA_VM=-server

JAVA_VM=""

#  Set SERVER_NAME and ADMIN_URL, they must by specified before starting

#  a managed server, detailed information can be found at

# http://download.oracle.com/docs/cd/E23943_01/web.1111/e13708/overview.htm

if [ "$1" = "" ] ; then
	if [ "${SERVER_NAME}" = "" ] ; then
		usage $0
		exit
	fi
else
	SERVER_NAME="$1"
	shift
fi

if [ "$1" = "" ] ; then
	if [ "${ADMIN_URL}" = "" ] ; then
		usage $0
		exit
	fi
else
	ADMIN_URL="$1"
	shift
fi

# Export the admin_url whether the user specified it OR it was sent on the command-line

ADMIN_URL="${ADMIN_URL}"
export ADMIN_URL

SERVER_NAME="${SERVER_NAME}"
export SERVER_NAME

DOMAIN_HOME="/wls/Oracle/Middleware/user_projects/domains/med_ydjy_domain"

if [ "$1" = "" ] ; then
	#  Call Weblogic Server with our default params since the user did not specify any other ones
	${DOMAIN_HOME}/bin/startWebLogic.sh nodebug noderby noiterativedev notestconsole noLogErrorsToConsole
else
	#  Call Weblogic Server with the params the user sent in INSTEAD of the defaults
	${DOMAIN_HOME}/bin/startWebLogic.sh $1 $2 $3 $4 $5 $6 $7 $8 $9
fi

```
- **说明：** 这个脚本是在创建domain的时候自动生成的，一般不建议随意修改，我们需要在这里设定一些配置
    - config
    - lib<br>
在```DOMAIN_HOME="/wls/Oracle/Middleware/user_projects/domains/med_ydjy_domain"```这行代码下面，我们加入我们的配置：
上面的代码看着很多，但作用很简单，就是加载项目启动时的jar包，指定项目配置的路径，也就是项目的classpath，到这里我们离成功已经很近了
```sh
sxlss_ydjy_lib_path="/wls/beanfs/med_ydjy_app/app/lib"
PUBLIC_CONFIG="/wls/beanfs/med_ydjy_app/app/config"
RUNQIAN_PATH="/wls/beanfs/med_ydjy_app/runqian"
    RUNQIAN_LIB=${sxlss_ydjy_lib_path}/runqianlib4/barcode.jar:${sxlss_ydjy_lib_path}/runqianlib4/itext2_rq.jar:${sxlss_ydjy_lib_path}/runqianlib4/jai_codec.jar:${sxlss_ydjy_lib_path}/runqianlib4/jai_core.jar:${sxlss_ydjy_lib_path}/runqianlib4/jdom.jar:${sxlss_ydjy_lib_path}/runqianlib4/poi2.jar:${sxlss_ydjy_lib_path}/runqianlib4/report4.jar:${sxlss_ydjy_lib_path}/runqianlib4/webutil.jar:
    flex_lib_path="${sxlss_ydjy_lib_path}/flex"
    FLEX_LIB=${flex_lib_path}/cfgatewayadapter.jar:${flex_lib_path}/commons-codec-1.3.jar:${flex_lib_path}/commons-httpclient-3.0.1.jar:${flex_lib_path}/flex-messaging-common.jar:${flex_lib_path}/flex-messaging-core.jar:${flex_lib_path}/lib/flex/flex-messaging-opt.jar:${flex_lib_path}/flex-messaging-proxy.jar:${flex_lib_path}/flex-messaging-remoting.jar:${flex_lib_path}/flex-rds-server.jar:${flex_lib_path}/xalan.jar:

    FLEX_LIB="${flex_lib_path}/cfgatewayadapter.jar:${flex_lib_path}/commons-codec-1.3.jar:${flex_lib_path}/commons-httpclient-3.0.1.jar:${flex_lib_path}/commons-logging.jar:${flex_lib_path}/flex-messaging-common.jar:${flex_lib_path}/flex-messaging-core.jar:${flex_lib_path}/flex-messaging-opt.jar:${flex_lib_path}/flex-messaging-proxy.jar:${flex_lib_path}/flex-messaging-remoting.jar:${flex_lib_path}/flex-rds-server.jar:${flex_lib_path}/xalan.jar"
    APP_LIB_hx="${sxlss_ydjy_lib_path}/commons-pool2-2.4.2.jar:${sxlss_ydjy_lib_path}/HRSSApi.jar:${sxlss_ydjy_lib_path}/otp-report-1.0.0.jar:${sxlss_ydjy_lib_path}/sxlss-ydjy-vo-1.0.0.jar:${sxlss_ydjy_lib_path}/YDJYINT02_Proxy-1.0.0.jar:${sxlss_ydjy_lib_path}/antlr-2.7.6.jar:${sxlss_ydjy_lib_path}/classes12.jar:${sxlss_ydjy_lib_path}/commons-beanutils-1.8.2.jar:${sxlss_ydjy_lib_path}/commons-cli-1.0.jar:${sxlss_ydjy_lib_path}/commons-collections.jar:${sxlss_ydjy_lib_path}/commons-dbcp-1.2.2.jar:${sxlss_ydjy_lib_path}/commons-digester-1.8.1.jar:${sxlss_ydjy_lib_path}/commons-el-1.0.jar:${sxlss_ydjy_lib_path}/commons-el-ext-1.0.jar:${sxlss_ydjy_lib_path}/commons-fileupload.jar:${sxlss_ydjy_lib_path}/commons-lang-2.4.jar:${sxlss_ydjy_lib_path}/commons-logging-1.1.1.jar:${sxlss_ydjy_lib_path}/commons-pool-1.3.jar:${sxlss_ydjy_lib_path}/commons-validator.jar:${sxlss_ydjy_lib_path}/connector-1_5.jar:${sxlss_ydjy_lib_path}/ecs-1.4.2.jar:${sxlss_ydjy_lib_path}/ejb.jar:${sxlss_ydjy_lib_path}/hessian-3.0.20.jar:${sxlss_ydjy_lib_path}/hsqldb-1.7.3.jar:${sxlss_ydjy_lib_path}/iText.jar:${sxlss_ydjy_lib_path}/iTextAsian.jar:${sxlss_ydjy_lib_path}/jakarta-oro-2.0.8.jar:${sxlss_ydjy_lib_path}/jakarta-regexp-1.4.jar:${sxlss_ydjy_lib_path}/javadbf.jar:${sxlss_ydjy_lib_path}/jms.jar:${sxlss_ydjy_lib_path}/jmx.jar:${sxlss_ydjy_lib_path}/jotm.jar:${sxlss_ydjy_lib_path}/jsp-api.jar:${sxlss_ydjy_lib_path}/jstl.jar:${sxlss_ydjy_lib_path}/jta.jar:${sxlss_ydjy_lib_path}/jxl.jar:${sxlss_ydjy_lib_path}/log4j-1.2.15.jar:${sxlss_ydjy_lib_path}/log4j-api-2.11.1.jar:${sxlss_ydjy_lib_path}/log4j-core-2.11.1.jar:${sxlss_ydjy_lib_path}/mail.jar:${sxlss_ydjy_lib_path}/otp-application-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-console-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-core-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-dao-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-dictionary-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-isb-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-log-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-navigator-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-notification-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-parameter-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-qryrpt-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-security-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-sso-1.0.0.jar:${sxlss_ydjy_lib_path}/otp-table-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-txc-2.0.0.jar:${sxlss_ydjy_lib_path}/otp-webgui-2.0.0.jar:${sxlss_ydjy_lib_path}/parser.jar:${sxlss_ydjy_lib_path}/PDFBox-0.6.2.jar:${sxlss_ydjy_lib_path}/poi-2.5.1.jar:${sxlss_ydjy_lib_path}/quartz-1.5.2.jar:${sxlss_ydjy_lib_path}/quartz-oracle-1.5.2.jar:${sxlss_ydjy_lib_path}/quartz-weblogic-1.5.2.jar:${sxlss_ydjy_lib_path}/runqianlib4:${sxlss_ydjy_lib_path}/servlet-api.jar:${sxlss_ydjy_lib_path}/spring-1.2.8.jar:${sxlss_ydjy_lib_path}/sslext-struts-1.2.jar:${sxlss_ydjy_lib_path}/standard.jar:${sxlss_ydjy_lib_path}/struts.jar:${sxlss_ydjy_lib_path}/xapool.jar:${sxlss_ydjy_lib_path}/xml-apis.jar:${sxlss_ydjy_lib_path}/ydjylss.jar:${sxlss_ydjy_lib_path}/dom4j-1.6.1.jar:${sxlss_ydjy_lib_path}/KSYDJYINT.jar:${sxlss_ydjy_lib_path}/YDJYINT02_Proxy.jar:${sxlss_ydjy_lib_path}/KSYDJYINT02-1.0.0.jar:${sxlss_ydjy_lib_path}/ezmorph-1.0.6.jar:${sxlss_ydjy_lib_path}/json-lib-2.2.3-jdk15.jar:${sxlss_ydjy_lib_path}/xstream-1.3.1.jar:${sxlss_ydjy_lib_path}/jsch-0.1.51.jar:${sxlss_ydjy_lib_path}/HRSSApi.jar:${sxlss_ydjy_lib_path}/commons-pool2-2.4.2.jar:${sxlss_ydjy_lib_path}/xssProtect-0.1.jar:${sxlss_ydjy_lib_path}/fastjson-1.2.9.jar:${sxlss_ydjy_lib_path}/PlaceOtherService.jar:${sxlss_ydjy_lib_path}/bcprov-jdk16-1.46.jar:${sxlss_ydjy_lib_path}/axis-1.4.jar:${sxlss_ydjy_lib_path}/commons-logging-1.0.4.jar:${sxlss_ydjy_lib_path}/commons-discovery-0.2.jar"
if [ "$SERVER_NAME" = "ydjyapp1" ] ; then
    APP_CONFIG="/wls/beanfs/med_ydjy_app/hxconfig1"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/hxapp"
    APP_LIB=${APP_LIB_hx}:${FLEX_LIB}:
   
fi

if [ "$SERVER_NAME" = "ydjyapp2" ] ; then
    APP_CONFIG="/wls/beanfs/med_ydjy_app/hxconfig2"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/hxapp"
    APP_LIB=${APP_LIB_hx}:${FLEX_LIB}:

fi


if [ "$SERVER_NAME" = "ydjyreckonerapp1" ] ; then   
    APP_CONFIG="/wls/beanfs/med_ydjy_app/hisconfig1"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/hisapp"

 fi

if [ "$SERVER_NAME" = "ydjyreckonerapp2" ] ; then
    APP_CONFIG="/wls/beanfs/med_ydjy_app/hisconfig2"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/hisapp"

 fi

if [ "$SERVER_NAME" = "ksydjyapp1" ] ; then
    APP_CONFIG="/wls/beanfs/med_ydjy_app/ksydconfig1"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/ksydjyapp"

 fi
  
if [ "$SERVER_NAME" = "ksydjyapp2" ] ; then
    APP_CONFIG="/wls/beanfs/med_ydjy_app/ksydconfig2"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/ksydjyapp"

 fi

if [ "$SERVER_NAME" = "hx03app" ] ; then

    APP_CONFIG="/wls/beanfs/med_ydjy_app/hx03config"
    APP_HOME="/wls/beanfs/med_ydjy_app/app/hx03app"

 fi

CLASSPATH="${RUNQIAN_PATH}:${APP_CONFIG}:${APP_LIB}:${PUBLIC_CONFIG}"
export CLASSPATH
```
- 上面的代码看着很多，但作用很简单，就是加载项目启动时的jar包，指定项目配置的路径，也就是项目的classpath，到这里我们离成功已经很近了

#### 五、部署项目
- 1、启动adminServier，也就是我们的weblogic，直接执行启动脚本即可，如果报错，请先检查自己本地是否有boot.properties文件，如果没有请参考第六步进行配置
- 2、进入domain控制台，输入我们创建domain的用户名及密码，选择我们的应用，指定服务发布目标，激活更改，选中项目，点击启动，然后进入ssh控制台

#### 六、创建boot.properties文件，启动服务
先执行你的启动脚本，第一次会报错，这没关系，因为你本地少了配置文件
- 1、创建security/文件夹，并在文件夹下创建boot.properties文件
```sh
// 先要进入你的服务文件夹下，位于domain的servers文件下
cd ./servers/ydjyapp1
mkdir security/
touch boot.properties
```
- 2、在boot.properties文件中配置你的domain的用户名和密码
```sh
vi boot.properties
// 在boot文件中添加如下配置
username=weblogic
password=weblogic
```
- 文件中的配置文件修改成你domain的用户名和密码，第一次启动后后自动加密，加密后不能修改，除非你修改了密码，否则修改后服务就没法启动了，然后再次执行启动脚本，服务应该可以正常启动了
- 至此，服务配置完成，访问下你的服务，看是否已经成功