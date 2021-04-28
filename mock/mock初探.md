# MOCK初探

## 背景

最近刚完成一个`bug`的修复，但是根据公司代码质量管理要求，所以改动代码必须编写测试用例，而且测试用例覆盖率必须达到`50%`，测试用例通过后，代码通过`sonar`扫描通过后（没有`bug`，单元测试他通过率大于]`50%`），方能将代码合入`master`分支，从这一点上讲，现在公司的代码管理确实规范多了，不像我之前待过的公司，测试、发布都是根据自己需要，想咋样都可以，代码质量压根就没管理。

基于以上要求，我必须得自己写单元测试了，但之前确实没咋写过单元测试，对与`Junit`也仅仅停留在会用`@Test`注解，然后没了。所以单元测试这块一切都要重头学，但是为了效率我是没时间看教程的，只能照葫芦画瓢，照猫画虎，因此今天的内容全是我这两天直接实战踩坑的血泪史，不涉及官方文档和资料，需要说明的是，今天我们的单元测试是基于`mockito`实现的。



## 踩坑过程

为了尽可能接近我实战的环境，这里的业务代码都是伪代码，我们先创建`springboot`项目，同时引入`mock`的依赖。

### mock依赖

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>3.6.0</version>
</dependency>
```

#### MOCK的第一眼

项目创建完成后，我们直接来看案例，我当时第一次看到别的单元测试是这样的：

```java
/**
 * test
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-28 下午10:14
 */
@RunWith(MockitoJUnitRunner.class)
public class UserServiceServiceTest {
    @InjectMocks
    private UserServiceImpl userService;
    @Mock
    private UserMapper userMapper;
    @Mock
    private MessageServiceImpl messageService;

    @Test
    public void saveUserTest1() {
        String userId = "test2312";
        given(userMapper.selectUser(anyString())).willReturn("admin");
        int saveUser1 = userService.saveUser(userId);
        assertEquals(saveUser1, -1);
    }

    @Test
    public void saveUserTest2() {
        String userId = "test2312";
        given(userMapper.intsertUser(anyString())).willReturn(2);
        given(messageService.sendMessage(anyString())).willReturn("user insert success");
        int saveUser2 = userService.saveUser(userId);
        assertEquals(saveUser2, 4);
    }
}
```

看完之后，我一脸懵逼，这都是啥东西？啥作用？干啥用？这是啥操作？满脸的黑人问号。之前看代码，单元测试根本就没关心过，想着不就是`@Test`吗，我也写过呀，别人写的单元测试和我没关系。但是昨天开始研究和琢磨以后，我裂开了，这都什么东东，很难受反正。

不知道你看了上面的代码啥感觉，有没有和我第一次的感觉一样，上面的代码还是我简化之后的，如果你看到实际代码，可能会更崩溃，单词可能认识，注解没见过呀……反正是一次悲催，但还不错的体验，特别是顿悟之后的体验，不亚于解决了一个大`bug`。

### 关联代码

下面是关联代码，所有的代码都是伪代码，业务逻辑和昨天实际可能差距比较大，但是说明问题足够了：

#### Mapper

- enterprise

```java
/**
 * enterprise
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-28 下午9:57
 */
@Component
public class EnterpriseMapper {

    @Autowired
    private MessageServiceImpl messageService;

    public int insertEnterprise(Long id) {
        System.out.println("保存enterprise：" + id);
        messageService.sendMessage("企业保存成功");
        return 1;
    }

    public String selectEnterprise(Long id) {
        System.out.println("查询企业成功:" + id);
        return "" + id;
    }
}
```

- message

```java
/**
 * mapper
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-27 下午11:34
 */
@Component
public class MessageMapper {
    public List<String> listStrs(Long id) {
        return new ArrayList();
    }

    public String insert(String data) {
        System.out.println("保存数据");
        return data;
    }
}
```

- UserMapper

```java
/**
 * user
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-28 下午10:01
 */
@Component
public class UserMapper {

    public int intsertUser(String userId) {
        System.out.println("保存用户：" + userId);
        return 1;
    }

    public String selectUser(String userId) {
        System.out.println("查询用户：" + userId);
        return userId;
    }
}
```

#### Serive

- EnterpriseServiceImpl

```java
/**
 * Mockservice
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-27 下午11:29
 */
@Service
public class EnterpriseServiceImpl {

