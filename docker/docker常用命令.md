# docker常用命令

#docker

### 进入容器

```sh
docker exec -it 6da28a1614c6 bash
```

### 启动容器
```
 docker run -it --name ubuntun-hass --network host \
-p 8022:22 \
-p 8123:8123 \
-v /home/syske/WorkSpace:/workspace \
--privileged \
 ubuntu-hass:latest
```