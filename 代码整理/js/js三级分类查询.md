tags: [#code, #三级分类]

# 1、html
```html
<div class="form-group">
    <label for="memberprice" class="col-sm-2 control-label">商品分类</label>
    <div class="col-sm-3">
    	<select class="form-control" id="first_leve">
    		<option>全部</option>
    	</select>
    </div>
    <div class="col-sm-3">
    	<select class="form-control" id="second_leve">
    		<option>全部</option>
    	</select>
    </div>
    <div class="col-sm-3">
    	<select class="form-control" id="thrid_leve">
    		<option>全部</option>
    	</select>
    </div>
</div>
```
# 2、js

```js
	function beforeEdit() {
		var eles = [ "#first_leve", "#second_leve", "#thrid_leve" ];
		ajaxCategories(eles);
	}

	/*加载数据，创建tree*/
	var zNodes = null;
	// /manager/resultCategoryListAndChildren
	function ajaxCategories(eles) {
		$.ajax({
			type : "post",
			url : "/shopping/manager/listCategories",
			dataType : "json",
			async : false,//同步
			success : function(result) {
				zNodes = eval(result);
				cret(zNodes, eles);

			}
		});
	}

	function cret(zNodes, eles) {
		var firstNodesArray = new Array();
		var secondNodesArray = new Array();
		var thridNodesArray = new Array();
		var j = 0;
		var k = 0;
		var l = 0;
		var firstselector = eles[0] + " option:not(:first)"
		$(firstselector).remove();
		for (var i = 0; i < zNodes.length; i++) {
			if (zNodes[i].level == '1') {
				firstNodesArray[j] = zNodes[i];
				var optionFirst = $(
						"<option value="+ zNodes[i].id +"></option>").text(
						zNodes[i].name);

				$(eles[0]).append(optionFirst);
				j++;
			}
			if (zNodes[i].level == '2') {
				secondNodesArray[k] = zNodes[i];
				k++;
			}
			if (zNodes[i].level == '3') {
				thridNodesArray[l] = zNodes[i];
				l++;
			}

		}

		var firstId = $(eles[0]).val()
		var secondId = $(eles[1]).val()
		var thridId = $(eles[2]).val()
		$(eles[0]).change(function() {
			addOption(eles[1], eles[0], secondNodesArray);
		});

		$(eles[1]).change(function() {
			addOption(eles[2], eles[1], thridNodesArray);
		});

		$(eles[2]).change(function() {
			firstId = $(eles[2]).val();
		});
	}

	function addOption(mainSelect, pSelector, NodesArray) {
		var selector = mainSelect + " option:not(:first)";
		$(selector).remove();
		var pId = $(pSelector).val();
		for ( var i in NodesArray) {
			if (pId == NodesArray[i].pid) {
				var options = $(
						"<option value="+ NodesArray[i].id +"></option>").text(
						NodesArray[i].name);
				$(mainSelect).append(options);

			}
		}
	}
```