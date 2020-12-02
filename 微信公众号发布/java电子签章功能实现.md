# java电子签章实现

##### 项目源码路径:https://github.com/Syske/learning-dome-code.git

#### 前言

最近应客户需求，需要实现电子签章功能，公章部分用的时金格科技的接口，个人人签字需要自己实现，公章部分我们就不说了，商业接口做的都比较成熟，也有示例代码，所以今天着重说的就是个人签字部分。

参照公章部分的实现方式，同时也参考了很多博客[1]，查了很多资料，也搞清楚了电子签章的基本流程：

![image-20200104084727316](..\images\image-20200104084727316.png)

因为我要实现的功能很简单就是个人签章，而且我的签名是手写的，所以创建签名部分就省略了，核心部分就是确定签名坐标和签名，确定坐标部分我根据自己查找的资料，实现了根据关键字确定坐标，因为确定坐标很麻烦，也不够灵活。

对于创建签名我有一个思路，可以将创建签名作为一个远程服务部署，然后远程调用，然后检验，返回签名；当然你也可以通过这种方式生成公章，但是因为没有经过公正机构认证，这种方式生成的公章其实是不具法律效应的，好了下面直接上代码吧。

#### 创建签名密钥

这个密钥在pdf签名的时候会校验

```java
package io.github.syske.common.util;

import org.bouncycastle.asn1.ASN1ObjectIdentifier;
import org.bouncycastle.asn1.ASN1Primitive;
import org.bouncycastle.asn1.x500.X500Name;
import org.bouncycastle.asn1.x509.*;
import org.bouncycastle.cert.X509CertificateHolder;
import org.bouncycastle.cert.X509v3CertificateBuilder;
import org.bouncycastle.cert.jcajce.JcaX509v3CertificateBuilder;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.operator.ContentSigner;
import org.bouncycastle.operator.jcajce.JcaContentSignerBuilder;

import java.io.*;
import java.math.BigInteger;
import java.security.*;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.text.SimpleDateFormat;
import java.util.*;
import java.security.cert.Certificate;
/**
 * @program: dpf-sign-test
 * @description: 签名工具类
 * @author: syske
 * @create: 2019-12-04 09:02
 */

public class Pkcs {

    private static KeyPair getKey() throws NoSuchAlgorithmException {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA",
                new BouncyCastleProvider());
        generator.initialize(1024);
        // 证书中的密钥 公钥和私钥
        KeyPair keyPair = generator.generateKeyPair();
        return keyPair;
    }

    /**
     * @param password
     *            密码
     * @param issuerStr 颁发机构信息
     *
     * @param subjectStr 使用者信息
     *
     * @param certificateCRL 颁发地址
     *
     * @return
     */
    public static Map<String, byte[]> createCert(String password,
                                                 String issuerStr, String subjectStr, String certificateCRL) {
        Map<String, byte[]> result = new HashMap<String, byte[]>();
        ByteArrayOutputStream out = null;
        try {
            // 生成JKS证书
            // KeyStore keyStore = KeyStore.getInstance("JKS");
            // 标志生成PKCS12证书
            KeyStore keyStore = KeyStore.getInstance("PKCS12",
                    new BouncyCastleProvider());
            keyStore.load(null, null);
            KeyPair keyPair = getKey();
            // issuer与 subject相同的证书就是CA证书
            Certificate cert = generateCertificateV3(issuerStr, subjectStr,
                    keyPair, result, certificateCRL, null);
            // cretkey随便写，标识别名
            keyStore.setKeyEntry("cretkey", keyPair.getPrivate(),
                    password.toCharArray(), new Certificate[] { cert });
            out = new ByteArrayOutputStream();
            cert.verify(keyPair.getPublic());
            keyStore.store(out, password.toCharArray());
            byte[] keyStoreData = out.toByteArray();
            result.put("keyStoreData", keyStoreData);
            return result;
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (out != null) {
                try {
                    out.close();
                } catch (IOException e) {
                }
            }
        }
        return result;
    }

    /**
     * @param issuerStr
     * @param subjectStr
     * @param keyPair
     * @param result
     * @param certificateCRL
     * @param extensions
     * @return
     */
    public static Certificate generateCertificateV3(String issuerStr,
                                                    String subjectStr, KeyPair keyPair, Map<String, byte[]> result,
                                                    String certificateCRL, List<Extension> extensions) {
        ByteArrayInputStream bout = null;
        X509Certificate cert = null;
        try {
            PublicKey publicKey = keyPair.getPublic();
            PrivateKey privateKey = keyPair.getPrivate();
            Date notBefore = new Date();
            Calendar rightNow = Calendar.getInstance();
            rightNow.setTime(notBefore);
            // 日期加1年
            rightNow.add(Calendar.YEAR, 1);
            Date notAfter = rightNow.getTime();
            // 证书序列号
            BigInteger serial = BigInteger.probablePrime(256, new Random());
            X509v3CertificateBuilder builder = new JcaX509v3CertificateBuilder(
                    new X500Name(issuerStr), serial, notBefore, notAfter,
                    new X500Name(subjectStr), publicKey);
            JcaContentSignerBuilder jBuilder = new JcaContentSignerBuilder(
                    "SHA1withRSA");
            SecureRandom secureRandom = new SecureRandom();
            jBuilder.setSecureRandom(secureRandom);
            ContentSigner singer = jBuilder.setProvider(
                    new BouncyCastleProvider()).build(privateKey);
            // 分发点
            ASN1ObjectIdentifier cRLDistributionPoints = new ASN1ObjectIdentifier(
                    "2.5.29.31");
            GeneralName generalName = new GeneralName(
                    GeneralName.uniformResourceIdentifier, certificateCRL);
            GeneralNames seneralNames = new GeneralNames(generalName);
            DistributionPointName distributionPoint = new DistributionPointName(
                    seneralNames);
            DistributionPoint[] points = new DistributionPoint[1];
            points[0] = new DistributionPoint(distributionPoint, null, null);
            CRLDistPoint cRLDistPoint = new CRLDistPoint(points);
            builder.addExtension(cRLDistributionPoints, true, cRLDistPoint);
            // 用途
            ASN1ObjectIdentifier keyUsage = new ASN1ObjectIdentifier(
                    "2.5.29.15");
            // | KeyUsage.nonRepudiation | KeyUsage.keyCertSign
            builder.addExtension(keyUsage, true, new KeyUsage(
                    KeyUsage.digitalSignature | KeyUsage.keyEncipherment));
            // 基本限制 X509Extension.java
            ASN1ObjectIdentifier basicConstraints = new ASN1ObjectIdentifier(
                    "2.5.29.19");
            builder.addExtension(basicConstraints, true, new BasicConstraints(
                    true));
            // privKey:使用自己的私钥进行签名，CA证书
            if (extensions != null)
                for (Extension ext : extensions) {
                    builder.addExtension(
                            new ASN1ObjectIdentifier(ext.getOid()),
                            ext.isCritical(),
                            ASN1Primitive.fromByteArray(ext.getValue()));
                }
            X509CertificateHolder holder = builder.build(singer);
            CertificateFactory cf = CertificateFactory.getInstance("X.509");
            bout = new ByteArrayInputStream(holder.toASN1Structure()
                    .getEncoded());
            cert = (X509Certificate) cf.generateCertificate(bout);
            byte[] certBuf = holder.getEncoded();
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
            // 证书数据
            result.put("certificateData", certBuf);
            //公钥
            result.put("publicKey", publicKey.getEncoded());
            //私钥
            result.put("privateKey", privateKey.getEncoded());
            //证书有效开始时间
            result.put("notBefore", format.format(notBefore).getBytes("utf-8"));
            //证书有效结束时间
            result.put("notAfter", format.format(notAfter).getBytes("utf-8"));
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (bout != null) {
                try {
                    bout.close();
                } catch (IOException e) {
                }
            }
        }
        return cert;
    }

    public static void main(String[] args) throws Exception{
        // CN: 名字与姓氏    OU : 组织单位名称
        // O ：组织名称  L : 城市或区域名称  E : 电子邮件
        // ST: 州或省份名称  C: 单位的两字母国家代码
        String issuerStr = "CN=电子签名,OU=github,O=github,C=CN,L=西安,ST=陕西";
        String subjectStr = "CN=电子签名,OU=github,O=github,C=CN,L=西安,ST=陕西";
        String certificateCRL  = "https://syske.github.io/";
        Map<String, byte[]> result = createCert("123456", issuerStr, subjectStr, certificateCRL);

        FileOutputStream outPutStream = new FileOutputStream("D:/keystore.p12"); // ca.jks
        outPutStream.write(result.get("keyStoreData"));
        outPutStream.close();
        FileOutputStream fos = new FileOutputStream(new File("D:/keystore.cer"));
        fos.write(result.get("certificateData"));
        fos.flush();
        fos.close();
    }
}
```