    @Autowired
    private EnterpriseMapper enterpriseMapper;

    @Autowired
    private UserServiceImpl userService;

    public String saveEnterpriseData(Long id, String userId, List<String> strs) {

        String enterprise = enterpriseMapper.selectEnterprise(id);
        if (!"admin".equals(enterprise)) {
            System.out.println("企业不存在");
            return "企业不存在";
        }
        int insertEnterprise = enterpriseMapper.insertEnterprise(id);
        int saveUser = userService.saveUser(userId);
        return "hello" + insertEnterprise + saveUser + strs;

    }
}
```

- MessageServiceImpl

```java
/**
 * mock2
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-28 下午9:51
 */
@Service
public class MessageServiceImpl {

    @Autowired
    private MessageMapper messageMapper;
    @Autowired
    private EnterpriseServiceImpl messageService;
    @Autowired
    private EnterpriseMapper enterpriseMapper;



    public String sendMessage(String message) {
        messageMapper.insert(message);
        return "success";
    }
}
```

- UserServiceImpl

```java
/**
 * user service
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-28 下午10:04
 */
@Service
public class UserServiceImpl {

    @Autowired
    private UserMapper userMapper;
    @Autowired
    private MessageServiceImpl messageService;

    public int saveUser(String userId) {
        if ("admin".equals(userMapper.selectUser(userId))) {
            System.out.println("用户已存在");
            return -1;
        }
        int i = userMapper.intsertUser(userId);
        String sendMessage = messageService.sendMessage("用户保存成功");
        System.out.println("发送消息成功：" + sendMessage);
        return 2 + i;
    }
}
```

### 开始踩坑

#### 第一次尝试

我参照第一眼的`mock`单元测试，写了自己人生中的第一个`Mock`单元测试，它大概长这样：

```java
/**
 * unit test
 *
 * @author syske
 * @version 1.0
 * @date 2021-04-27 下午11:13
 */
@RunWith(MockitoJUnitRunner.class)
public class EnterpriseServiceTest {

    @InjectMocks
    private EnterpriseServiceImpl enterpriseService;

    @Test
    public void test() {
        ArrayList<String> ls = new ArrayList<>();
        ls.add("sdfsdf");
        enterpriseService.saveEnterpriseData(any(), any(), any());
    }
}
```

但很不幸的是，第一步我就失败了（出师未捷身先死，太难了），红色的提示告诉我问题没这么难，不就是空指针吗：



#### 第N次尝试

捣鼓了半天，事实告诉我问题没这么简单，请教了身边的同事，他告诉我两点：

- `@InjectMocks`注入的是要测试的方法所属的类
- `@Mock`注入的是你方法要用到的类

但是知道了上面两点以后，我依然毫无进展，然后在我的无数次的坚持和摸索之下，我终于知道空指针的错误是因为依赖的类（就是项目中被`@Autowired`注入的类）要通过`@Mock`注入（别人告诉你的，在没理解，没形成认知，你思想上确实很难翻过那个梁），然后我把代码调整成这样：

```java
@RunWith(MockitoJUnitRunner.class)
public class EnterpriseServiceTest {

    @InjectMocks
    private EnterpriseServiceImpl enterpriseService;

    @Mock
    private EnterpriseMapper enterpriseMapper;

    @Test
    public void test() {
        ArrayList<String> ls = new ArrayList<>();
        ls.add("sdfsdf");
        enterpriseService.saveEnterpriseData(any(), any(), any());
    }
}
```

#### 再次失败

这时候错误变了，变成这样的提示了：

```sh
org.mockito.exceptions.misusing.InvalidUseOfMatchersException: 
Invalid use of argument matchers!
1 matchers expected, 3 recorded:
-> at io.github.syske.springbootmockdemo.EnterpriseServiceTest.test(EnterpriseServiceTest.java:38)
-> at io.github.syske.springbootmockdemo.EnterpriseServiceTest.test(EnterpriseServiceTest.java:38)
-> at io.github.syske.springbootmockdemo.EnterpriseServiceTest.test(EnterpriseServiceTest.java:38)

This exception may occur if matchers are combined with raw values:
    //incorrect:
    someMethod(anyObject(), "raw String");
When using matchers, all arguments have to be provided by matchers.
For example:
    //correct:
    someMethod(anyObject(), eq("String by matcher"));

