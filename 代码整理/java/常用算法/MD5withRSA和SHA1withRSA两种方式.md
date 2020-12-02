```
package rsa;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;


import client.util.HEX2Byte;

public class DigitalSignatureMain {
	public static void main(String[] args) throws Exception {
		String content = "study hard and make progress everyday";
		System.out.println("content :" + content);

		KeyPair keyPair = getKeyPair();
		PublicKey publicKey = keyPair.getPublic();
		PrivateKey privateKey = keyPair.getPrivate();

		String md5Sign = getMd5Sign(content, privateKey);
		System.out.println("sign with md5 and rsa :" + md5Sign);
		boolean md5Verifty = verifyWhenMd5Sign(content, md5Sign, publicKey);
		System.out.println("verify sign with md5 and rsa :" + md5Verifty);

		String sha1Sign = getSha1Sign(content, privateKey);
		System.out.println("签名长度：" + sha1Sign.length());
		System.out.println("sign with sha1 and rsa :" + sha1Sign);
		boolean sha1Verifty = verifyWhenSha1Sign(content, sha1Sign, publicKey);
		System.out.println("verify sign with sha1 and rsa :" + sha1Verifty);

	}

	// 生成密钥对
	static KeyPair getKeyPair() throws Exception {
		KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
		keyGen.initialize(512); // 可以理解为：加密后的密文长度，实际原文要小些 越大 加密解密越慢
		KeyPair keyPair = keyGen.generateKeyPair();
		return keyPair;
	}

	// 用md5生成内容摘要，再用RSA的私钥加密，进而生成数字签名
	static String getMd5Sign(String content, PrivateKey privateKey)
			throws Exception {
		byte[] contentBytes = content.getBytes("utf-8");
		Signature signature = Signature.getInstance("MD5withRSA");
		signature.initSign(privateKey);
		signature.update(contentBytes);
		byte[] signs = signature.sign();
		return HEX2Byte.bytesToHex(signs);
	}

	// 对用md5和RSA私钥生成的数字签名进行验证
	static boolean verifyWhenMd5Sign(String content, String sign,
			PublicKey publicKey) throws Exception {
		byte[] contentBytes = content.getBytes("utf-8");
		Signature signature = Signature.getInstance("MD5withRSA");
		signature.initVerify(publicKey);
		signature.update(contentBytes);
		return signature.verify(HEX2Byte.hexToByteArray(sign));
	}

	// 用sha1生成内容摘要，再用RSA的私钥加密，进而生成数字签名
	static String getSha1Sign(String content, PrivateKey privateKey)
			throws Exception {
		byte[] contentBytes = content.getBytes("utf-8");
		Signature signature = Signature.getInstance("SHA1withRSA");
		signature.initSign(privateKey);
		signature.update(contentBytes);
		byte[] signs = signature.sign();
		return HEX2Byte.bytesToHex(signs);
	}

	// 对用md5和RSA私钥生成的数字签名进行验证
	static boolean verifyWhenSha1Sign(String content, String sign,
			PublicKey publicKey) throws Exception {
		byte[] contentBytes = content.getBytes("utf-8");
		Signature signature = Signature.getInstance("SHA1withRSA");
		signature.initVerify(publicKey);
		signature.update(contentBytes);
		
		return signature.verify(HEX2Byte.hexToByteArray(sign));
	}
}
```
工具类
```java
package client.util;

public class HEX2Byte {
	/**
	 * hex字符串转byte数组
	 * 
	 * @param inHex
	 *            待转换的Hex字符串
	 * @return 转换后的byte数组结果
	 */
	public static byte[] hexToByteArray(String inHex) {
		int hexlen = inHex.length();
		byte[] result;
		if (hexlen % 2 == 1) {
			// 奇数
			hexlen++;
			result = new byte[(hexlen / 2)];
			inHex = "0" + inHex;
		} else {
			// 偶数
			result = new byte[(hexlen / 2)];
		}
		int j = 0;
		for (int i = 0; i < hexlen; i += 2) {
			result[j] = hexToByte(inHex.substring(i, i + 2));
			j++;
		}

		return result;
	}

	/**
	 * Hex字符串转byte
	 * 
	 * @param inHex
	 *            待转换的Hex字符串
	 * @return 转换后的byte
	 */
	public static byte hexToByte(String inHex) {
		return (byte) Integer.parseInt(inHex, 16);
	}

	/**
	 * 字节数组转16进制
	 * 
	 * @param bytes
	 *            需要转换的byte数组
	 * @return 转换后的Hex字符串
	 */
	public static String bytesToHex(byte[] bytes) {
		StringBuffer sb = new StringBuffer();
		for (int i = 0; i < bytes.length; i++) {
			String hex = Integer.toHexString(bytes[i] & 0xFF);
			if (hex.length() < 2) {
				sb.append(0);
			}
			sb.append(hex);
		}
		return sb.toString();
	}

}

```