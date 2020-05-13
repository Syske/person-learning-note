- 进入autostart文件夹：

```sh
cd /home/pi/.config
mkdir autostart
cd autostart
```
- 在[autostart]目录中新建名为my.desktop的文件:

```sh
sudo vi my.desktop
```
文件内容:
```sh
[Desktop Entry]
Type=Application
Exec=chromium-browser  --disable-popup-blocking --no-first-run --disable-desktop-notifications  --kiosk "http://www.aifei.com/"
```
上面的网址可以修改成自己需要的URL, 保存退出, 重启:
```sh
sudo reboot
```

