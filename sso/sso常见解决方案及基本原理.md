### 是什么

`sso`完整的写法是Single Sign On，中文的意思是单点登陆，更详细的解释是：**在多个应用系统中，只需要登录一次，就可以访问其他相互信任的应用系统。**

如果不采用单点登陆系统，那么用户访问多个应用时是这样的：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200329221250.png)

但如果采用了单点登陆系统，那就简便了很多：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200329220520.png)

也就是，当你有多个系统时（一般大型企业应用中会有这种需求，比如阿里巴巴），用户只需要登陆一次，即可访问所有应用系统，而不需要频繁登陆。

### 为什么

为什么要采用`sso`，它有什么样的应用场景呢？前面我们提了一句，就是为了增加用户体验，避免用户重复登陆。特别是在一些大型应用系统中，如果应用系统数量比较庞大，每个系统都需要用户去重新登陆，那想想都觉得可怕，毕竟现如今这种情况也比较多。基于以上原因（应该不够完整），单点登陆应用需求应运而生。

### 怎么实现

上面我们简单说了`sso`的应用场景，以及采用`sso`的原因，`sso`具体又是如何实现的，它的原理到底是怎样的呢？现在我们就来探讨下吧。

`sso`的目的是为了增加用户体验，避免每个应用系统都要单独登陆认证的情况。具体的实现原理大致如下：

将登陆、授权、鉴权等操作单独抽取出来整合成一个系统，各个用户系统之间共享用户信息，当用户访问某一个系统时，该系统会根据用户的请求校验是否登陆，若未登陆则跳转至单点登陆系统，用户登陆成功后，跳转至原应用系统，同时会将用户信息存至信息共享区，方便其他应用系统获取用户信息，流程图表示如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200329212320.png)

我承认我画的图很一般😂，我要好好努力。关于用户信息共享的实现方式，大致有如下几种

- session共享
- cookie共享
- token共享

#### session共享

将用户信息存储在session会话中，设置过期时间，用户登陆成功后，将用户会话id返回，每次用户发送请求时需携带sessionid，根据sessionid校验用户状态信息

#### cookie共享

cookie共享用户信息，就是将用户信息通过加密后存储到客户端（浏览器），用户发送请求时携带cookie数据，而且必须满足如下条件，才能实现信息共享：

- Domain必须是相同的，也就是所有应用必须是同一个父级域名，如www.taotao.com，Sso.taotao.com，Search.taotao.com，需要设置domain为.taotao.com。
- 设置path：/

存在的问题是若客户端限制了cookie的使用，这时会比较麻烦

#### token共享

token共享的方式比较灵活，具体的来说就是，用户登陆成功后，会返回一个特殊的token串给客户端，每次发送请求时用户需携带token，token本身可以设置过期时间，客户端存储比较方便，可以存在cookie、localstorage、sessionstorage中。

### 目前常用的解决方案

#### CAS

 cas是 Yale 大学发起的一个企业级的、开源的项目，旨在为 Web 应用系统提供一种可靠的单点登录解决方法（属于 Web SSO）

CAS 包括两部分： CAS Server 和 CAS Client 。CAS Server 负责完成对用户的认证工作 , 需要独立部署 , CAS Server 会处理用户名 / 密码等凭证(Credentials) 。CAS Client与受保护的客户端应用部署在一起，以 Filter 方式保护受保护的资源。负责处理对客户端受保护资源的访问请求，需要对请求方进行身份认证时，重定向到 CAS Server 进行认证。（原则上，客户端应用不再接受任何的用户名密码等 Credentials）

基本协议过程如下：

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/20200329220426.png)

#### JWT

Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（[(RFC 7519](https://link.jianshu.com?t=https://tools.ietf.org/html/rfc7519)).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。

这里不做过多说明，因为后面还会详细讲到，会有详细的讲解和示例。

#### Spring Security

Spring Security是一个功能强大且高度可定制的身份验证和访问控制框架。它是用于保护基于Spring的应用程序的实际标准。

Spring Security是一个框架，致力于为Java应用程序提供身份验证和授权。与所有Spring项目一样，Spring Security的真正强大之处在于可以轻松扩展以满足自定义要求