For more info see javadoc for Matchers class.


	at io.github.syske.springbootmockdemo.service.EnterpriseServiceImpl.saveEnterpriseData(EnterpriseServiceImpl.java:28)
	at io.github.syske.springbootmockdemo.EnterpriseServiceTest.test(EnterpriseServiceTest.java:38)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:59)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:56)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.mockito.internal.runners.DefaultInternalRunner$1$1.evaluate(DefaultInternalRunner.java:54)
	at org.junit.runners.ParentRunner$3.evaluate(ParentRunner.java:306)
	at org.junit.runners.BlockJUnit4ClassRunner$1.evaluate(BlockJUnit4ClassRunner.java:100)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:366)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:103)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:63)
	at org.junit.runners.ParentRunner$4.run(ParentRunner.java:331)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:79)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:329)
	at org.junit.runners.ParentRunner.access$100(ParentRunner.java:66)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:293)
	at org.junit.runners.ParentRunner$3.evaluate(ParentRunner.java:306)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:413)
	at org.mockito.internal.runners.DefaultInternalRunner$1.run(DefaultInternalRunner.java:99)
	at org.mockito.internal.runners.DefaultInternalRunner.run(DefaultInternalRunner.java:105)
	at org.mockito.internal.runners.StrictRunner.run(StrictRunner.java:40)
	at org.mockito.junit.MockitoJUnitRunner.run(MockitoJUnitRunner.java:163)
	at org.junit.runner.JUnitCore.run(JUnitCore.java:137)
	at com.intellij.junit4.JUnit4IdeaTestRunner.startRunnerWithArgs(JUnit4IdeaTestRunner.java:68)
	at com.intellij.rt.execution.junit.IdeaTestRunner$Repeater.startRunnerWithArgs(IdeaTestRunner.java:47)
	at com.intellij.rt.execution.junit.JUnitStarter.prepareStreamsAndStart(JUnitStarter.java:242)
	at com.intellij.rt.execution.junit.JUnitStarter.main(JUnitStarter.java:70)
```

然后，又琢磨来半天，查了好多博客，问题也没接近，最后请教同事，他也解决不了，使劲浑身解数也没有解决。所以问题又回到了我这里，我得自己解决问了，毕竟解决问题这种高光时刻还是要交给我来完成的，最后我也没有辜负问题的重托，完美解决了它。最后竟然是因为我制定的参数不够精确，你敢信，你敢信，你敢信……这也再一次告诉我们，代码不会有错，一定是你的问题，好好反思自己的问题。

##### 扩展知识

这里要补充下`mock`的一些知识，主要涉及几个方法：

- `any()`：生成任意`Object`，需要传对象的地方都可以用
- `anyString`、`anyLong()`、`anyInt()`、`anyList()`……：生成对应的类型

上面这种方式，只针对可以为空的参数，类似于占位符，在调用具体方法的时候，必须准确传值，否则会报如上错误

#### 调用成功了

我把代码改成下面这也，单元测试通过了，也没报错：

```java
@RunWith(MockitoJUnitRunner.class)
public class EnterpriseServiceTest {

    @InjectMocks
    private EnterpriseServiceImpl enterpriseService;

    @Mock
    private EnterpriseMapper enterpriseMapper;

