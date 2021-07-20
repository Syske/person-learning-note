# spring-boot启用security组件

### 前言



### Security组件

#### 创建项目

```xml
<dependency>
     <groupId>org.springframework.boot</groupId>
     <artifactId>spring-boot-starter</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>30.1.1-jre</version>
    <!-- or, for Android: -->
    <!--<version>30.1.1-android</version>-->
</dependency>
```

#### 测试

```java
@RestController
@RequestMapping("/test")
public class TestController {

    @GetMapping("security")
    public Object testSecurity(String name) {
        return "hello, " + name;

    }
}
```



![](https://gitee.com/sysker/picBed/raw/master/20210720085510.png)

#### 配置security

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    private Logger logger = LoggerFactory.getLogger(SecurityConfig.class);
    @Autowired
    private ReaderRepository readerRepository;

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(username -> {
            System.out.println(username);
            return readerRepository.loadUserByUsername("admin");
                    }).passwordEncoder(new BCryptPasswordEncoder());
    }
}
```



```java
@Service
public class ReaderRepository implements UserDetailsService {
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        if ("admin".equals(username)) {
            return new UserInfo("admin", new BCryptPasswordEncoder()
                    .encode("admin"));
        } else {
            return null;
        }
    }

    public static class UserInfo implements UserDetails {
        private String username;
        private String password;

        public UserInfo(String username, String password) {
            this.username = username;
            this.password = password;
        }

        @Override
        public Collection<? extends GrantedAuthority> getAuthorities() {
            return Arrays.asList(new SimpleGrantedAuthority("READER"));
        }

        @Override
        public String getPassword() {
            return this.password;
        }

        @Override
        public String getUsername() {
            return this.username;
        }

        @Override
        public boolean isAccountNonExpired() {
            return true;
        }

        @Override
        public boolean isAccountNonLocked() {
            return true;
        }

        @Override
        public boolean isCredentialsNonExpired() {
            return true;
        }

        @Override
        public boolean isEnabled() {
            return true;
        }
    }
}
```



### 总结