
### 视频截取

```css
ffmpeg -i input.mp4 -ss 00:00:10 -t 00:00:20 -c copy output.mp4
```

这个命令将截取从第 10 秒开始、持续 20 秒的视频段，并将其保存为 output.mp4。具体来说，命令参数的含义如下：

-i input.mp4：指定输入文件为 input.mp4。  
-ss 00:00:10：指定截取视频的开始时间为 10 秒。  
-t 00:00:20：指定截取视频的持续时间为 20 秒。  
-c copy：指定使用“copy”模式，这样可以保留视频的编码格式和画质。  
output.mp4：指定输出文件为 output.mp4。


### 视频转换

```shell
ffmpeg -i test.mp4 test1.mp4
```


### 丢帧视频修复

```
ffmpeg -f lavfi -i movie=国际建筑减排、碳中和发展趋势.mp4 -c:v libx264 -crf 18 -preset veryfast -c:a copy .\convert\国际建筑减排、碳中和发展趋势.mp4
```


```
ffmpeg -i 国际建筑减排、碳中和发展趋势.mp4 -vf minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1 -c:a copy .\convert\国际建筑减排、碳中和发展趋势.mp4
```