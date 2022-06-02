tags: [#ireport]

#### 前言

上周我们探讨了如何用IReport设计PDF报表，我们了解了IReport报表的设计流程，也学会了如何构建多数据集报表，本周我们来探讨下如何在我们的项目中使用我们设计的报表。

#### 创建项目，编写业务代码

首先我们要先创建web项目，我创建的servlet/jsp项目，具体pom文件如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>io.github.syske</groupId>
    <artifactId>ireport-use-in-web</artifactId>
    <version>1.0-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>servlet-api</artifactId>
            <version>2.5</version>
        </dependency>
        <dependency>
            <groupId>net.sf.jasperreports</groupId>
            <artifactId>jasperreports</artifactId>
            <version>5.6.0</version>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.16</version>
        </dependency>
        <dependency>
            <groupId>com.lowagie</groupId>
            <artifactId>itextasian</artifactId>
            <version>1.0</version>
        </dependency>
    </dependencies>

</project>
```

编辑web.xml:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <servlet>
        <servlet-name>IreportServlet</servlet-name>
        <servlet-class>io.github.syske.servlet.IreportServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>IreportServlet</servlet-name>
        <url-pattern>/ireport</url-pattern>
    </servlet-mapping>
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
</web-app>
```

编写数据库连接工具：

```java
package io.github.syske.db;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * @program: ireportuseinweb
 * @description:
 * @author: syske
 * @create: 2019-12-28 12:04
 */
public class DBHelper {

    private static String driver = "com.mysql.jdbc.Driver";   //数据库驱动
    //连接数据库的URL地址
    private static final String url = "jdbc:mysql://localhost:3307/test?serverTimezone=Asia/Shanghai";
    private static final String usename = "root";
    private static final String password = "root"; //数据库密码

    private static Connection connection =null;
    //静态代码块负责加载驱动
    static{//静态块中的代码会优先被执行
        try {
            Class.forName(driver);
        } catch (ClassNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    //单例模式返回数据库连接对象
    public static Connection getConnection(){
        if(connection==null){
            try {
                connection = DriverManager.getConnection(url,usename,password);
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            return connection;
        }
        return connection;
    }
    public static void main(String[] args) {
        ResultSet resultSet = null;
        try{
            Connection connection = DBHelper.getConnection();
            Statement statement =  connection.createStatement();
            resultSet = statement.executeQuery("SELECT * FROM goods;");
            while(resultSet.next()){
                System.out.println(resultSet.getString("name"));
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
```

编写servlet：

```java
package io.github.syske.servlet;

import io.github.syske.db.DBHelper;
import io.github.syske.util.IReportUtil;
import net.sf.jasperreports.engine.JRException;

import javax.servlet.ServletContext;
import java.io.IOException;
import java.sql.Connection;
import java.util.HashMap;
import java.util.Map;

public class IreportServlet extends javax.servlet.http.HttpServlet {
    protected void doPost(javax.servlet.http.HttpServletRequest request,
                          javax.servlet.http.HttpServletResponse response) throws javax.servlet.ServletException, IOException {

    }

    protected void doGet(javax.servlet.http.HttpServletRequest request,
                         javax.servlet.http.HttpServletResponse response) throws javax.servlet.ServletException, IOException {
        Map<String, Object> parameters = new HashMap<String, Object>();
        Connection connection = DBHelper.getConnection();
        parameters.put("username", request.getParameter("username"));
        try {
            ServletContext context = request.getSession().getServletContext();

            String sourceFileName = context.getRealPath("ireport/"
                    + "ireport-demo.jasper");
            IReportUtil.exportPdfFileServer(sourceFileName, "D:/test.pdf",parameters, connection);
        } catch (JRException e) {
            e.printStackTrace();
        }
    }
}
```

然后编写我们IReport的工具类：

```java
package io.github.syske.util;

import net.sf.jasperreports.engine.JRException;
import net.sf.jasperreports.engine.JasperRunManager;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.Connection;
import java.util.Map;
import java.util.UUID;

/**
 * @program: ireportuseinweb
 * @description:
 * @author: syske
 * @create: 2019-12-28 11:17
 */
public class IReportUtil {

    /**
     * IReport报表生成pdf
     *
     * @param reprotfileName 报表文件名称
     * @param exportFileName pdf保存完整路径，包含文件名及后缀
     * @param parameters     报表入参参数集
     * @param connection     数据库连接
     * @return
     * @throws IOException
     * @throws JRException
     */
    public static String exportPdfFileServer(
            String reprotfileName, String exportFileName,
            Map<String, Object> parameters, Connection connection)
            throws IOException, JRException {

        String sourceFileName = reprotfileName;
        // 根据文件创建文件的输出流
        JasperRunManager.runReportToPdfFile(sourceFileName, exportFileName,
                parameters, connection);
        return exportFileName;

    }

    /**
     * IReport报表生成pdfStream
     *
     * @param reprotfileName 报表文件名称
     * @param parameters     报表入参参数集
     * @param connection     数据库连接
     * @return
     * @throws IOException
     * @throws JRException
     */
    public static FileOutputStream exportPdfFileServer(String reprotfileName,
            Map<String, Object> parameters, Connection connection)
            throws IOException, JRException {

        FileInputStream sourceFileInputStream = new FileInputStream(
                 reprotfileName);
        String exportFileName = UUID.randomUUID().toString() + ".pdf";
        FileOutputStream exportFileOutputStream = new FileOutputStream(
                exportFileName);
        // 根据文件创建文件的输出流
        JasperRunManager.runReportToPdfStream(sourceFileInputStream,
                exportFileOutputStream, parameters, connection);
        return exportFileOutputStream;

    }

}
```

导入报表的编译文件，也就是.jasper结尾的文件，下面是今天演示报表的源文件(.jrxml)：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport xmlns="http://jasperreports.sourceforge.net/jasperreports" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports http://jasperreports.sourceforge.net/xsd/jasperreport.xsd" name="ireport-demo" pageWidth="595" pageHeight="842" columnWidth="555" leftMargin="20" rightMargin="20" topMargin="20" bottomMargin="20" uuid="b3d5e4e1-d3f8-446d-952d-724571f940fb">
	<property name="ireport.zoom" value="1.2100000000000006"/>
	<property name="ireport.x" value="0"/>
	<property name="ireport.y" value="0"/>
	<subDataset name="test" uuid="3234304e-333d-4afa-87f3-890e416942ad">
		<queryString>
			<![CDATA[select count(*) count from user]]>
		</queryString>
		<field name="count" class="java.lang.Long"/>
	</subDataset>
	<parameter name="username" class="java.lang.String">
		<defaultValueExpression><![CDATA[$P{username}]]></defaultValueExpression>
	</parameter>
	<queryString>
		<![CDATA[select username,age,salary from user
where username=$P{username}]]>
	</queryString>
	<field name="username" class="java.lang.String">
		<fieldDescription><![CDATA[]]></fieldDescription>
	</field>
	<field name="age" class="java.lang.Integer">
		<fieldDescription><![CDATA[]]></fieldDescription>
	</field>
	<field name="salary" class="java.lang.Float">
		<fieldDescription><![CDATA[]]></fieldDescription>
	</field>
	<variable name="age_sum" class="java.lang.Integer" calculation="Sum">
		<variableExpression><![CDATA[$F{age}]]></variableExpression>
	</variable>
	<variable name="salary_sum" class="java.lang.Double" calculation="Sum">
		<variableExpression><![CDATA[$F{salary}]]></variableExpression>
	</variable>
	<background>
		<band splitType="Stretch"/>
	</background>
	<title>
		<band height="79" splitType="Stretch">
			<staticText>
				<reportElement x="0" y="37" width="555" height="42" uuid="d75420a9-d1af-4f0f-8fec-97ae35f49159"/>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font fontName="宋体" size="24" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[IReport测试]]></text>
			</staticText>
		</band>
	</title>
	<pageHeader>
		<band height="35" splitType="Stretch">
			<staticText>
				<reportElement x="0" y="0" width="555" height="34" uuid="89ebed96-9d55-48e8-b083-199c0686fd6f"/>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[我是页眉]]></text>
			</staticText>
		</band>
	</pageHeader>
	<columnHeader>
		<band height="31" splitType="Stretch">
			<staticText>
				<reportElement x="71" y="0" width="137" height="31" uuid="133aed5c-0d6a-4c06-aa47-e19ca168ecba"/>
				<box>
					<topPen lineWidth="0.75"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[用户名]]></text>
			</staticText>
			<staticText>
				<reportElement x="208" y="0" width="137" height="31" uuid="2f6c838c-0c4e-4f45-86e7-ccf1c850bb0f"/>
				<box>
					<topPen lineWidth="0.75"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[年龄]]></text>
			</staticText>
			<staticText>
				<reportElement x="345" y="0" width="137" height="31" uuid="bc8fa3d4-9683-49e0-8cd0-80eb9a30b5c1"/>
				<box>
					<topPen lineWidth="0.75"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
					<rightPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[薪资]]></text>
			</staticText>
		</band>
	</columnHeader>
	<detail>
		<band height="28" splitType="Stretch">
			<textField>
				<reportElement x="71" y="0" width="137" height="27" uuid="c7b969ee-07b5-446d-b5b6-3863ecfc0371"/>
				<box>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<textFieldExpression><![CDATA[$F{username}]]></textFieldExpression>
			</textField>
			<textField>
				<reportElement x="208" y="0" width="137" height="27" uuid="f2c06cb4-4894-4c9c-b654-11de56e73426"/>
				<box>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<textFieldExpression><![CDATA[$F{age}]]></textFieldExpression>
			</textField>
			<textField>
				<reportElement x="345" y="0" width="137" height="27" uuid="07e927e8-f179-4deb-8a7d-b736c68d5f8d"/>
				<box>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
					<rightPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<textFieldExpression><![CDATA[$F{salary}]]></textFieldExpression>
			</textField>
		</band>
	</detail>
	<columnFooter>
		<band height="45" splitType="Stretch">
			<staticText>
				<reportElement x="211" y="15" width="100" height="20" uuid="caf39b65-a514-4caa-a9b7-d62bf84e6a70"/>
				<textElement textAlignment="Center">
					<font fontName="宋体" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[column footer]]></text>
			</staticText>
		</band>
	</columnFooter>
	<pageFooter>
		<band height="54" splitType="Stretch">
			<componentElement>
				<reportElement x="0" y="0" width="555" height="54" uuid="e8c621d6-d885-443c-815e-df7bf7b08e7f"/>
				<jr:list xmlns:jr="http://jasperreports.sourceforge.net/jasperreports/components" xsi:schemaLocation="http://jasperreports.sourceforge.net/jasperreports/components http://jasperreports.sourceforge.net/xsd/components.xsd" printOrder="Vertical">
					<datasetRun subDataset="test" uuid="5dab7dc4-f964-4bec-a700-dc9cd8473d3a">
						<connectionExpression><![CDATA[$P{REPORT_CONNECTION}]]></connectionExpression>
					</datasetRun>
					<jr:listContents height="54" width="555">
						<staticText>
							<reportElement x="14" y="14" width="131" height="20" uuid="42ac7b35-c6d9-4159-adf9-86e646c9bd04"/>
							<textElement textAlignment="Center" verticalAlignment="Middle">
								<font pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H"/>
							</textElement>
							<text><![CDATA[多数据集测试-汇总人数：]]></text>
						</staticText>
						<textField>
							<reportElement x="160" y="14" width="100" height="20" uuid="ed58dfe5-904b-4657-aa1a-aa59aef2b05c"/>
							<textElement textAlignment="Center" verticalAlignment="Middle"/>
							<textFieldExpression><![CDATA[$F{count}]]></textFieldExpression>
						</textField>
					</jr:listContents>
				</jr:list>
			</componentElement>
		</band>
	</pageFooter>
	<summary>
		<band height="42" splitType="Stretch">
			<textField>
				<reportElement x="208" y="0" width="137" height="42" uuid="b6171b32-2c50-49e3-98aa-d742d2f68421"/>
				<box>
					<topPen lineWidth="0.0"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<textFieldExpression><![CDATA[$V{age_sum}]]></textFieldExpression>
			</textField>
			<staticText>
				<reportElement x="71" y="0" width="137" height="42" uuid="0a7d649d-ef2d-47ed-9b72-657c8955d452"/>
				<box>
					<topPen lineWidth="0.0"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" isBold="true" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<text><![CDATA[汇总]]></text>
			</staticText>
			<textField pattern="###0.00;-###0.00">
				<reportElement x="345" y="0" width="137" height="42" uuid="3859ce87-c7d9-44dc-b35b-341c8c2a4cd2"/>
				<box>
					<topPen lineWidth="0.0"/>
					<leftPen lineWidth="0.75"/>
					<bottomPen lineWidth="0.75"/>
					<rightPen lineWidth="0.75"/>
				</box>
				<textElement textAlignment="Center" verticalAlignment="Middle">
					<font size="14" pdfFontName="STSong-Light" pdfEncoding="UniGB-UCS2-H" isPdfEmbedded="true"/>
				</textElement>
				<textFieldExpression><![CDATA[$V{salary_sum}]]></textFieldExpression>
			</textField>
		</band>
	</summary>
