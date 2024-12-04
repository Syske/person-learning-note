### 常用注解

#### 1.Configuration 和 Bean

该@Configuration注释向Spring表明该类是一个配置类，它将为Spring应用程序上下文提供bean。配置类的方法被注释，@Bean指示它们返回的对象应该作为bean添加到应用程序上下文中（默认情况下，它们各自的bean ID将与定义它们的方法的名称相同）。

```
@Configuration
public class ServiceConfiguration {
  @Bean
  public InventoryService inventoryService() {
    return new InventoryService();
  }

  @Bean
  public ProductService productService() {
    return new ProductService(inventoryService());
  }
}
```
和XML中如下配置等价：
```
<bean id="inventoryService"
      class="com.example.InventoryService" />

<bean id="productService"
      class="com.example.ProductService" />
  <constructor-arg ref="inventoryService" />
</bean>
```
