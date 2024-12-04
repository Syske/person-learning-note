# 树莓派安装openCV

## 准备工作
### 安装依赖
#### 安装编译openCV源码的工具
```
sudo apt-get install build-essential cmake pkg-config
```

#### 图像处理和视频处理的包
```
sudo apt-get install libjpeg-dev libtiff5-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
```

#### 图像展示的功能需要依模块
```
sudo apt install libgtk2.0-dev libatlas-base-dev gfortran
```

```
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=/home/pi/opencv-4.6.0/modules -D BUILD_EXAMPLES=ON -D WITH_LIBV4L=ON PYTHON3_EXECUTABLE=/usr/bin/python3.7 PYTHON_INCLUDE_DIR=/usr/include/python3.7 PYTHON_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython3.7m.so PYTHON3_NUMPY_INCLUDE_DIRS=/usr/lib/python3/dist-packages/numpy/core/include ..

```