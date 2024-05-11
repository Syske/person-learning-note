
### 项目构建

#### 依赖

```xml
<dependency>  
    <groupId>io.netty</groupId>  
    <artifactId>netty-all</artifactId> <!-- Use 'netty-all' for 4.0 or above -->  
    <version>4.1.65.Final</version>  
    <scope>compile</scope>  
</dependency>
```

#### 服务器端

下属代码是启动服务器代码

```java
public static void main(String[] args) {  
    //构造两个线程组  
    EventLoopGroup bossrGroup = new NioEventLoopGroup();  
    EventLoopGroup workerGroup = new NioEventLoopGroup();  
    try {  
        //服务端启动辅助类  
        ServerBootstrap bootstrap = new ServerBootstrap();  
  
        bootstrap.group(bossrGroup, workerGroup)  
                .channel(NioServerSocketChannel.class)  
                .childHandler(new HttpServerInitializer());  
  
        ChannelFuture future = bootstrap.bind(8080).sync();  
        //等待服务端口关闭  
        future.channel().closeFuture().sync();  
    } catch (InterruptedException e) {  
        e.printStackTrace();  
    }finally {  
        // 优雅退出，释放线程池资源  
        bossrGroup.shutdownGracefully();  
        workerGroup.shutdownGracefully();  
    }  
}
```

##### 服务器初始化组件

这里有个坑，如果`SimpleChannelInboundHandler`的请求泛型是`FullHttpRequest`，那消息聚合器必须设置，否则浏览器请求时，就会一直无响应，服务器也收不到请求。
但是如果请求是`DefaultHttpRequest`，则可以不指定消息集合器

```java
public class HttpServerInitializer extends ChannelInitializer<SocketChannel> {  
  
    @Override  
    protected void initChannel(SocketChannel sc) throws Exception {  
        ChannelPipeline pipeline = sc.pipeline();  
        //处理http消息的编解码  
        pipeline.addLast("httpServerCodec", new HttpServerCodec());  
        // 添加 HTTP 消息聚合器  
        pipeline.addLast(new HttpObjectAggregator(65536));  
        //添加自定义的ChannelHandler  
        pipeline.addLast("httpServerHandler", new HttpServerChannelHandler());  
    }  
}
```

##### 请求处理器

```java
@ChannelHandler.Sharable  
public class HttpServerChannelHandler extends SimpleChannelInboundHandler<FullHttpRequest > {  
  
    protected void channelRead0(ChannelHandlerContext ctx, FullHttpRequest  request) {  
  
        ctx.channel().remoteAddress();  
  
        System.out.println("请求方法名称:" + request.method().name());  
  
        System.out.println("uri:" + request.uri());  
        String uri = request.uri();  
        System.out.print(uri);  
        HttpHeaders headers = request.headers();  
        System.out.println(headers);  
  
  
        ByteBuf byteBuf = Unpooled.copiedBuffer("hello world", CharsetUtil.UTF_8);  
        FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK, byteBuf);  
        response.headers().add(HttpHeaderNames.CONTENT_TYPE, "text/plain");  
        response.headers().add(HttpHeaderNames.CONTENT_LENGTH, byteBuf.readableBytes());  
  
        ctx.writeAndFlush(response);  
    }  
}
```
