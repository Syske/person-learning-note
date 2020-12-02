#### 1、导包
- Spring
- commons-fileupload
- commons-io

#### 2、项目配置web.xml

- 配置文件没有什么特别之处

```
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" id="WebApp_ID" version="3.0">
  <display-name>uploadmvc</display-name>
  <welcome-file-list>
    <welcome-file>index.html</welcome-file>
    <welcome-file>index.htm</welcome-file>
    <welcome-file>index.jsp</welcome-file>
    <welcome-file>default.html</welcome-file>
    <welcome-file>default.htm</welcome-file>
    <welcome-file>default.jsp</welcome-file>
  </welcome-file-list>
  <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:spring-servlet.xml</param-value>
    </context-param>

    <servlet>
        <servlet-name>springServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value></param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>springServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

#### 3、DispatcherServlet配置

```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.1.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-4.1.xsd">                    

    <!-- scan the package and the sub package -->
    <context:component-scan base-package="com.sysker"/>

    <!-- don't handle the static resource -->
    <mvc:default-servlet-handler />

    <!-- if you use annotation you must configure following setting -->
    <mvc:annotation-driven />
    <!-- 文件上传解析器 -->
    <bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    	<!-- 文件总大小 -->
    	<property name="maxUploadSize" value="500000"></property>
    	<!-- 单个文件总大小 -->
    	<property name="maxUploadSizePerFile" value="500000"></property>
    	<!-- 编码方式 -->
    	<property name="defaultEncoding" value="utf-8"></property>
    </bean>
    <!-- configure the InternalResourceViewResolver -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver" 
            id="internalResourceViewResolver">
        <!-- 前缀 -->
        <property name="prefix" value="/WEB-INF/view/" />
        <!-- 后缀 -->
        <property name="suffix" value=".jsp" />
    </bean>
</beans>
```

- 在该配置文件中需要配置文件上传的解析器

```
 <!-- 文件上传解析器 -->
    <bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
    	<!-- 文件总大小 -->
    	<property name="maxUploadSize" value="500000"></property>
    	<!-- 单个文件总大小 -->
    	<property name="maxUploadSizePerFile" value="500000"></property>
    	<!-- 编码方式 -->
    	<property name="defaultEncoding" value="utf-8"></property>
    </bean>
```

#### 4、创建Controller

```
package com.sysker.util;

import java.io.File;

import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class UploadAndDownloadController {

    @RequestMapping(value = "/")
    public String index() {
        return "index";
    }

    /**
     * 单个文件上传
     * 
     * @param uploadFile
     * @param session
     * @return
     * @throws Exception
     */
    @RequestMapping(value = "/upload")
    public String doUpload(MultipartFile uploadFile, HttpSession session)
            throws Exception {
        String fileName = uploadFile.getOriginalFilename();

        String leftPath = session.getServletContext().getRealPath("/images");

        File file = new File(leftPath, fileName);
        uploadFile.transferTo(file);
        return "welcome";

    }

    /**
     * 限制文件上传格式
     * 
     * @param uploadFile
     * @param session
     * @return
     * @throws Exception
     */
    @RequestMapping(value = "/uploadlim")
    public String doUploadLim(MultipartFile uploadFile, HttpSession session)
            throws Exception {
        if (uploadFile.getSize() > 0) {
            String fileName = uploadFile.getOriginalFilename();
            if (fileName.endsWith("jpg") || fileName.endsWith("gif")
                    || fileName.endsWith("png")) {
                String leftPath = session.getServletContext()
                        .getRealPath("/images");
                File file = new File(leftPath, fileName);
                uploadFile.transferTo(file);

            } else {
                return "error";
            }
        } else {
            return "error";
        }

        return "welcome";

    }

    /**
     * 多文件上传
     * 
     * @param uploadFile
     * @param session
     * @return
     * @throws Exception
     */
    @RequestMapping(value = "/uploadmany")
    public String doUploadMany(@RequestParam MultipartFile[] uploadFile,
            HttpSession session) throws Exception {
        for (MultipartFile multipartFile : uploadFile) {
            String fileName = multipartFile.getOriginalFilename();
            if (fileName.endsWith("jpg") || fileName.endsWith("gif")
                    || fileName.endsWith("png")) {

                String leftPath = session.getServletContext()
                        .getRealPath("/images");

                File file = new File(leftPath, fileName);

                multipartFile.transferTo(file);

            } else {
                return "error";
            }
        }

        return "welcome";

    }
}


```

- 这里需要注意的是代码中指定的的文件夹要手动创建，比如在我的代码中指定的路径为/images，那么我就必须在WebRoot下创建该目录，否则会抛出异常：

```
java.io.FileNotFoundException: D:\tools\eclipse-jee-oxygen-3a-win32-x86_64\eclipse-workspace\uploadmvc\WebContent\images
\58ba68439f0ea21d2ec37ffbe25f9e73.jpg (系统找不到指定的路径。)
```


- jsp页面：

```
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Insert title here</title>
</head>
<body>
 <form action="${pageContext.request.contextPath }/upload" method="post" enctype="multipart/form-data">
   <h2>文件上传</h2>
                文件:<input type="file" name="uploadFile"/><br/><br/>
      <input type="submit" value="上传"/>
   </form>
   
   <form action="${pageContext.request.contextPath }/uploadlim" method="post" enctype="multipart/form-data">
   <h2>文件上传：限定文件格式</h2>
                文件:<input type="file" name="uploadFile "/><br/><br/>
      <input type="submit" value="上传"/>
   </form>
   
   <form action="${pageContext.request.contextPath }/uploadmany" method="post" enctype="multipart/form-data">
   <h2>文件上传：多文件限定文件格式</h2>
                文件1:<input type="file" name="uploadFile "/><br/><br/>
                文件2:<input type="file" name="uploadFile "/><br/><br/>
                文件3:<input type="file" name="uploadFile "/><br/><br/>
      <input type="submit" value="上传"/>
   </form>
</body>
</html>
```