</jasperReport>
```

编写jsp文件：

```jsp
<%--
  Created by IntelliJ IDEA.
  User: syske
  Date: 2019-12-28
  Time: 12:11
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>IReport Test</title>
</head>
<body>

<form action="/ireport"method="get">
    用户名：<input name="username" type="text"><br>
    <input type="submit" name="导出">
</form>

</body>
</html>
```

项目结构如下：

![](
https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/images/image-20191228132908308.png)

##### 总结

今天的项目总体来说没有什么难度，核心部分就是工具类，但还是有几个问题需要注意：

**第一、**IReport默认的语言是groovy，xml格式报表文件jasperReport标签有个language属性，默认是groovy（language="groovy"），所以在你发布项目时需要在lib下加入groovy-all-2.0.1.jar，和版本应该关系不大，不然会提示找不到class的错误：

```cmake
java.lang.NoClassDefFoundError: org/codehaus/groovy/control/CompilationFailedException
	java.lang.Class.getDeclaredConstructors0(Native Method)
	java.lang.Class.privateGetDeclaredConstructors(Class.java:2671)
	java.lang.Class.getConstructor0(Class.java:3075)
	java.lang.Class.getConstructor(Class.java:1825)
	net.sf.jasperreports.engine.JasperCompileManager.getCompiler(JasperCompileManager.java:814)
	net.sf.jasperreports.engine.JasperCompileManager.getEvaluator(JasperCompileManager.java:377)
	net.sf.jasperreports.engine.fill.JRFillDataset.createCalculator(JRFillDataset.java:462)
	net.sf.jasperreports.engine.fill.JRBaseFiller.<init>(JRBaseFiller.java:405)
	net.sf.jasperreports.engine.fill.JRVerticalFiller.<init>(JRVerticalFiller.java:89)
	net.sf.jasperreports.engine.fill.JRVerticalFiller.<init>(JRVerticalFiller.java:104)
	net.sf.jasperreports.engine.fill.JRVerticalFiller.<init>(JRVerticalFiller.java:62)
	net.sf.jasperreports.engine.fill.JRFiller.createFiller(JRFiller.java:179)
	net.sf.jasperreports.engine.fill.JRFiller.fill(JRFiller.java:81)
	net.sf.jasperreports.engine.JasperFillManager.fill(JasperFillManager.java:457)
	net.sf.jasperreports.engine.JasperFillManager.fill(JasperFillManager.java:418)
	net.sf.jasperreports.engine.JasperRunManager.runToPdfStream(JasperRunManager.java:210)
	net.sf.jasperreports.engine.JasperRunManager.runReportToPdfStream(JasperRunManager.java:729)
	io.github.syske.util.IReportUtil.exportPdfFileServer(IReportUtil.java:65)
	io.github.syske.servlet.IreportServlet.doGet(IreportServlet.java:29)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:624)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:731)
	org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52
