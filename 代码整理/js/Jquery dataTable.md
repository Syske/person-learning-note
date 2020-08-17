### 示例代码
#### js
```
 $('#sampleTable').on( 'init.dt', function () {           // 初始化之后执行的回调函数
            $('.bs-component [data-toggle="popover"]').popover();
        } ).DataTable( {
            destroy: true,
            data : dataString,
            bAutoWidth: false,
            language: {
                paginate: {
                    first: '首页',
                    previous: '上一页',
                    next: '下一页',
                    last: '尾页',
                },
                info: "第 _START_ 至 _END_ 行，共 _TOTAL_ 行",
                search: "搜索:",
                searchPlaceholder: "请输入要搜索内容...",
                processing: "处理中...",
                lengthMenu: "显示 _MENU_ 项结果",
                zeroRecords: "没有找到相应的结果",
                infoEmpty: "第 0 至 0 项结果，共 0 项",
                infoFiltered: "(由 _MAX_ 项结果过滤)",
            },
            "columnDefs": [
                { "title": "协议号" , "targets": 0, "class": "center" },
                { "title": "身份证号" , "targets": 1, "class": "center" },
                { "title": "个人参保号" , "targets": 2, "class": "center" },
                { "title": "姓名" , "targets": 3, "class": "center" },
                { "title": "参保地" , "targets": 4, "class": "center" },
                { "title": "就医地" , "targets": 5, "class": "center" },
                { "title": "开始时间" , "targets": 6, "class": "center" },
                { "title": "结束时间" , "targets": 7, "class": "center" },
                { "title": "就医类型" , "targets": 8, "class": "center" },
                { "title": "协议标识" , "targets": 9, "class": "center" },
                { "title": "全选标识" , "targets": 10, "class": "center" },
                { "title": "险种" , "targets": 11, "class": "center" ,
                    "render": function ( data, type, full, meta ) {
                        switch(data) {
                            case '3' : return '职工';
                                break;
                            case '390' : return '居民';
                                break;
                            case '340' : return '离休';
                                break;
                            case '350' : return '残疾军人';
                                break;
                            case '360' : return '老红军';
                                break;
                            case '380' : return '新农合';
                                break;
                            case '391' : return '城镇居民';
                                break;
                        }
                    }},
                { "title": "上传时间" , "targets": 12, "class": "center" },
                { "title": "行政区划" , "targets": 13, "class": "center" },
                { "title": "医院" , "targets": 14, "class": "center" }
            ],
            "columns": [
                { "data": "bAZ201" , "class": "center" ,"sDefaultContent" : "-"},
                { "data": "aAC002" , "class": "center" ,"sDefaultContent" : "-"},
                { "data": "aAC001" , "class": "center" ,"sDefaultContent" : "-"},
                { "data": "aAC003", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAB721_Name", "class": "center","sDefaultContent" : "-" },
                { "data": "bAB720_Name", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAE010", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAE011", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAE018", "class": "center" ,"sDefaultContent" : "-",
                    "render": function ( data, type, full, meta ) {
                        if (data=='03')
                            return '<span class="badge badge-success">转外就医</span>';
                        else if (data=='01')
                            return '<span class="badge badge-warning">异地安置</span>' ;
                        else if (data=='02')
                            return '<span class="badge badge-primary">其他</span>';
                    }},
                { "data": "bAE019", "class": "center" ,"sDefaultContent" : "-",
                    "render": function ( data, type, full, meta ) {
                        if (data=='1')
                            return '<span class="badge badge-success">有效</span>'
                        else if (data=='0')
                            return '<span class="badge badge-danger">无效</span>'
                    }},
                { "data": "bAE025", "class": "center" ,"sDefaultContent" : "-",
                    "render": function ( data, type, full, meta ) {
                        if (data=='1')
                            return '<span class="badge badge-primary">全选</span>'
                        else if (data=='0')
                            return '<span class="badge badge-warning">非全选</span>'
                    }},
                { "data": "aAE140", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAE020", "class": "center" ,"sDefaultContent" : "-"},
                { "data": "bAA001", "class": "center" ,"sDefaultContent" : "-"},
                { "data": null,
                    "render": function ( data, type, full, meta ) {
                        var str_bt = " ";
                        $.ajax( {type : "POST", //提交方式
                            async: false,
                            url : "/kc0hQuery",//路径
                            data : {
                                "BAZ201" : full.bAZ201
                            },//数据，这里使用的是Json格式进行传输
                            success : function(result) {
                                var resultString = eval(result);
                                for(i in resultString) {
                                    if (i == resultString.length-1)
                                        str_bt+=resultString[i].bAB002;
                                    else
                                        str_bt =str_bt + resultString[i].bAB002+ '<br>';
                                }
                            }
                        });
                        var bt_test = $('<div class="bs-component"><button class="btn btn-info" type="button" title="" data-container="body" data-toggle="popover" data-placement="bottom" data-content="'+ str_bt +'" data-original-title="医院列表" data-html="true">医院列表</button></div>')

                        if(full.bAE018=='03') {
                            return bt_test.html();
                        } else if(full.bAE018=='02') {
                            return bt_test.html();
                        } else {
                            return '<button class="btn btn-success" type="button" onclick="queryKB0a(\''+ full.bAB721+'\',\''+ full.bAB720+'\',\''+ full.aAC002+'\')">协议医院</button>';
                        }
                    }}
            ]
        } );
```
#### html
```
<div class="col-md-12" style="overflow-x: scroll;">
            <div class="tile" style="width: 180%;">
                <h3 class="tile-title">备案列表</h3>
                <div class="bs-component">
                    <table class="table" id="sampleTable">
                    </table>
                </div>

    </div>
```