```java
package io.github.syske.common.util;

/**
 * @program: dpf-sign-test
 * @description:
 * @author: syske
 * @create: 2019-12-04 09:00
 */
public class Extension {
    private String oid;

    private boolean critical;

    private byte[] value;

    public String getOid() {
        return oid;
    }

    public byte[] getValue() {
        return value;
    }
    public boolean isCritical() {
        return critical;
    }
}
```



#### 生成签名

生成的签名是png图片

```java
package io.github.syske.common.util;

/**
 * @program: dpf-sign-test
 * @description:
 * @author: syske
 * @create: 2019-12-03 22:50
 */
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.FileOutputStream;
import java.io.IOException;
import sun.font.FontDesignMetrics;

import com.sun.image.codec.jpeg.JPEGCodec;
import com.sun.image.codec.jpeg.JPEGEncodeParam;
import com.sun.image.codec.jpeg.JPEGImageEncoder;

public class SignImage {

    /**
     * @param doctorName   String 医生名字
     * @param hospitalName String 医生名称
     * @param date         String 签名日期
     *                     图片高度
     * @param jpgname      String jpg图片名
     * @return
     */
    public static boolean createSignTextImg(
            String doctorName, //
            String hospitalName, //
            String date,
            String jpgname) {
        int width = 255;
        int height = 100;
        FileOutputStream out = null;
        //背景色
        Color bgcolor = Color.WHITE;
        //字色
        Color fontcolor = Color.RED;
        Font doctorNameFont = new Font(null, Font.BOLD, 20);
        Font othorTextFont = new Font(null, Font.BOLD, 18);
        try { // 宽度 高度
            BufferedImage bimage = new BufferedImage(width, height,
                    BufferedImage.TYPE_INT_RGB);
            Graphics2D g = bimage.createGraphics();
            g.setColor(bgcolor); // 背景色
            g.fillRect(0, 0, width, height); // 画一个矩形
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                    RenderingHints.VALUE_ANTIALIAS_ON); // 去除锯齿(当设置的字体过大的时候,会出现锯齿)

            g.setColor(Color.RED);
            g.fillRect(0, 0, 8, height);
            g.fillRect(0, 0, width, 8);
            g.fillRect(0, height - 8, width, height);
            g.fillRect(width - 8, 0, width, height);

            g.setColor(fontcolor); // 字的颜色
            g.setFont(doctorNameFont); // 字体字形字号
            FontMetrics fm = FontDesignMetrics.getMetrics(doctorNameFont);
            int font1_Hight = fm.getHeight();
            int strWidth = fm.stringWidth(doctorName);
            int y = 35;
            int x = (width - strWidth) / 2;
            g.drawString(doctorName, x, y); // 在指定坐标除添加文字

            g.setFont(othorTextFont); // 字体字形字号

            fm = FontDesignMetrics.getMetrics(othorTextFont);
            int font2_Hight = fm.getHeight();
            strWidth = fm.stringWidth(hospitalName);
            x = (width - strWidth) / 2;
            g.drawString(hospitalName, x, y + font1_Hight); // 在指定坐标除添加文字

            strWidth = fm.stringWidth(date);
            x = (width - strWidth) / 2;
            g.drawString(date, x, y + font1_Hight + font2_Hight); // 在指定坐标除添加文字

            g.dispose();
            out = new FileOutputStream(jpgname); // 指定输出文件
            JPEGImageEncoder encoder = JPEGCodec.createJPEGEncoder(out);
            JPEGEncodeParam param = encoder.getDefaultJPEGEncodeParam(bimage);
            param.setQuality(50f, true);
            encoder.encode(bimage, param); // 存盘
            out.flush();
            return true;
        } catch (Exception e) {
            return false;
        } finally {
            if (out != null) {
                try {
                    out.close();
                } catch (IOException e) {
                }
            }
        }
    }

    public static void main(String[] args) {
        createSignTextImg("华佗", "在线医院", "2018.01.01", "sign.jpg");
    }
}
```

