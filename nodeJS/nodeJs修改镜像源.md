### 查看安装结果与版本

```sh
node -v #查看安装版本
npm -v #查看npm安装版本
```

### 修改镜像源

```sh
// 设置 淘宝镜像源
npm config set registry https://registry.npm.taobao.org
// 查看 使用的 镜像源
npm config get registry
// 安装 淘宝镜像源
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

###  查看Nodejs默认配置

```sh
npm config ls -l
; cli configs
long = true
metrics-registry = "https://registry.npm.taobao.org/"
scope = ""
user-agent = "npm/6.9.0 node/v10.16.0 win32 x64"

; userconfig C:\Users\sysker\.npmrc
registry = "https://registry.npm.taobao.org/"

; builtin config undefined
prefix = "C:\\Users\\sysker\\AppData\\Roaming\\npm"

; default values
access = null
allow-same-version = false
also = null
always-auth = false
audit = true
audit-level = "low"
auth-type = "legacy"
before = null
bin-links = true
browser = null
ca = null
cache = "C:\\Users\\sysker\\AppData\\Roaming\\npm-cache"
cache-lock-retries = 10
cache-lock-stale = 60000
cache-lock-wait = 10000
cache-max = null
cache-min = 10
cafile = undefined
cert = null
cidr = null
color = true
commit-hooks = true
depth = null
description = true
dev = false
dry-run = false
editor = "notepad.exe"
engine-strict = false
fetch-retries = 2
fetch-retry-factor = 10
fetch-retry-maxtimeout = 60000
fetch-retry-mintimeout = 10000
force = false
git = "git"
git-tag-version = true
global = false
global-style = false
globalconfig = "C:\\Users\\sysker\\AppData\\Roaming\\npm\\etc\\npmrc"
globalignorefile = "C:\\Users\\sysker\\AppData\\Roaming\\npm\\etc\\npmignore"
group = 0
ham-it-up = false
heading = "npm"
https-proxy = null
if-present = false
ignore-prepublish = false
ignore-scripts = false
init-author-email = ""
init-author-name = ""
init-author-url = ""
init-license = "ISC"
init-module = "C:\\Users\\sysker\\.npm-init.js"
init-version = "1.0.0"
json = false
key = null
legacy-bundling = false
link = false
local-address = undefined
loglevel = "notice"
logs-max = 10
; long = false (overridden)
maxsockets = 50
message = "%s"
; metrics-registry = null (overridden)
node-options = null
node-version = "10.16.0"
noproxy = null
offline = false
onload-script = null
only = null
optional = true
otp = null
package-lock = true
package-lock-only = false
parseable = false
prefer-offline = false
prefer-online = false
; prefix = "C:\\Program Files\\nodejs" (overridden)
preid = ""
production = false
progress = true
proxy = null
read-only = false
rebuild-bundle = true
; registry = "https://registry.npmjs.org/" (overridden)
rollback = true
save = true
save-bundle = false
save-dev = false
save-exact = false
save-optional = false
save-prefix = "^"
save-prod = false
scope = ""
script-shell = null
scripts-prepend-node-path = "warn-only"
searchexclude = null
searchlimit = 20
searchopts = ""
searchstaleness = 900
send-metrics = false
shell = "C:\\WINDOWS\\system32\\cmd.exe"
shrinkwrap = true
sign-git-commit = false
sign-git-tag = false
sso-poll-frequency = 500
sso-type = "oauth"
strict-ssl = true
tag = "latest"
tag-version-prefix = "v"
timing = false
tmp = "C:\\Users\\sysker\\AppData\\Local\\Temp"
umask = 0
unicode = false
unsafe-perm = true
update-notifier = true
usage = false
user = 0
; user-agent = "npm/{npm-version} node/{node-version} {platform} {arch}" (overridden)
userconfig = "C:\\Users\\sysker\\.npmrc"
version = false
versions = false
viewer = "browser"
```

