### 是什么？

> Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（[(RFC 7519](https://link.jianshu.com?t=https://tools.ietf.org/html/rfc7519)).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。

jwt是一套完整的签名验证机制，可以使用秘密（使用**HMAC**算法）或使用**RSA**或**ECDSA**的公用/专用密钥对对JWT进行**签名**。

### 什么时候应该使用JSON Web令牌？

以下是JSON Web令牌有用的一些情况：

- **授权**：这是使用JWT的最常见方案。一旦用户登录，每个后续请求将包括JWT，从而允许用户访问该令牌允许的路由，服务和资源。单一登录是当今广泛使用JWT的一项功能，因为它的开销很小并且可以在不同的域中轻松使用。
- **信息交换**：JSON Web令牌是在各方之间安全地传输信息的好方法。因为可以对JWT进行签名（例如，使用公钥/私钥对），所以您可以确定发件人是他们所说的人。此外，由于签名是使用标头和有效负载计算的，因此您还可以验证内容是否遭到篡改。

### JSON Web令牌结构是什么？

JSON Web令牌以紧凑的形式由三部分组成，这些部分由点（`.`）分隔，分别是：

- 标头
- 有效载荷
- 签名

因此，JWT通常如下所示。

```
xxxxx.yyyyy.zzzzz
```

让我们分解不同的部分。

#### 标头

标头*通常*由两部分组成：令牌的类型（即JWT）和所使用的签名算法，例如HMAC SHA256或RSA。

例如：

```
{
  "alg": "HS256",
  "typ": "JWT"
}
```

然后，此JSON被**Base64Url**编码以形成JWT的第一部分。

#### 有效载荷

令牌的第二部分是有效负载，其中包含声明。声明是有关实体（通常是用户）和其他数据的声明。声明有以下三种类型：

- **标准中注册的声明**：这些是一组非强制性的但建议使用的预定义权利要求，以提供一组有用的，可互操作的权利要求。其中一些是： **iss**（发布者）， **exp**（到期时间）， **sub**（主题）， **aud**（受众群体）[等](https://tools.ietf.org/html/rfc7519#section-4.1)。

  > 请注意，声明名称仅是三个字符，因为JWT是紧凑的。

- **公共的声明**：使用JWT的人员可以随意定义这些声明。但是为避免冲突，应在[ IANA JSON Web令牌注册表](https://www.iana.org/assignments/jwt/jwt.xhtml)中定义它们，或将其定义为包含抗冲突名称空间的URI。

- **私有的声明**：这些都是使用它们同意并既不是当事人之间建立共享信息的自定义声明*注册*或*公众*的权利要求。

有效负载示例可能是：

```
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

然后，对有效负载进行**Base64Url**编码，以形成JSON Web令牌的第二部分。

> 请注意，对于已签名的令牌，此信息尽管可以防止篡改，但任何人都可以读取。除非将其加密，否则请勿将机密信息放入JWT的有效负载或报头元素中。

#### 签名

要创建签名部分，您必须获取编码的标头，编码的有效载荷，机密，标头中指定的算法，并对其进行签名。

例如，如果要使用HMAC SHA256算法，则将通过以下方式创建签名：

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

签名用于验证消息在此过程中没有更改，并且对于使用私钥进行签名的令牌，它还可以验证JWT的发送者是它所说的真实身份。

#### 放在一起

输出是三个由点分隔的Base64-URL字符串，可以在HTML和HTTP环境中轻松传递这些字符串，与基于XML的标准（例如SAML）相比，它更紧凑。

下面显示了一个JWT，它已对先前的标头和有效负载进行了编码，并用一个秘密进行签名。 ![](https://gitee.com/sysker/picBed/raw/master/images/20200331094307.png)

如果您想使用JWT并将这些概念付诸实践，则可以使用[jwt.io Debugger](https://jwt.io/#debugger-io)解码，验证和生成JWT。

### 简单示例

是不是看到这里还是不知所云，其实我当时也是这么觉得的，后来通过实践，才慢慢理解，所以这里我们也废话少说，show me code。

#### 创建springboot项目

本次示例采用的技术架构为：springboot + redis + shiro，页面模板引擎用的是thymeleaf，首先我们创建个spring boot项目，为啥用spring boot，因为构建项目快啊，简单方便。然后添加如下依赖（完整的直接去githu，会放链接）：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
    <exclusions>
        <exclusion>
            <groupId>io.lettuce</groupId>
            <artifactId>lettuce-core</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<dependency>
    <groupId>com.auth0</groupId>
    <artifactId>java-jwt</artifactId>
    <version>3.7.0</version>
</dependency>

<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-core</artifactId>
    <version>1.3.2</version>
</dependency>
<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-spring</artifactId>
    <version>1.3.2</version>
</dependency>
```

因为我们这里用不到数据库，所以就不配置数据库相关信息，但如果你不配置数据库，springboot启动会报错，为了让springboot启动不报错，我们要在springboot启动入口添加如下注解：

```java
@SpringBootApplication(exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class})
```

然后就可以启动了，如果没有什么问题，继续往下看

#### 编写jwt工具类

如果你在此之前连jwt是什么也不清楚，那也没关系，先参照下面的代码写，我下面会解释。我当时第一次接触jwt的时候也是这么过来的，别害怕，就是干，别问谁给我的勇气，反正不是梁静茹😂

```java
public class JwtUtil {
    private static Logger logger = LoggerFactory.getLogger(JwtUtil.class);

    private JwtUtil() {}
    /**
     * Description: 生成一个jwt字符串
     *
     * @param username    用户名
     * @param timeOut 超时时间（单位ms）
     * @return java.lang.String
     * @author syske
     * @date 2019/3/4 17:26
     */
    public static String encode(String username, String secret, long timeOut) {
        Algorithm algorithm = Algorithm.HMAC256(secret);
        String token = JWT.create()
                //设置过期时间为一个小时
                .withExpiresAt(new Date(System.currentTimeMillis() + timeOut))
                //设置负载
                .withClaim("username", username)
                .sign(algorithm);
        return token;
    }

    /**
     * Description: 解密jwt
     *
     * @param token  token
     * @param secret secret
     * @return java.util.Map<java.lang.String, com.auth0.jwt.interfaces.Claim>
     * @author syske
     * @date 2019/3/4 18:14
     */
    public static Map<String, Claim> decode(String token, String secret) {
        if (StringUtils.isEmpty(token) || StringUtils.isEmpty(secret)) {
            logger.info("token：" + token + " , secret:" + secret);
            throw new AuthorizationException("用户状态校验失败:会话已过期，请重新登陆");
        }
        Algorithm algorithm = Algorithm.HMAC256(secret);
        JWTVerifier jwtVerifier = JWT.require(algorithm).build();
        DecodedJWT decodedJWT = null;
        try {
            decodedJWT = jwtVerifier.verify(token);
        } catch (TokenExpiredException e) {
            logger.error("会话已过期，请重新登陆:", e);
            throw new AuthorizationException("会话已过期，请重新登陆");
        }
        return decodedJWT.getClaims();
    }

    /**
     * 获得token中的信息无需secret解密也能获得
     *
     * @return token中包含的用户名
     */
    public static String getUsername(String token) {
        try {
            DecodedJWT jwt = JWT.decode(token);
            return jwt.getClaim("username").asString();
        } catch (JWTDecodeException e) {
            logger.error("获取用户名信息失败：", e);
            throw new AuthorizationException("获取用户名信息失败");
        }
    }
}
```

上面的方法都很简单，下来我们一个一个详细讲解：

- 第一个方法（encode）就是生成token，上面我们在荷载里面加入了用户名，你也可以增加自己的其他用户信息，但是不要放用户密码，因为荷载区任何人都可以解密，需要注意的是这个方法需要传一个字符串（secret），这个字符串也可以叫做密钥，你可以随意指定，但为了安全考虑，一般会统计将固定字符串，拼接上用户名，时间戳，然后加密（越复杂越好），这样也比较安全，当然你的secret要存好，不然你没法解密了😂，这也是我们用redis的原因，就是为了存用户的secret，键名用token加你自己特殊处理过的字符串（当然也是越复杂越好，前提是你能正确拿到，并正常校验）。

- 第二个方法（decode）是验证token，验证token是否合法，是否过期，在生成token的时候我们设置了一个过期时间，这个时间很重要，如果过期校验也是通不过的；这里就要用到我们前面生成token的密钥，没有密钥或者密钥不正确，解密肯定不通过。

- 第三个方法是从荷载区中拿到我们放进去的信息，我获取的是用户名，如果你生成的时候放了其他数据，你也可以获取其他数据。

其实，到这里jwt的知识点就完了，因为jwt提供的就是一套加密验证的机制，下来我们要解决的token的传输、secret的存储等问题和jwt没什么关系，这些问题取决于你的各种解决方案。我们先说下会有哪些问题：

- **token传输**：客户端请求的时候，每次请求接口的时候都必须携带token，如果是所有的接口、页面都是一个服务或者部署在同一个容器中，那没什么问题，但如果登陆的服务（单点登录）、接口服务、前端服务（前后端分离）都不是同一个服务器，你就需要解决token跨域传输。

- **token存储**：token登陆成功后是返回给客户端的，客户端如何存储token，是放在cookie、sessionStoreage，还是localStorage，如果登陆和当前服务有跨域问题的话，你还需要考虑如何跨域共享token。

- **secret存储问题**：这个是服务端要考虑的问题，本次示例是存在redis中，当然你如果有其他更好的解决方案，欢迎分享。

  上面这些问题，我会在后续详细讲解我的解决方案，这里就不过多赘述了，下来看看其他核心代码。

#### jwt服务类

```java
@Service
public class JwtService {
    private static Logger logger = LoggerFactory.getLogger(JwtService.class);
    // 过期时间30分钟
    public static final long EXPIRE_TIME = 30 * 60 * 1000;

    @Autowired
    private RedisUtil redisUtil;



    /**
     * Description:登录获取token
     *
     * @param user user
     * @return java.lang.String
     * @author sysker
     * @date 2019/3/4 18:45
     */
    public String login(User user) {
        //进行登录校验
        try {
            if (user.getUsername().equalsIgnoreCase(user.getPassword())) {
                return this.generateNewJwt(user.getUsername());
            } else {
                logger.info("账号密码错误:{}{}", user.getUsername(), user.getPassword());
                throw new AuthorizationException("账号密码错误");
            }
        } catch (Exception e) {
            logger.info("账号密码错误:{},{}", user.getUsername(), user.getPassword());
            throw new AuthorizationException(e, "账号密码错误");
        }
    }

    /**
     * 过期时间小于半小时，返回新的jwt，否则返回原jwt
     * @param jwt
     * @return
     */
    public String refreshJwt(String jwt) {
        String secret = (String)redisUtil.get(jwt);
        Map<String, Claim> map = JwtUtil.decode(jwt, secret);
        if(map.get("exp").asLong()*1000 - System.currentTimeMillis()/1000<30*60*1000){
            return this.generateNewJwt(map.get("name").asString());
        }else{
            return jwt;
        }
    }


    /**
     * Description: 生成新的jwt,并放入jwtMap中
     *
     * @return java.lang.String
     * @author sysker
     * date 2019/3/5 10:44
     */
    private String generateNewJwt(String username) {
        String data = SecretConstant.DATAKEY + username + UUIDUtil.getUUIDStr();
        logger.debug("创建密钥加密前data：", data);
        String secretEncrypted = null;
        try {
            secretEncrypted = Base64Util.encryptBase64(AESSecretUtil.encryptToStr(data,
                    SecretConstant.BASE64SECRET));
        } catch (Exception e) {
            logger.error("base64加密失败：", e);
            throw new AuthorizationException("未知错误");
        }
        logger.debug("密钥加密后data：", secretEncrypted);
        String token = JwtUtil.encode(username, secretEncrypted, EXPIRE_TIME);
        logger.debug("创建token:", token);
        redisUtil.set(CommonConstant.PREFIX_USER_TOKEN + token, secretEncrypted, EXPIRE_TIME);
        return token;
    }

    /**
     * Description:检查jwt有效性
     *
     * @return Boolean
     * @author sysker
     * @date 2019/3/4 18:47
     */
    public ReturnEntity checkJwt(String jwt) {
            String secret = (String)redisUtil.get(CommonConstant.PREFIX_USER_TOKEN + jwt);
            JwtUtil.decode(jwt, secret);
            return ReturnEntity.successResult(1, true);
    }

    /**
     * Description: 作废token，使该jwt失效
     *
     * @author sysker
     * @date 2019/3/4 19:58
     */
    public void inValid(String jwt) {
        redisUtil.del(jwt);
    }
```

上面用到的所有工具类，github示例中都有，服务中的这些方法基本都是调用jwt工具类中的方法，只是部分方法需要从redis中获取用户的secret，或者删除、更新用户的token。

#### 其他实现思路

##### 登陆拦截

登陆校验我是在拦截器中实现的，但是这里需要解决的问题是拦截器中的异常处理问题，如果直接抛出异常，前台收到的是500异常，因为filter早于spring，所以集中异常处理并不能捕获，查了很多资料后，最后增加一个异常过滤器，将异常转发至自己的controller，然后在controller中抛出，然后在自己写的TokenErrorController中集中处理：

jwt拦截器

```java
public class JwtFilter extends BasicHttpAuthenticationFilter {
    private final Logger logger = LoggerFactory.getLogger(JwtFilter.class);

    private AntPathMatcher antPathMatcher = new AntPathMatcher();

    /**
     * 执行登录认证(判断请求头是否带上token)
     *
     * @param request
     * @param response
     * @param mappedValue
     * @return
     */
    @Override
    protected boolean isAccessAllowed(ServletRequest request, ServletResponse response, Object mappedValue) {
        logger.info("JwtFilter-->>>isAccessAllowed-Method:init()");
        //如果请求头不存在token,则可能是执行登陆操作或是游客状态访问,直接返回true
        if (isLoginAttempt(request, response)) {
            return true;
        }
        //如果存在,则进入executeLogin方法执行登入,检查token 是否正确
        executeLogin(request, response);
        return true;
    }

    /**
     * 判断用户是否是登入,检测headers里是否包含token字段
     */
    @Override
    protected boolean isLoginAttempt(ServletRequest request, ServletResponse response) {
        logger.info("JwtFilter-->>>isLoginAttempt-Method:init()");
        HttpServletRequest req = (HttpServletRequest) request;
        if (antPathMatcher.match("/userLogin", req.getRequestURI())) {
            return true;
        }
        String token = req.getHeader(CommonConstant.ACCESS_TOKEN);
        if (StringUtils.isEmpty(token)) {
            return false;
        }
        JwtService jwtService = (JwtService) SpringContextUtil.getBean("jwtService");
        Boolean isPass = (jwtService.checkJwt(token).getCode() == 1);
        if (!isPass) {
            return false;
        }
        logger.info("JwtFilter-->>>isLoginAttempt-Method:返回true");
        return true;
    }

    /**
     * 重写AuthenticatingFilter的executeLogin方法丶执行登陆操作
     */
    @Override
    protected boolean executeLogin(ServletRequest request, ServletResponse response) {
        logger.info("JwtFilter-->>>executeLogin-Method:init()");
        String token = getTokenFromRequest((HttpServletRequest) request);
        if (StringUtils.isEmpty(token)) {
            throw new AuthorizationException("未找到用户token令牌信息，请登陆");
        }
        JwtToken jwtToken = new JwtToken(token);
        // 提交给realm进行登入,如果错误他会抛出异常并被捕获, 反之则代表登入成功,返回true
        getSubject(request, response).login(jwtToken);
        return true;
    }

    /**
     * 从request头中获取token
     *
     * @param request
     * @return
     */
    private String getTokenFromRequest(HttpServletRequest request) {
        HttpServletRequest httpServletRequest = request;
        return httpServletRequest.getHeader(CommonConstant.ACCESS_TOKEN);
    }

    /**
     * 对跨域提供支持
     */
    @Override
    protected boolean preHandle(ServletRequest request, ServletResponse response) throws Exception {
        logger.info("JwtFilter-->>>preHandle-Method:init()");
        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        HttpServletResponse httpServletResponse = (HttpServletResponse) response;
        httpServletResponse.setHeader("Access-control-Allow-Origin", httpServletRequest.getHeader("Origin"));
        httpServletResponse.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE");
        httpServletResponse.setHeader("Access-Control-Allow-Headers", httpServletRequest.getHeader("Access-Control-Request-Headers"));
        // 跨域时会首先发送一个option请求，这里我们给option请求直接返回正常状态
        if (httpServletRequest.getMethod().equals(RequestMethod.OPTIONS.name())) {
            httpServletResponse.setStatus(HttpStatus.OK.value());
            return false;
        }
        return super.preHandle(request, response);
    }
}
```

因为我用了shiro，所以我把jwtFilter配置在shiro里面了，当然你要可以单独配置。对于单点登陆而言，目前我觉得shiro没发挥他该有的作用。下面贴出shiro配置类：

```java
@Configuration
public class ShiroConfig {

    @Bean("securityManager")
    public DefaultWebSecurityManager getManager(JwtShiroRealm jwtShiroRealm) {
        DefaultWebSecurityManager manager = new DefaultWebSecurityManager();
        // 使用自己的realm
        manager.setRealm(jwtShiroRealm);

        /*
         * 关闭shiro自带的session，详情见文档
         * http://shiro.apache.org/session-management.html#SessionManagement-StatelessApplications%28Sessionless%29
         */
        DefaultSubjectDAO subjectDAO = new DefaultSubjectDAO();
        DefaultSessionStorageEvaluator defaultSessionStorageEvaluator = new DefaultSessionStorageEvaluator();
        defaultSessionStorageEvaluator.setSessionStorageEnabled(false);
        subjectDAO.setSessionStorageEvaluator(defaultSessionStorageEvaluator);
        manager.setSubjectDAO(subjectDAO);

        return manager;
    }

    @Bean("shiroFilter")
    public ShiroFilterFactoryBean factory(DefaultWebSecurityManager securityManager) {
        ShiroFilterFactoryBean factoryBean = new ShiroFilterFactoryBean();

        factoryBean.setSecurityManager(securityManager);     //设置安全管理器
        factoryBean.setLoginUrl("/userLogin");//     如果不设置默认会自动寻找Web工程根目录下的"/login.jsp"页面
        factoryBean.setSuccessUrl("/index"); //  登录成功后要跳转的链接
        factoryBean.setUnauthorizedUrl("/401");//未授权界面;
        // 添加自己的过滤器并且取名为jwt
        Map<String, Filter> filterMap = new HashMap<>();
        filterMap.put("jwt", new JwtFilter());
        factoryBean.setFilters(filterMap);


        /*
         * 自定义url规则
         * http://shiro.apache.org/web.html#urls-
         */
        Map<String, String> filterRuleMap = new LinkedHashMap<>();
        // 访问401和404页面不通过我们的Filter
        filterRuleMap.put("/401", "anon");
        filterRuleMap.put("/static/**", "anon");
        filterRuleMap.put("/css/**","anon");
        filterRuleMap.put("/layui/**","anon");
        filterRuleMap.put("/img/**","anon");
        filterRuleMap.put("/js/**","anon");
        filterRuleMap.put("/index","anon");
        filterRuleMap.put("/login","anon");
        filterRuleMap.put("/","anon");
        filterRuleMap.put("/userLogin","anon");
        filterRuleMap.put("/logout","logout");//配置退出 过滤器,其中的具体的退出代码Shiro已经实现
        filterRuleMap.put("/**","authc");//过滤链定义，从上向下顺序执行，一般将/**放在最为下边
        // 所有请求通过我们自己的JWT Filter
        filterRuleMap.put("/**", "jwt");

        factoryBean.setFilterChainDefinitionMap(filterRuleMap);
        return factoryBean;
    }

    /**
     * 下面的代码是添加注解支持
     */
    @Bean
    @DependsOn("lifecycleBeanPostProcessor")
    public DefaultAdvisorAutoProxyCreator defaultAdvisorAutoProxyCreator() {
        DefaultAdvisorAutoProxyCreator defaultAdvisorAutoProxyCreator = new DefaultAdvisorAutoProxyCreator();
        // 强制使用cglib，防止重复代理和可能引起代理出错的问题
        // https://zhuanlan.zhihu.com/p/29161098
        defaultAdvisorAutoProxyCreator.setProxyTargetClass(true);
        return defaultAdvisorAutoProxyCreator;
    }

    @Bean
    public LifecycleBeanPostProcessor lifecycleBeanPostProcessor() {
        return new LifecycleBeanPostProcessor();
    }

    @Bean
    public AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor(DefaultWebSecurityManager securityManager) {
        AuthorizationAttributeSourceAdvisor advisor = new AuthorizationAttributeSourceAdvisor();
        advisor.setSecurityManager(securityManager);
        return advisor;
    }
}
```

异常拦截器：

```java
@Component
public class ExceptionFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        try {
            chain.doFilter(request, response);
        } catch (Exception e) {
            Throwable eCause = e.getCause();
            // 异常捕获，发送到error controller
            request.setAttribute("filter.error", eCause);
            //将异常分发到/error/exthrow控制器
            request.getRequestDispatcher("/error/exthrow").forward(request, response);
        }
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void destroy() {

    }
}
```

这里要注意的是，`setAttribute("filter.error", e)`的时候，为了能区分是哪种异常，这里要区分判断异常的类型，如果不处理的话，默认是`javax.servlet.ServletException`异常，我是通过`e.getCause()`来获取引起异常的类型，也就是我在拦截器中抛出的异常。

异常拦截器配置：

```java
@Configuration
public class WebFilterConfig {
    @Bean
    public FilterRegistrationBean exceptionFilterRegistration() {
        FilterRegistrationBean registration = new FilterRegistrationBean();
        registration.setFilter(new ExceptionFilter());
        registration.setName("exceptionFilter");
        //此处尽量小，要比其他Filter靠前
        registration.setOrder(-1);
        return registration;
    }
}
```

异常controller:

```java
@Controller
public class ExceptionController {

    @RequestMapping("/error/exthrow")
    public void rethrow(HttpServletRequest request) throws Exception {
        throw ((Exception) request.getAttribute("filter.error"));

    }
}
```

controller集中异常处理，但一直没起作用，就算我把错误转发到controller，最后也没进到这里，这个问题有时间了再研究下：

```java
@RestController
public class TokenErrorController extends BasicErrorController {

    public TokenErrorController(ErrorAttributes errorAttributes) {
        super(errorAttributes, new ErrorProperties());
    }

    @Override
    @RequestMapping(produces = {MediaType.APPLICATION_JSON_VALUE})
    public ResponseEntity<Map<String, Object>> error(HttpServletRequest request) {
        return new ResponseEntity<>(ReturnEntity.failedResultMap(1, "未知错误"), HttpStatus.OK);
    }

}
```

还写了个ExceptionHandle，但是没有拦截器之前不起作用，增加了异常拦截器以后就正常了：

```java
@RestControllerAdvice
public class ExceptionHandle extends ResponseEntityExceptionHandler {
    private Logger logger = LoggerFactory.getLogger(ExceptionHandle.class);

    @ExceptionHandler(Exception.class)
    public ReturnEntity handleException(Exception e) {
        logger.warn("错误信息:", e);
        if (e instanceof AuthorizationException) {
            return ReturnEntity.failedResult(1, "未知错误");
        } else {
            return ReturnEntity.failedResult(2, "未知错误");
        }
    }
}
```

其实还有很多内容需要分享，但是由于篇幅问题，今天就到这里吧，最后提一点，因为filter早于spring，所以spring管理的组件，你在filter你是拿不到的，所以你要通过springContextUtil来获取组件的实例：

```java
public class SpringContextUtil {

    private static ApplicationContext applicationContext;

    //获取上下文
    public static ApplicationContext getApplicationContext() {
        return applicationContext;
    }

    //设置上下文
    public static void setApplicationContext(ApplicationContext applicationContext) {
        SpringContextUtil.applicationContext = applicationContext;
    }

    //通过名字获取上下文中的bean
    public static Object getBean(String name){
        return applicationContext.getBean(name);
    }

    //通过类型获取上下文中的bean
    public static Object getBean(Class<?> requiredType){
        return applicationContext.getBean(requiredType);
    }

}
```

由于篇幅问题，这里就不贴出太多代码了，想详细了解的小伙伴直接去github查看完整示例：https://github.com/Syske/learning-dome-code/tree/master/springboot-jwt-demo

