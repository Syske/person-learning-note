```
$(function () {
          var ajaxFormOption = {
               type: "post",  //提交方式 
               dataType: "json", //数据类型 
               data: myData,//自定义数据参数，视情况添加
               url: "TestHandler.ashx?type=ajaxForm", //请求url 
               success: function (data) { //提交成功的回调函数 
                  document.write("success");
               }
           };
 
           //form中有submit按钮——方式1
           $("#form1").ajaxForm(ajaxFormOption);
 
           //form中有submit按钮——方式2
           $("#form1").submit(function () {
               $(this).ajaxSubmit(ajaxFormOption);
                 return false;
           });
 
          //不需要submit按钮，可以是任何元素的click事件
           $("#myButton").click(function () {
                $("#form1").ajaxSubmit(ajaxFormOption);
                  return false;
           });
 
       });
       
       ```
      完整 
       ```
var object= {
              url:url,　　　　　　//form提交数据的地址
　　　　　　  type:type,　　　  //form提交的方式(method:post/get)
　　　　　　  target:target,　　//服务器返回的响应数据显示的元素(Id)号
              beforeSerialize:function(){} //序列化提交数据之前的回调函数
　　　　　　  beforeSubmit:function(){},　　//提交前执行的回调函数
　　　　　　  success:function(){},　　　　   //提交成功后执行的回调函数
              error:function(){},             //提交失败执行的函数
　　　　　　  dataType:null,　　　　　　　//服务器返回数据类型
　　　　　　  clearForm:true,　　　　　　 //提交成功后是否清空表单中的字段值
　　　　　　  restForm:true,　　　　　　  //提交成功后是否重置表单中的字段值，即恢复到页面加载时的状态
　　　　　　  timeout:6000 　　　　　 　 //设置请求时间，超过该时间后，自动退出请求，单位(毫秒)。　　

}
       ```