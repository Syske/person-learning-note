tags: [#code, #ztree]

# 1、css样式

```css
<style type="text/css">
.ztree li span.button.add {
	margin-left: 2px;
	margin-right: -1px;
	background-position: -144px 0;
	vertical-align: top;
	*vertical-align: middle
}
</style>
```

# 2、html
```html
<ul id="treeDemo" class="ztree"></ul>
```
添加tree模态框
```html
<!-- Modal -->
				<div class="modal" id="myModalAddCategory" tabindex="-1"
					role="dialog" aria-labelledby="myModalLabel">
					<div class="modal-dialog" role="document">
						<div class="modal-content">
							<div class="modal-header">
								<button type="button" class="close" data-dismiss="modal"
									aria-label="Close">
									<span aria-hidden="true">&times;</span>
								</button>
								<h4 class="modal-title" id="myModalLabel">添加分类</h4>
							</div>
							<div class="modal-body">
								<form class="form-horizontal" id="addform">
									<div class="form-group">
										<input type="text" class="form-control" name="name"
											placeholder="分类名" id="name">
									</div>
									<div class="form-group">
										<input type="text" class="form-control" name="descr"
											placeholder="菜单描述" id="descr">
									</div>
									<div class="am-form-group">
										<label for="doc-ipt-pwd-2" class="am-u-sm-2 am-form-label">状态：</label>
										<label class="am-radio-inline"> <input type="radio"
											name="status" id="status1" value="1" checked>启用
										</label> <label class="am-radio-inline"> <input type="radio"
											name="status" id="status0" value="0">禁用
										</label>
									</div>
								</form>
							</div>
							<div class="modal-footer">
								<button type="button" class="btn btn-info" data-dismiss="modal">关闭</button>
								<button type="button" data-dismiss="modal"
									class="btn btn-danger" id="modalAddBtn">确认</button>
							</div>
						</div>
					</div>
				</div>
```


# 3、js

```js
<script type="text/javascript">
		//alert("tesete")
		var setting = {
				view : {
					addHoverDom : addHoverDom,
					removeHoverDom : removeHoverDom,
					selectedMulti : false
				},
				check : {
					enable : true
				},
				edit : {
					enable : true,
				},
				data : {
					simpleData : {
						enable : true,
						pIdKey : "pid"
					}
				},
				callback : {
					beforeDrag : beforeDrag,
					beforeEditName : beforeEditName,
					beforeRemove : beforeRemove,
					beforeRename : beforeRename,
					onRemove : onRemove,
					onRename : onRename
				}
			};

			/*增删改*/
			var zNodes;
			var log, className = "dark";
			function beforeDrag(treeId, treeNodes) {
				return false;
			}
			function beforeEditName(treeId, treeNode) {
				className = (className === "dark" ? "" : "dark");
				showLog("[ " + getTime() + " beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; "
						+ treeNode.name);
				var zTree = $.fn.zTree.getZTreeObj("treeDemo");
				zTree.selectNode(treeNode);
				setTimeout(function() {
					if (confirm("确认修改 " + treeNode.name + " 吗？")) {
						setTimeout(function() {
							zTree.editName(treeNode);
						}, 0);
					}
				}, 0);
				return false;
			}
			function beforeRemove(treeId, treeNode) {
				className = (className === "dark" ? "" : "dark");
				showLog("[ " + getTime() + " beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
						+ treeNode.name);
				var zTree = $.fn.zTree.getZTreeObj("treeDemo");
				zTree.selectNode(treeNode);
				return confirm("确认删除 节点 -- " + treeNode.name + " 吗？");
			}
			function onRemove(e, treeId, treeNode) {
				showLog("[ " + getTime() + " onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; "
						+ treeNode.name);
				$.ajax({
					type : "POST",
					url : "/shopping/manager/deleteCategory",
					data : {
						"id" : treeNode.id
					},
					dataType : "json",
					async : false,//同步
					success : function(data) {
						$(".panel-body").html(data);
					}
				});

			}
			function beforeRename(treeId, treeNode, newName, isCancel) {
				className = (className === "dark" ? "" : "dark");
				showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + getTime()
						+ " beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
						+ (isCancel ? "</span>" : ""));
				if (newName.length == 0) {
					setTimeout(function() {
						var zTree = $.fn.zTree.getZTreeObj("treeDemo");
						zTree.cancelEditName();
						alert("资源名称不能为空.");
					}, 0);
					return false;
				} else {
					$.ajax({
						type : "POST",
						url : "/shopping/manager/updateCategory",
						data : {
							"id" : treeNode.id,
							"name" : newName
						},
						dataType : "json",
						async : false,//同步
						success : function(data) {
							$(".panel-body").html(data);
						}
					});
				}
				return true;
			}
			function onRename(e, treeId, treeNode, isCancel) {
				showLog((isCancel ? "<span style='color:red'>" : "") + "[ " + getTime()
						+ " onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name
						+ (isCancel ? "</span>" : ""));
			}
			function showRemoveBtn(treeId, treeNode) {
				return !treeNode.isFirstNode;
			}
			function showRenameBtn(treeId, treeNode) {
				return !treeNode.isLastNode;
			}

			function showLog(str) {
				if (!log)
					log = $("#log");
				log.append("<li class='"+className+"'>" + str + "</li>");
				if (log.children("li").length > 8) {
					log.get(0).removeChild(log.children("li")[0]);
				}
			}
			function getTime() {
				var now = new Date(), h = now.getHours(), m = now.getMinutes(), s = now
						.getSeconds(), ms = now.getMilliseconds();
				return (h + ":" + m + ":" + s + " " + ms);
			}
		<%--
				*新增分类
				
				--%>
			var newCount = 1;
			function addHoverDom(treeId, treeNode) {
				var sObj = $("#" + treeNode.tId + "_span");
				if (treeNode.editNameFlag || $("#addBtn_" + treeNode.tId).length > 0)
					return;
				var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
						+ "' title='add node' onfocus='this.blur();'></span>";
				sObj.after(addStr);
				var btn = $("#addBtn_" + treeNode.tId);
				if (btn)
					btn.bind("click", function() {
						$('#addform')[0].reset();
						// 解决模态框与ztree JQuery版本不兼容的问题
						showModal();
						$("#modalAddBtn").click(function() {
							var zTree = $.fn.zTree.getZTreeObj("treeDemo");
							var nodeId = uuid();
							var newNode = {};
							newNode.id = nodeId;
							newNode.pid = treeNode.id;
							newNode.name = $("#name").val();
							if ($("#name").val() == null) {
								newNode.descr = $("#name").val();
							} else {
								newNode.descr = $("#descr").val();
							}
							newNode.status = $("#status1").val();
							zTree.addNodes(treeNode, {
								id : nodeId,
								pid : treeNode.id,
								name : newNode.name,
								descr : newNode.descr,
								status : newNode.status
							});
							var nodeJson = JSON.stringify(newNode);
							$.ajax({
								type : "post",
								url : "/shopping/manager/insertCategory",
								data : newNode,
								success : function(data) {
									$(".panel-body").html(data);
								}

							});

						});
						return false;
					});
			};

			function removeHoverDom(treeId, treeNode) {
				$("#addBtn_" + treeNode.tId).unbind().remove();
			};

			/*增删改end*/

			/*加载数据，创建tree*/
			var zNodes = null;
			$(function() {
				//alert("zNodes")
				$.ajax({
					type : "post",
					url : "/shopping/manager/listCategories",
					dataType : "json",
					async : false,//同步
					success : function(result) {
						zNodes = eval(result);
						//console.log(zNodes);
					}
				});
			});
			var code;

			function setCheck() {
				var zTree = $.fn.zTree.getZTreeObj("treeDemo"), py = $("#py").attr(
						"checked") ? "p" : "", sy = $("#sy").attr("checked") ? "s" : "", pn = $(
						"#pn").attr("checked") ? "p" : "", sn = $("#sn")
						.attr("checked") ? "s" : "", type = {
					"Y" : "s",
					"N" : "s"
				};
				zTree.setting.check.chkboxType = type;
				showCode('setting.check.chkboxType = { "Y" : "' + type.Y + '", "N" : "'
						+ type.N + '" };');
				zTree.expandAll(true);
			}
			function showCode(str) {
				if (!code)
					code = $("#code");
				code.empty();
				code.append("<li>" + str + "</li>");
			}

			$(document).ready(function() {
				$.fn.zTree.init($("#treeDemo"), setting, zNodes);
				setCheck();
				$("#py").bind("change", setCheck);
				$("#sy").bind("change", setCheck);
				$("#pn").bind("change", setCheck);
				$("#sn").bind("change", setCheck);

			});
		
	
</script>
```