```

还有一种解决方法是将该属性值改为java，但我发下修改保存后，该属性不见了，可能删除掉该属性也可以。以上两种方法都测试过，没有问题。

**第二、**只要你的报表中有中文或者你有将pdf Font name这个属性改成STSong-Light，那么你就要在lib下加入iTextAsian.jar，而且版本不要太高，太高包名可能发生变化，否则会报如下错误：

```cmake
net.sf.jasperreports.engine.JRRuntimeException: Could not load the following font : 
pdfFontName   : STSong-Light
pdfEncoding   : UniGB-UCS2-H
isPdfEmbedded : true
	net.sf.jasperreports.engine.export.JRPdfExporter.getFont(JRPdfExporter.java:2116)
	net.sf.jasperreports.engine.export.JRPdfExporter.getChunk(JRPdfExporter.java:1906)
	net.sf.jasperreports.engine.export.JRPdfExporter.getPhrase(JRPdfExporter.java:1875)
	net.sf.jasperreports.engine.export.SimplePdfTextRenderer.getPhrase(SimplePdfTextRenderer.java:89)
	net.sf.jasperreports.engine.export.SimplePdfTextRenderer.render(SimplePdfTextRenderer.java:99)
	net.sf.jasperreports.engine.export.JRPdfExporter.exportText(JRPdfExporter.java:2238)
	net.sf.jasperreports.engine.export.JRPdfExporter.exportElements(JRPdfExporter.java:950)
	net.sf.jasperreports.engine.export.JRPdfExporter.exportPage(JRPdfExporter.java:909)
	net.sf.jasperreports.engine.export.JRPdfExporter.exportReportToStream(JRPdfExporter.java:786)
	net.sf.jasperreports.engine.export.JRPdfExporter.exportReport(JRPdfExporter.java:513)
	net.sf.jasperreports.engine.JasperExportManager.exportToPdfStream(JasperExportManager.java:198)
	net.sf.jasperreports.engine.JasperRunManager.runToPdfStream(JasperRunManager.java:212)
	net.sf.jasperreports.engine.JasperRunManager.runReportToPdfStream(JasperRunManager.java:729)
	io.github.syske.util.IReportUtil.exportPdfFileServer(IReportUtil.java:65)
	io.github.syske.servlet.IreportServlet.doGet(IreportServlet.java:29)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:624)
	javax.servlet.http.HttpServlet.service(HttpServlet.java:731)
	org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:52)
```

[注]: 以上项目源码均可在Syske/learning-dome-code（github）找到	"（https://github.com/Syske/learning-dome-code）"

注 以上项目源码均可在Syske/learning-dome-code（github）找到 （https://github.com/Syske/learning-dome-code）

[注]: https://github.com/Syske/learning-dome-code	"注 以上项目源码均可在Syske/learning-dome-code"

