# arduino控制无线小车

### 前言


### 项目过程

#### 准备材料

- `arduino`开发板`1`个
- `L9110S`电机驱动板`1`个
- 双轴摇杆`1`个
- 双马达小车`1`个
- 杜邦线若干

全家福如下：
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230320211504.png)

#### 接线

电源部分，`L9110`接的是`5V`电压，摇杆连接的是`3.3V`电压，电机驱动板如果供电电压不够，可能无法正常驱动电机；
两个电机直接连接驱动板就可以

序号 | arduino | L9110 | 摇杆 | 备注
---  | ---     | ---   | --- | ---
1   | A0      |   /   | VRX  | 采集`X`轴数据
2   | A1      | /    | VRY   | 采集`Y`轴数据
3   |PWM2     |  A1A    | \  | 控制第一个电机输出
4   |PWM3     |  A1B    | \  | 控制第一个电机输出
5   |PWM4     | A2A     | \  | 控制第二个电机输出
6   |PWM5     | A2B     | \  | 控制第二个电机输出


电路连接示意图：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/20230320220327.png)

#### 代码

这里的代码和我们前面分享的控制丝杆电机部分的内容没有太大区别，`X`负责控制前进和后退，`Y`轴负责转向。

需要注意的是，转向和前进后退是冲突的，所以在转向的时候，要尽可能避免摇杆`X`轴方向的偏移量，否则会出现电机停止转动的情况。

代码中，为了避免转向时会触发`X`的偏移，已经把`Y`轴的控制量调到比较大的数值。

```c
// L9110s驱动板A-1A引脚，连接arduino uno的2号引脚（PWM区的2号，也叫就是d2引脚）
const int IA = 2; 
// L9110s驱动板A-1B引脚，连接arduino uno的3号引脚（PWM区的3号，也叫就是d3引脚）
const int IB = 3;

const int IIA = 4;

const int IIB = 5;
// 摇杆的x轴引脚，连接A0引脚（analog区的第1个引脚）,analog是模拟区，本引脚用于输入模拟信号
const int joyStick_x = 0;// GPIO15(D8) x
// 摇杆的y轴引脚，连接A1引脚（analog区的第2个引脚）
const int joyStick_y = 1;
// 摇杆z轴引脚，连接d7引脚
const int joyStick_z = 8;

// 电机的转速，范围是0-255，本次只有一个电机，所以只关注x轴
byte speed_x = 0;  // change this (0-255) to control the speed of the motor
byte speed_y = 0;
void setup() {
  // 把电机驱动板的引脚设置为输出模式
  pinMode(IA, OUTPUT); // set pins to output
  pinMode(IB, OUTPUT);
  // 设置波特率
  Serial.begin(9600);
}
void loop() {

  int x, y, z;
  // 获取x轴的模拟量，这里输入的是模拟量，所以必须是支持模拟量输入的引脚，之前通过esp8266获取到的值异常，就是因为esp8266没有模拟量输入引脚
  x = analogRead(joyStick_x);
  // 获取y轴的模拟量
  y = analogRead(joyStick_y);
  // 获取z的输入值，z轴为数字输入，只有0和1
  z = digitalRead(joyStick_z);

  Serial.print("joyStick: x=");
  Serial.print(x, DEC);
  Serial.print(",y=");
  Serial.print(y, DEC);
  Serial.print(",z=");
  Serial.println(z, DEC);

  // 以下数值要根据自己的摇杆测试获取，如果取值有问题，会出现电机速度输出不稳定的情况，比如我手里的这款摇杆，静止状态下x轴的值在325-327之间波动，y轴在333-337之间波动
  if (x <= 330 && x > 320) { // 静止区（也就是默认情况下摇杆的模拟输入值）
    analogWrite(IA, 0);
    analogWrite(IB, 0);

    analogWrite(IIA, 0);
    analogWrite(IIB, 0);
  }  else if (x <= 320) { // 向右推摇杆，越靠近中间值速度越慢
    // 获取速度模拟值
    speed_x = map(x, 320, 0, 0, 255);
    analogWrite(IA, 0);
    analogWrite(IB, speed_x);

    analogWrite(IIA, 0);
    analogWrite(IIB, speed_x);
  } else if (x > 330) { // 向左推摇杆，越靠近中间值速度越慢，摇杆的最大模拟值需要实测，我这里最大值是827左右，这里取模拟值的时候一定要包含摇杆的取值范围，否则再靠近边界的时候会出现转速抖动
    speed_x = map(x, 320, 830, 0, 255);
    analogWrite(IA, speed_x);
    analogWrite(IB, 0);

    analogWrite(IIA, speed_x);
    analogWrite(IIB, 0);
  }

  // 转向
  // 以下数值要根据自己的摇杆测试获取，如果取值有问题，会出现电机速度输出不稳定的情况，比如我手里的这款摇杆，静止状态下x轴的值在325-327之间波动，y轴在333-337之间波动
 if (y <= 200) { // 向右推摇杆，越靠近中间值速度越慢
    // 获取速度模拟值
    speed_y = map(y, 320, 0, 0, 255);
    analogWrite(IA, 0);
    analogWrite(IB, 0);

    analogWrite(IIA, 0);
    analogWrite(IIB, speed_y);
  } else if (y > 500) { // 向左推摇杆，越靠近中间值速度越慢，摇杆的最大模拟值需要实测，我这里最大值是827左右，这里取模拟值的时候一定要包含摇杆的取值范围，否则再靠近边界的时候会出现转速抖动
    speed_x = map(y, 320, 830, 0, 255);
    analogWrite(IA, 0);
    analogWrite(IB, speed_y);

    analogWrite(IIA, 0);
    analogWrite(IIB, 0);
  }

  
  Serial.print("speed:");
  Serial.println(speed_x, DEC);
  delay(15);
}
```

### 总结