#### 签名实现

这里需要注意的是，签名入参中的页码，如果是最后一页，页码传null

```java
package io.github.syske.common.util;

import com.itextpdf.awt.geom.Rectangle2D;
import com.itextpdf.text.Image;
import com.itextpdf.text.Rectangle;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.PdfSignatureAppearance;
import com.itextpdf.text.pdf.PdfSignatureAppearance.RenderingMode;
import com.itextpdf.text.pdf.PdfStamper;
import com.itextpdf.text.pdf.parser.ImageRenderInfo;
import com.itextpdf.text.pdf.parser.PdfReaderContentParser;
import com.itextpdf.text.pdf.parser.RenderListener;
import com.itextpdf.text.pdf.parser.TextRenderInfo;
import com.itextpdf.text.pdf.security.*;
import com.itextpdf.text.pdf.security.MakeSignature.CryptoStandard;

import org.apache.log4j.Logger;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import java.io.*;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.PrivateKey;
import java.security.Security;
import java.security.cert.Certificate;
import java.util.UUID;

/**
 * @program: SignPdf
 * @description:
 * @author: syske
 * @create: 2019-12-03 22:54
 */

public class SignPdf {
    private static Logger logger = Logger.getLogger(SignPdf.class);
    private static final String PASSWORD = "123456"; // 秘钥密码
    private static final String KEY_STORE_PATH = "d:\\keystore.p12"; // 秘钥文件路径

    private SignPdf() {
    }

    /**
     * 图片签章，指定签名坐标位置
     *
     * @param signPdfSrc
     *            签名的PDF文件
     * @param signedPdfOutFile
     *            签名后的的PDF文件
     * @param signImage
     *            签名图片完整路径
     * @param x
     *            以左下角为原点x坐标值
     * @param y
     *            以左下角为原点Y坐标值
     * @param numberOfPages
     *            签名页码，如果是最后一页则传null
     * @param pageStyle
     *            页面布局，横向或者纵向
     * @throws Exception
     */
    public static void sign(String signPdfSrc, String signedPdfOutFile,
                            String signImage, Float x, Float y, Integer numberOfPages,
                            PageStyle pageStyle) throws Exception {
        sign(signPdfSrc, signedPdfOutFile, signImage, x, y, null,
                numberOfPages, pageStyle);
    }

    /**
     * 图片签章，指定关键字
     *
     * @param signPdfSrc
     *            签名的PDF文件
     * @param signedPdfFile
     *            签名后的的PDF文件
     * @param signImage
     *            签名图片完整路径
     * @param keyWords
     *            关键字
     * @param numberOfPages
     *            签名页码，如果是最后一页则传null
     * @param pageStyle
     *            页面布局，横向或者纵向
     */
    public static void sign(String signPdfSrc, String signedPdfFile,
                            String signImage, String keyWords, Integer numberOfPages,
                            PageStyle pageStyle) throws Exception {
        sign(signPdfSrc, signedPdfFile, signImage, null, null, keyWords,
                numberOfPages, pageStyle);
    }

    /**
     * 私人签章
     *
     * @param signPdfSrc
     *            签名的PDF文件
     * @param signedPdfOutFile
     *            签名后的的PDF文件
     * @param signImage
     *            签名图片完整路径
     * @param x
     *            以左下角为原点x坐标
     * @param y
     *            以左下角为原点y坐标
     * @param keyWords
     *            关键字
     * @param numberOfPages
     *            签名页码，如果是最后一页则传null
     * @param pageStyle
     *            页面布局，横向或者纵向
     * @return
     */
    public static void sign(String signPdfSrc, String signedPdfOutFile,
                            String signImage, Float x, Float y, String keyWords,
                            Integer numberOfPages, PageStyle pageStyle) throws Exception {
        File signPdfSrcFile = new File(signPdfSrc);
        PdfReader reader = null;
        ByteArrayOutputStream signPDFData = null;
        PdfStamper stp = null;
        FileInputStream fos = null;
        FileOutputStream pdfOutputStream = null;
        try {
            BouncyCastleProvider provider = new BouncyCastleProvider();
            Security.addProvider(provider);
            KeyStore ks = KeyStore.getInstance("PKCS12",
                    new BouncyCastleProvider());
            fos = new FileInputStream(KEY_STORE_PATH);
            // 私钥密码 为Pkcs生成证书是的私钥密码 123456
            ks.load(fos, PASSWORD.toCharArray());
            String alias = ks.aliases().nextElement();
            PrivateKey key = (PrivateKey) ks.getKey(alias,
                    PASSWORD.toCharArray());
            Certificate[] chain = ks.getCertificateChain(alias);
            reader = new PdfReader(signPdfSrc); // 也可以输入流的方式构建
            signPDFData = new ByteArrayOutputStream();
            numberOfPages = numberOfPages == null ? reader.getNumberOfPages()
                    : 0;

            // 临时pdf文件
            File temp = new File(signPdfSrcFile.getParent(),
                    System.currentTimeMillis() + ".pdf");
            stp = PdfStamper.createSignature(reader, signPDFData, '\0', temp,
                    true);
            stp.setFullCompression();
            PdfSignatureAppearance sap = stp.getSignatureAppearance();
            sap.setReason("数字签名，不可改变");
            // 使用png格式透明图片
            Image image = Image.getInstance(signImage);

            sap.setImageScale(0);
            sap.setSignatureGraphic(image);
            sap.setRenderingMode(RenderingMode.GRAPHIC);
            float llx = 0f;
            float lly = 0f;

            float signImageWidth = image.getWidth();
            float signImageHeight = image.getHeight();

            float signImageHeightSocale = 85 / signImageWidth * signImageHeight;
            if (keyWords != null && !keyWords.isEmpty()) {
                KeyWordInfo keyWordInfo = getKeyWordLocation(numberOfPages,
                        keyWords, reader);
                Rectangle pageSize = reader.getPageSize(numberOfPages);
                float width = pageSize.getWidth();
                if (PageStyle.PAGE_STYLE_LANDSCAPE.equals(pageStyle)) {
                    llx = keyWordInfo.getY() + (float) keyWordInfo.getHeight();
                    lly = width - keyWordInfo.getX() - signImageHeightSocale
                            / 2;
                } else if (PageStyle.PAGE_STYLE_PORTRAIT.equals(pageStyle)) {
                    llx = keyWordInfo.getX() + (float) keyWordInfo.getWidth()*keyWords.length();
                    lly = keyWordInfo.getY() - signImageHeightSocale / 2;
                }

            } else if (x != null && y != null) {
                llx = x;
                lly = y;
            } else {
                throw new Exception("坐标和关键字不能同时为空！");
            }

            float urx = llx + 85;
            float ury = lly + signImageHeightSocale;
            // 是对应x轴和y轴坐标
            sap.setVisibleSignature(new Rectangle(llx, lly, urx, ury),
                    numberOfPages,
                    UUID.randomUUID().toString().replaceAll("-", ""));
            stp.getWriter().setCompressionLevel(5);
            ExternalDigest digest = new BouncyCastleDigest();
            ExternalSignature signature = new PrivateKeySignature(key,
                    DigestAlgorithms.SHA512, provider.getName());
            MakeSignature.signDetached(sap, digest, signature, chain, null,
                    null, null, 0, CryptoStandard.CADES);
            stp.close();
            reader.close();
            pdfOutputStream = new FileOutputStream(signedPdfOutFile);
            pdfOutputStream.write(signPDFData.toByteArray());
            pdfOutputStream.close();
        } catch (KeyStoreException e) {
            logger.error("签名验证失败", e);
            throw new Exception("签名验证失败", e);
        } catch (FileNotFoundException e) {
            logger.error("文件未找到", e);
            throw new Exception("文件未找到", e);
        } catch (IOException e) {
            logger.error("IO异常", e);
            throw new Exception("IO异常", e);
        } catch (Exception e) {
            logger.error("签章失败", e);
            throw new Exception("签章失败", e);
        } finally {
            if (signPDFData != null) {
                try {
                    signPDFData.close();
                } catch (IOException e) {
                    logger.error("资源关闭失败", e);
                    throw new Exception("资源关闭失败", e);
                }
            }

            if (fos != null) {
                try {
                    fos.close();
                } catch (IOException e) {
                    logger.error("资源关闭失败", e);
                    throw new Exception("资源关闭失败", e);
                }
            }
            if (pdfOutputStream != null) {
                try {
                    pdfOutputStream.close();
                } catch (IOException e) {
                    logger.error("资源关闭失败", e);
                    throw new Exception("资源关闭失败", e);
                }
            }

        }
    }

    /**
     * 查找关键字定位
     *
     * @param numberOfPages
     * @param keyWords
     *            关键字
     * @param reader
     * @return
     * @throws IOException
     */
    private static KeyWordInfo getKeyWordLocation(Integer numberOfPages,
                                                  final String keyWords, PdfReader reader) throws IOException {
        PdfReaderContentParser pdfReaderContentParser = new PdfReaderContentParser(
                reader);

        final KeyWordInfo keyWordInfo = new KeyWordInfo();

        pdfReaderContentParser.processContent(numberOfPages,
                new RenderListener() {
                    @Override
                    public void renderText(TextRenderInfo textRenderInfo) {
                        String text = textRenderInfo.getText(); // 整页内容

                        if (null != text && text.contains(keyWords)) {
                            Rectangle2D.Float boundingRectange = textRenderInfo
                                    .getBaseline().getBoundingRectange();
                            float leftY = (float) boundingRectange.getMinY() - 1;
                            float rightY = (float) boundingRectange.getMaxY() + 1;

                            logger.debug(boundingRectange.x + "--"
                                    + boundingRectange.y + "---");

                            keyWordInfo.setHeight(rightY - leftY);
                            keyWordInfo.setWidth((rightY - leftY)
                                    * keyWords.length());
                            keyWordInfo.setX(boundingRectange.x);
                            keyWordInfo.setY(boundingRectange.y);
                        }

                    }

                    @Override
                    public void renderImage(ImageRenderInfo arg0) {}

                    @Override
                    public void endTextBlock() {}

                    @Override
                    public void beginTextBlock() {}
                });
        return keyWordInfo;
    }

    private static class KeyWordInfo {
        private float x;
        private float y;
        private double width;
        private double height;

        public float getX() {
            return x;
        }

        public void setX(float x) {
            this.x = x;
        }

        public float getY() {
            return y;
        }

        public void setY(float y) {
            this.y = y;
        }

        public double getWidth() {
            return width;
        }

        public void setWidth(double width) {
            this.width = width;
        }

        public double getHeight() {
            return height;
        }

        public void setHeight(double height) {
            this.height = height;
        }
    }

    enum PageStyle {
        PAGE_STYLE_LANDSCAPE, // 横向
        PAGE_STYLE_PORTRAIT // 纵向
    }

    public static PageStyle getPageStyle_LANDSCAPE() {
        return PageStyle.PAGE_STYLE_LANDSCAPE;
    }

    public static PageStyle getPageStyle_PORTRAIT() {
        return PageStyle.PAGE_STYLE_PORTRAIT;
    }

    public static void main(String[] args) throws Exception {
        sign("E:\\test2_sgin.pdf",//
                "D:\\signed-35.pdf",
                "E:\\workSpeace\\pansky\\other_files\\电子签章\\png\\sign_0000_1_yxz.png",
                null, null, "负责人", null, PageStyle.PAGE_STYLE_LANDSCAPE);
        // read();

        // test();
    }



}
```

