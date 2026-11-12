## 工作笔记 | 来，我们今天来学习一个古老的知识：weblogic创建domain

## 前言

最近在整理之前的工作笔记，稍后会一一分享出来，希望这些知识能够帮到你。今天分享的是`weblogic`创建`domain`的过程，话不多说，直接开始正文





## 创建domain

- 首先进入weblogic的安装目录，具体如下：
```sh
cd /wls/Oracle/Middleware/Oracle_Home/wlserver/common/bin
```

### 图形化创建
- 1、下载xmanager软件
- 2、使用远程连接工具链接linux操作系统
- 3、在模拟终端上执行如下命令：
```
export DISPLAY=localhost:10.0
```
见下图
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-01.png)

- 4、执行如下命令：
```
./config.sh
```
**注意：** 第一次输入这个命令可能会报如下错误
```sh
Exception in thread "main" java.awt.AWTError: Can't connect to X11 window server using 'localhost:10.0' as the value of the DISPLAY variable.
	at sun.awt.X11GraphicsEnvironment.initDisplay(Native Method)
	at sun.awt.X11GraphicsEnvironment.access$200(X11GraphicsEnvironment.java:65)
	at sun.awt.X11GraphicsEnvironment$1.run(X11GraphicsEnvironment.java:115)
	at java.security.AccessController.doPrivileged(Native Method)
	at sun.awt.X11GraphicsEnvironment.<clinit>(X11GraphicsEnvironment.java:74)
	at java.lang.Class.forName0(Native Method)
	at java.lang.Class.forName(Class.java:264)
	at java.awt.GraphicsEnvironment.createGE(GraphicsEnvironment.java:103)
	at java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment(GraphicsEnvironment.java:82)
	at sun.awt.X11.XToolkit.<clinit>(XToolkit.java:126)
	at java.lang.Class.forName0(Native Method)
	at java.lang.Class.forName(Class.java:264)
	at java.awt.Toolkit$2.run(Toolkit.java:860)
	at java.awt.Toolkit$2.run(Toolkit.java:855)
	at java.security.AccessController.doPrivileged(Native Method)
	at java.awt.Toolkit.getDefaultToolkit(Toolkit.java:854)
	at sun.swing.SwingUtilities2.getSystemMnemonicKeyMask(SwingUtilities2.java:2020)
	at javax.swing.plaf.basic.BasicLookAndFeel.initComponentDefaults(BasicLookAndFeel.java:1158)
	at javax.swing.plaf.metal.MetalLookAndFeel.initComponentDefaults(MetalLookAndFeel.java:431)
	at javax.swing.plaf.basic.BasicLookAndFeel.getDefaults(BasicLookAndFeel.java:148)
	at javax.swing.plaf.metal.MetalLookAndFeel.getDefaults(MetalLookAndFeel.java:1577)
	at javax.swing.UIManager.setLookAndFeel(UIManager.java:539)
	at javax.swing.UIManager.setLookAndFeel(UIManager.java:579)
	at javax.swing.UIManager.initializeDefaultLAF(UIManager.java:1349)
	at javax.swing.UIManager.initialize(UIManager.java:1459)
	at javax.swing.UIManager.maybeInitialize(UIManager.java:1426)
	at javax.swing.UIManager.getDefaults(UIManager.java:659)
	at javax.swing.UIManager.put(UIManager.java:988)
	at com.oracle.cie.common.ui.gui.GUIHelper.initPLAF(GUIHelper.java:51)
	at com.oracle.cie.wizard.internal.cont.GUIContext.<clinit>(GUIContext.java:296)
	at com.oracle.cie.wizard.internal.cont.GUITaskContainer.createTaskContext(GUITaskContainer.java:73)
	at com.oracle.cie.wizard.internal.cont.GUITaskContainer.createTaskContext(GUITaskContainer.java:21)
	at com.oracle.cie.wizard.internal.cont.AbstractTaskContainer.init(AbstractTaskContainer.java:32)
	at com.oracle.cie.wizard.internal.cont.GUITaskContainer.init(GUITaskContainer.java:21)
	at com.oracle.cie.wizard.internal.engine.WizardControllerEngine.loadTaskContainer(WizardControllerEngine.java:656)
	at com.oracle.cie.wizard.internal.engine.WizardControllerEngine.configureMode(WizardControllerEngine.java:595)
	at com.oracle.cie.wizard.internal.engine.WizardControllerEngine.init(WizardControllerEngine.java:172)
	at com.oracle.cie.wizard.WizardController.createWizardEnine(WizardController.java:110)
	at com.oracle.cie.wizard.WizardController.<init>(WizardController.java:28)
	at com.oracle.cie.wizard.WizardController.invokeWizardAndWait(WizardController.java:119)
	at com.oracle.cie.wizard.WizardController.main(WizardController.java:67)
```
报错没有关系，再次输入该命令就可以正常进入创建界面

- 5、然后会弹出和windows环境相同的界面，后续操作同windows
- 具体步骤
    - 第一步：<br>
![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-02.png)
    - 第二步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-03.png)
    - 第三步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-04.png)
    - 第四步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-05.png)
    - 第五步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-06.png)
    - 第六步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-07.png)
    - 第七步<br>
    ![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/weblogic-linux-08.png)
- 至此，domain创建完成

## 结语

不知道还有没有小伙伴在使用`weblogic`，阿里巴巴作为国内`java`的大厂，从当年发起去`IOE`（`IBM`、`Oracle`、`EMC`）运动开始，`IOE`的相关产品就开始在国内的慢慢消失了，毕竟是国内`java`的领导者，大家都紧跟阿里的架构，除了部分政府单位还在使用外相关组件外，国内鲜有互联网公司使用，而且随着信息安全的不断加强，现在政府招投标的新项目也开始去`IOE`，所以如果你掌握了这门技术，就可以独领风骚了🤣

好了，闲扯完毕，大家晚安哦！
