
### 作为接收者

这里的接收者，我理解类似`java`的实例对象，不论是方法本身定义的接收者是还是指针，都是支持对象或者指针作为接收者的，但是需要注意的是，如果指针作为接受对象，会修改对象的数据，对象作为接受者则不会（我理解还是值传递和引用传递的区别）：

```go
package main

import (
	"fmt"
	"math"
)

type Vertex struct {
	X, Y float64
}

// 指针作为接收者时可以传对象或者指针
func (v *Vertex) ScaleFunc(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {
	v1 := Vertex{3, 4}
	v1.ScaleFunc(10.0)
	// 这里打印的值没有变，说明对象的属性没有被修改
	fmt.Println(v1)
	p2 := &v1
	p2.ScaleFunc(10)
	// 这里变了，是因为上面传的是指针
	fmt.Printf("p2=%v\n", v1)
}
```

如果方法本身是对象作为接收者，不论传的是对象还是指针，数据都不会被修改：
```go
// 对象作为接收者
func (v Vertex) ScaleFunc(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {
	v1 := Vertex{3, 4}
	v1.ScaleFunc(10.0)
	// 这里打印的值没有变，说明对象的属性没有被修改
	fmt.Println(v1)
	p2 := &v1
	p2.ScaleFunc(10)
	// 这里和上面打印结果一样
	fmt.Printf("p2=%v\n", v1)
}

```

### 作为参数

在`java`语言中，虽然我们经常听到`NPE`，但是其实对于指针的操作并不会涉及，对于`object`类型的数据，我们传的其实就是对象的指针，在`golang`也是如此，只是在`golang`中，我们需要显式地传递指针，否则就是值传递，导致数据修改其实对传入地对象（`struct`）并不生效：

```go
package main

import (
	"fmt"
	"math"
)

type Vertex struct {
	X, Y float64
}

func Abs(v Vertex) float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

// 如果删除这里的*就是值传递了，实际上并不会改变Vertex对象的值，不过对应的调用的时候就不能传指针了（也就是`&v`），而是将对象直接传入（不加`&`）
func Scale(v *Vertex, f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {

	v := Vertex{3, 4}
	Scale(&v, 10)
	fmt.Println(v)
	fmt.Println(Abs(v))

}

```

总结一下：
- **传指针**，相应的修改会直接修改指针指向的数据，是**引用传递**
- **传对象**，传的是对象的值，是**值传递**