    @Test
    public void test() {
        ArrayList<String> ls = new ArrayList<>();
        ls.add("sdfsdf");
        enterpriseService.saveEnterpriseData(12323L, "testets", ls);
    }
}
```

#### 为了应对覆盖率继续改进

但是看了业务代码以后，我发现有部分业务没有跑，也就是单元测试未覆盖，如果要上线发布，那所有代码必须覆盖，所以我得想办法让业务继续往下走，这时候就是体现`given`方法价值的时候了，不过这都是后话，都是我经历了`N`次失败之后得出来的。

昨天下班走的时候，我突然意识到，`given`方法不就相当于方法的拦截器吗，拦截方法，修改返回结果，那一刻我觉得我顿悟了，然后一切都豁然开朗了，比如这样的用法，其实就是修改了`essageService.sendMessage`的执行结果，把方法的返回值改成了`user insert success`：

```java
given(messageService.sendMessage(anyString())).willReturn("user insert success");
```

**提示：** 需要注意的是你需要将`given`方法`mock`的方法的调用参数全部改成`any`类型的，否则你修改的方法结果是不生效的，返回值结果会是`NUll`:

```java
given(enterpriseMapper.selectEnterprise(12323L)).willReturn("admin");
```

但是这样写的话，返回值就是你`willReturn`指定的值：

```java
given(enterpriseMapper.selectEnterprise(anyLong())).willReturn("admin");
```

另外，还有一点要注意的是，`willReturn`指定的值类似必须和方法的返回值类型一致，否则会报编译错误。

加了`given`处理代码之后，单元测试就可以保证全覆盖了，但是不巧的是，这时候竟然报错了：

```sh
java.lang.NullPointerException
	at io.github.syske.springbootmockdemo.service.EnterpriseServiceImpl.saveEnterpriseData(EnterpriseServiceImpl.java:34)
	at io.github.syske.springbootmockdemo.EnterpriseServiceTest.test(EnterpriseServiceTest.java:39)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:59)
	at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
	at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:56)
	at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
	at org.mockito.internal.runners.DefaultInternalRunner$1$1.evaluate(DefaultInternalRunner.java:54)
	at org.junit.runners.ParentRunner$3.evaluate(ParentRunner.java:306)
	at org.junit.runners.BlockJUnit4ClassRunner$1.evaluate(BlockJUnit4ClassRunner.java:100)
	at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:366)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:103)
	at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:63)
	at org.junit.runners.ParentRunner$4.run(ParentRunner.java:331)
	at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:79)
	at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:329)
	at org.junit.runners.ParentRunner.access$100(ParentRunner.java:66)
	at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:293)
	at org.junit.runners.ParentRunner$3.evaluate(ParentRunner.java:306)
	at org.junit.runners.ParentRunner.run(ParentRunner.java:413)
	at org.mockito.internal.runners.DefaultInternalRunner$1.run(DefaultInternalRunner.java:99)
	at org.mockito.internal.runners.DefaultInternalRunner.run(DefaultInternalRunner.java:105)
	at org.mockito.internal.runners.StrictRunner.run(StrictRunner.java:40)
	at org.mockito.junit.MockitoJUnitRunner.run(MockitoJUnitRunner.java:163)
```

如果你`debug`方式跟一下代码，你就会发现，代码中`userService`的值是`null`，这时候你只需要在单元测试中`@Mock`一下`userService`就可以啦。这里报错的原因是，因为之前业务逻辑没有触发，单元测试并没有运行这里的代码，所以自然也不需要注入相关依赖，但是后面我们修改了返回值之后，业务逻辑发生变化，这时候后面代码要被执行，但是业务逻辑依赖的类没有被注入，自然就报错了。只需要`mock`相关依赖，方法就可以执行。

#### 再次扩展

关于`@Mock`我想补充一些内容，如果你只是`mock`了对应的类，那默认情况下该类所有实例方法的返回值都是`null`，但通常情况下，你为了满足一些特殊业务场景测试，需要定制返回值，那这时候`given`就显示出它的价值了，简单来说`given`就相当于方法的`mock`。

另外，还要补充一点——`assert`，中文名，断言，是`Junit`下的一个重要类，常用的方法有：`assertEquals`、`assertFalse`、`assertTrue`、`assertNull`等，简单来说就是对方法执行结果进行校验，以确保测试结果正确。



## 总结

其实，对于一个陌生事物，认知前和认知后，是一种很奇妙的感受，认知前你可能很难想明白，也想不通，哪怕别人告诉你答案，你也会困惑，因为你想不明白为什么；但是认知后，你又很难再回到再回到认知前那种呆萌状态，答案你就是在知道，但可能另一个人问你原因的时候，你可能也说不出来。这两种状态存在着某种临界点，你如果能够快速打破临界状态，那你的认知水平也会极大地提升。

今天的内容，我其实特别想记录自己对`mock`单元测试的整个认知过程，但是我觉得我失败了，就像我上面说的那样，从已经有认知的点，回看当时自己未认知前的状态，很多当时困惑的细节已经丧失了，而且也想不明白当时为什么不知道，整个过程是不可逆的，很玄学。

最后，想再说一点，其实学任何东西，都是实践出真知，就像今天这样，我在没有看官方文档，和相关教程的情况下，通过看代码，测试，还是对`MOCK`建立起了一些基础的认知，保证我可以很好地上手现在的工作，这样学习的好处在于，你的目标很明确，你就是要你的代码跑起来，虽然过程中会遇到很多问题，但你的目标始终不变。好了，今天就到这里吧，大家晚安

