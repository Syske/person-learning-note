
拿到`canvas`对象

```js
var canvas = $('canvas')
```

转`base64`
```js
var canvasData = canvas.toDataURL('image/png')
```

之后将`base64`转图片即可