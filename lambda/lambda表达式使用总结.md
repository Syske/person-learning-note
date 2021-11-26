# lambda表达式使用总结

### 前言

最近一段时间一直在赶项目，所以也比较忙，但是整个项目参与的收获可以和各位小伙伴分享下。由于整个项目都采用`redis`存储数据（你没听错，就是拿`redis`当数据库），所以在数据读写方面，特别是查询的时候，很多场景下都是拿到数据后，还需要手动处理下，所以本次对`lambda`使用的频次特别高，今天我们就先抽点时间做一个简单的梳理和总结。



### 拉姆达表达式

我想各位各位小伙伴对`lambda`表达式应该不会太陌生，`lambda`是`JDK1.8`引入的新特性，而且经常在面试的时候会被问道，更重要的是用`lambda`确实可以让我们的代码更简洁，很多场景也更容易实现。前面我们也分享过`lambda`的相关知识点，感兴趣的小伙伴可以去看下：

[每日一例 | 流式编程时代，效率之王了解下？](https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648417789&idx=1&sn=712ded6251339a87c4f9db92a4402890&chksm=bea6cb7789d142615e152f3834523e3c83b98ddb465d902542573360e458d93b65ca0ce4bdd6&token=28080402&lang=zh_CN#rd)

[每日一例 | 要想java学的好，optional少不了……](https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648418162&idx=1&sn=ad7169e2cb9caeb0d14258b698b7343c&chksm=bea6c9f889d140ee7a25f46b50ab7704ea17bb05d02dfc52d84786dafbafa189a91c3f6558e9&token=28080402&lang=zh_CN#rd)

[每日一例 | lamubda表达式之forEach](https://mp.weixin.qq.com/s?__biz=MjM5NDMwNzA0NQ==&mid=2648417426&idx=1&sn=0343e6ec2838440e9cc311e102c5344f&chksm=bea6ca1889d1430e5f2f9310269c6b7983dbaa144ae059608409f4c2dbd34bd3ad213654c0ce&token=28080402&lang=zh_CN#rd)

今天我们主要`lambda`中的以下几块内容，这几个也是本次用的频次比较高的：

- `map`

- `filter`

- `joining`

- `max`

- 排序

- `flatMap`

- `collect`

  