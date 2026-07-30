在 CentOS 上离线安装 Nginx 需要提前准备好 Nginx 的安装包及其依赖包。以下是详细的步骤：

---

### **1. 准备工作**
1. **在一台可以联网的 CentOS 机器上**：
   - 下载 Nginx 及其依赖包。
   - 将这些包拷贝到目标离线机器。

2. **在目标离线机器上**：
   - 确保系统版本与下载依赖包的机器一致（例如 CentOS 7 或 CentOS 8）。
   - 确保有 `root` 或 `sudo` 权限。

---

### **2. 在联网机器上下载 Nginx 及其依赖包**
1. 安装 `yum-utils` 工具（用于下载 RPM 包及其依赖）：
   ```bash
   sudo yum install yum-utils -y
   ```

2. 创建目录存放下载的 RPM 包：
   ```bash
   mkdir ~/nginx-offline
   cd ~/nginx-offline
   ```

3. 下载 Nginx 及其依赖包：
   - 如果使用官方 Nginx 仓库：
     ```bash
     sudo yum install nginx --downloadonly --downloaddir=./ --installroot=/tmp/nginx-installroot
     ```
   - 如果使用 EPEL 仓库：
     - 先安装 EPEL 仓库：
       ```bash
       sudo yum install epel-release -y
       ```
     - 然后下载 Nginx：
       ```bash
       sudo yum install nginx --downloadonly --downloaddir=./
       ```

4. 将下载的 RPM 包打包：
   ```bash
   tar -czvf nginx-offline.tar.gz ./*.rpm
   ```

5. 将 `nginx-offline.tar.gz` 文件拷贝到目标离线机器（例如使用 U 盘或 SCP 传输）。

---

### **3. 在离线机器上安装 Nginx**
6. 将 `nginx-offline.tar.gz` 文件解压：
   ```bash
   tar -xzvf nginx-offline.tar.gz
   ```

7. 进入解压后的目录：
   ```bash
   cd nginx-offline
   ```

8. 使用 `rpm` 命令安装所有 RPM 包：
   ```bash
   sudo rpm -ivh *.rpm --nodeps --force
   ```
   - `--nodeps`：忽略依赖检查（因为依赖包已经下载）。
   - `--force`：强制安装。

9. 验证 Nginx 是否安装成功：
   ```bash
   nginx -v
   ```
   如果显示 Nginx 版本号，说明安装成功。

---

### **4. 配置和启动 Nginx**
10. 启动 Nginx 服务：
   ```bash
   sudo systemctl start nginx
   ```

11. 设置 Nginx 开机自启：
   ```bash
   sudo systemctl enable nginx
   ```

12. 检查 Nginx 服务状态：
   ```bash
   sudo systemctl status nginx
   ```

13. 验证 Nginx 是否正常运行：
   - 打开浏览器，访问 `http://<服务器IP>`。
   - 如果看到 Nginx 欢迎页面，说明安装成功。

---

### **5. 防火墙配置（可选）**
如果启用了防火墙，需要开放 HTTP（80 端口）和 HTTPS（443 端口）：
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

### **6. 卸载 Nginx（可选）**
如果需要卸载 Nginx，可以使用以下命令：
```bash
sudo rpm -e nginx
```

---

### **总结**
通过以上步骤，你可以在 CentOS 上离线安装 Nginx。关键在于提前下载好 Nginx 及其依赖包，并在离线机器上使用 `rpm` 命令安装。