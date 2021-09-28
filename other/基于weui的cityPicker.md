## 基于weui的城市选择器（city-picker）

### 前言

最近在用weui做一个移动端的项目，有个城市选择器的需求，但是weui原生并不支持，需要自定义实现，查了一些资料，需求完美实现，下面分享下实现过程。

### 效果

先看下最终的效果：

![](https://gitee.com/sysker/picBed/raw/master/images/20210928103642.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210928103700.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210928103716.png)

![](https://gitee.com/sysker/picBed/raw/master/images/20210928103734.png)



### 代码

#### html

话不多说，先放html页面：

```html
    <div class="weui-form">
            <div class="weui-form__text-area">
                <h2 class="weui-form__title">城市选择器示例</h2>
            </div>
         
            <div id="apply-form" class="weui-form__control-area" style="margin: 20px 0;">
                <div style="margin-left: 15px; margin-bottom: 10px; overflow: hidden;">
                    <span style="display: block; width: 5px; height: 25px; background: #10aeff; float: left; margin-right: 10px; border-radius: 2px;"></span>
                    <span style="float: left;">城市信息</span>
                </div>
                <div class="weui-cells__title">请认真填写以下信息</div>
                <div class="weui-cells weui-cells_form"> 
                    <div class="weui-cell weui-cell_active weui-cell_access" id="showCityPicker1">
                        <div class="weui-cell__hd"><label class="weui-label">省份1级<spsn style="color: red; float: left; margin-right: 5px;">*</spsn></label></div>
                        <div class="weui-cell__bd weui-flex"><label id="city1-label"
                                                                    style="color: #ccc;">请选择省份</label>
                            <input id="city1" type="hidden" tips="请选择省份">
                        </div>
                        <div class="weui-cell__ft"></div>
                    </div>
                </div>

                <div class="weui-cells weui-cells_form"> 
                    <div class="weui-cell weui-cell_active weui-cell_access" id="showCityPicker2">
                        <div class="weui-cell__hd"><label class="weui-label">城市2级<spsn style="color: red; float: left; margin-right: 5px;">*</spsn></label></div>
                        <div class="weui-cell__bd weui-flex"><label id="city2-label"
                                                                    style="color: #ccc;">请选择城市</label>
                            <input id="city2" type="hidden" tips="请选择城市">
                        </div>
                        <div class="weui-cell__ft"></div>
                    </div>
                </div>

                <div class="weui-cells weui-cells_form"> 
                    <div class="weui-cell weui-cell_active weui-cell_access" id="showCityPicker3">
                        <div class="weui-cell__hd"><label class="weui-label">城市区县3级<spsn style="color: red; float: left; margin-right: 5px;">*</spsn></label></div>
                        <div class="weui-cell__bd weui-flex"><label id="city3-label"
                                                                    style="color: #ccc;">请选择城市区县</label>
                            <input id="city3" type="hidden" tips="请选择城市">
                        </div>
                        <div class="weui-cell__ft"></div>
                    </div>
                </div>
            </div>
            <div class="weui-form__opr-area">
                <a class="weui-btn weui-btn_primary" href="javascript:" id="make-sure">确定</a>
            </div>
        </div>
```

#### js

js代码：

```js
$(function () {
            $('#make-sure').on('click', function () {
                var msg = "你选择的省份编码是：" + $('#showCityPicker1  #city1').val() +
                "\n你选择的城市编码是：" + $('#showCityPicker2  #city2').val() +
                "\n你选择的城市区县编码是：" + $('#showCityPicker3  #city3').val()
                alert();
            });

            $('#showCityPicker1').on('click', function () {
                weui.picker(cityData, {
                    defaultValue: [110000],
                    depth: 1,
                    onChange: function (result) {
                        console.log(result);
                    },
                    onConfirm: function (result) {
                        console.log(result);
                        $('#showCityPicker1  #city1-label').html(result[0].label);
                        $('#showCityPicker1  #city1-label').css("color", "#000");
                        $('#showCityPicker1  #city1').val(result[0].value);
                    },
                    title: '省份'
                });
            }); 
           
            $('#showCityPicker2').on('click', function () {
                weui.picker(cityData, {
                    defaultValue: [110000, 110000],
                    depth: 2,
                    onChange: function (result) {
                        console.log(result);
                    },
                    onConfirm: function (result) {
                        console.log(result);
                        $('#showCityPicker2  #city2-label').html(result[0].label + " - " + result[1].label);
                        $('#showCityPicker2  #city2-label').css("color", "#000");
                        $('#showCityPicker2  #city2').val(result[1].value);
                    },
                    title: '城市'
                });
            });  

            $('#showCityPicker3').on('click', function () {
                weui.picker(cityData, {
                    defaultValue: [110000, 110000, 110101],
                    depth: 3,
                    onChange: function (result) {
                        console.log(result);
                    },
                    onConfirm: function (result) {
                        console.log(result);
                        $('#showCityPicker3  #city3-label').html(result[0].label + " - " + result[1].label + " - " + result[2].label);
                        $('#showCityPicker3  #city3-label').css("color", "#000");
                        $('#showCityPicker3  #city3').val(result[2].value);
                    },
                    title: '城市区县'
                });
            });  
        });    
```

其中cityData是我修改的城市信息，大致结构如下：

```js
ar cityData = [{
    value: 110000,
    label: '北京市',
    children: [{
        value: 110000,
        label: '北京市',
        children: [{value: 110101, label: '东城区'}, {value: 110102, label: '西城区'}, {
            value: 110105,
            label: '朝阳区'
        }, {value: 110106, label: '丰台区'}, {value: 110107, label: '石景山区'}, {
            value: 110108,
            label: '海淀区'
        }, {value: 110109, label: '门头沟区'}, {value: 110111, label: '房山区'}, {
            value: 110112,
            label: '通州区'
        }, {value: 110113, label: '顺义区'}, {value: 110114, label: '昌平区'}, {
            value: 110115,
            label: '大兴区'
        }, {value: 110116, label: '怀柔区'}, {value: 110117, label: '平谷区'}, {
            value: 110118,
            label: '密云区'
        }, {value: 110119, label: '延庆区'}]
    }]
},{...}
```

完整代码请移步github，文末有地址。

### 结语

这就是个简单的示例，有需求的小伙伴自取，githuhub路径：[weui-demo-city-picker](https://github.com/Syske/learning-dome-code/blob/dev/weui-demo/city-picker.html)。

因为这次的项目也实现了在线签名的需求，所以后面也会发布在线签名的相关实现

