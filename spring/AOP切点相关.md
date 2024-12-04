[TOC]

### 1、切点定义

#### 切点定义包含两个部分

> 一个切入点表达式
> 一个包含名字和任意参数的方法签名

```
package com.sysker.aspect;

import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;

@Aspect
public class CreatePointcut {
    @Pointcut("execution(* transfer(..))")
    private void anyOldTransfer() { }
}

```
- 在@AspectJ风格的AOP中，切入点签名采用一个普通的方法定义（方法体通常为空）来提供，且该方法的返回值必须是void；切入点表达式需要使用@Point注解来标注，如上代码
- 切入点表达式，也就是@Pointcut 注解的值，是正规的AspectJ 切入点表达式
- 如果需要使用本切面类中的切入点，则可以在使用@Before、@After、@Around等注解定义Advice时，使用pointcut或value属性值引用已有的切入点
```
package com.sysker.aspect;

import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;

@Aspect
public class CreatePointcut {
    @Pointcut("execution(* transfer(..))")
    private void anyOldTransfer() {}
    
    @Pointcut("execution(* transfer(..))")
    public void myPointcut() {}

    @AfterReturning(pointcut = "mypointcut()", returning = "retVal")
    public void writeLog(String msg, Object retVal) {

    }
}

```

- private修饰的切点，其他切面类不能使用，而且在引用其他切面类中的切点时，必须添加类名前缀

```
    @After(value="CreatePointcut.myPointcut()")
    public void show() {
        System.out.println("myPointcut模拟释放资源");
    }
```

### 2、切入点指示符

#### 2.1 execution:匹配执行方法的连接点，用法相对复杂，表达式如下：
```
execution(modifiers-pattern? ret-type-pattern declaring-type-pattern? name-pattern(param-pattern) throws-pattern?)
```
- modifiers-pattern:指定方法的修饰符，支持通配，该部分可省略；
- ret-type-pattern:指定方法的返回值类型，支持通配符，可以使用“*”通配符来匹配所有的返回值类型
- declaring-type-pattern:指定方法所属的类，支持通配符，该部分可省略；
- name-pattern：指定匹配指定的方法名，支持通配，可以使用“*”通配符来匹配所有方法
- parapn-pattern:指定方法声明中的形参列表，支持两个通配符，即“\*”和“..”，其中“\*”代表一个任意类型的参数，而（..）代表零个或多个任意类型的参数
- throws-pattern：指定方法声明抛出的异常，支持通配符，该部分可省略



#### 2.2 within:用于限定匹配特定类型的连接点，当使用Spring AOP的时候，只能匹配方法执行的连接点

```
// 在com.sysker.service包中的任意连接点（在Spring AOP中只是方法执行的连接点）
within(com.sysker.service.*)
// 在com.sysker.service包或其子包中的任意连接点（在Spring AOP中只是方法执行的连接点）
within(com.sysker.service..*)
```

#### 2.3 this:用于限定AOP代理必须指定类型的实例，匹配该对象的所有连接点，当使用Spring AOP的时候，只能匹配方法执行的连接点

```
// 匹配实现了 com.sysker.service.AccountService接口的AOP代理的所有连接点
// 在SpringAOP中只是方法执行的连接点
this(com.sysker.service.AccountService)
```

#### 2.4 target:用于对连接点的参数类型进行限制，要求参数类型是指定类型的实例，当使用Spring AOP的时候，只能匹配方法执行的连接点

```
// 匹配实现了 com.sysker.service.AccountService.AccountService 接口的目标对象的所有连接点
// 在Spring AOP中只是方法执行的连接点
target(com.sysker.service.AccountService.AccountService)
```

#### 2.5 args:用于对连接点的参数类型进行限制，要求参数类型是指定类型的实例。当使用Spring AOP的时候，只能匹配方法执行的连接点。
```
// 匹配只接受一个参数，且传入的参数类型是serializable
// 在Spring AOP中只是方法执行的连接点
target(com.sysker.service.AccountService.AccountService)
```

#### 2.6 bean:用于限定只匹配指定bean实例内的连接点，实际上只能使用方法执行行为作为连接点
- 定义bean表达式时需要传入bean的id或name,表示只匹配该bean实例内的连接点，支持使用“*”通配符

```
// 匹配tradeService Bean实例内方法执行的连接点
bean(tradeService)
// 匹配名字以service结尾的Bean实例内方法执行的连接点
bean（*Service）
```

### 3 组合切入点表达式

> && ：要求连接点同时匹配两个切入点表达式

> || ：只要连接点匹配任意一个切入点表达式

> ! : 要求连接点不匹配指定的切入点表达式



#aop  