#### 项目pom依赖

差点都忘记了😂

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>io.github.syske</groupId>
    <artifactId>dpf-sign-test</artifactId>
    <version>1.0-SNAPSHOT</version>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>6</source>
                    <target>6</target>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <dependencies>
        <dependency>
            <groupId>com.itextpdf</groupId>
            <artifactId>itextpdf</artifactId>
            <version>5.5.13</version>
        </dependency>

        <!-- https://mvnrepository.com/artifact/com.itextpdf/itext-asian -->
        <dependency>
            <groupId>com.itextpdf</groupId>
            <artifactId>itext-asian</artifactId>
            <version>5.2.0</version>
        </dependency>

        <dependency>
            <groupId>org.bouncycastle</groupId>
            <artifactId>bcpkix-jdk15on</artifactId>
            <version>1.64</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on -->

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
            <version>1.7.25</version>
        </dependency>


    </dependencies>


</project>
```

签名预览

![image-20200104103808061](..\images\image-20200104103808061.png)

#### 总结

因为本身业务不复杂，所以也没有过多的说明，但以上代码实现部分还有很多需要改进的地方，比如：

1、查找关键字的时候，只获取了一次坐标，但是同一页关键字可能存在多个，如果想在相同关键字的地方都盖章，是不能实现的，如果你正好有这样的需求，你可以动手自己改造；

2、和第一个类似，没有实现全文档签名

[^1]: https://blog.csdn.net/javasun608/article/details/79307845

##### 项目源码路径:https://github.com/Syske/learning-dome-code.git

