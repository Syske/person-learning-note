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

// 如果删除这里的*就是值传递了，实际上并不会改变Vertex对象的值，不过对应的调用的时候就不能传指针了（也就是`&v`），而是将对象直接传入（不加`&`）
func Scale(v *Vertex, f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {

	v := Vertex{3, 4}
	Scale(&v, 10)
	fmt.Println(v)

}

```

但是，如果方法在定义的时候，要求的参数是对象（而不是指针），则只能传对象，否则会报编译错误：

```go
// 对象作为接收者
func (v Vertex) AbsFunc() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
func main() {
	v1 := Vertex{3, 4}
	fmt.Println(v1)
	p2 := &v1
	// 这里是正常的
	fmt.Println(Abs(v))
	// 这里会报编译错误
	fmt.Println(Abs(p2))

}

```

![](https://syske-pic-bed.oss-cn-hangzhou.aliyuncs.com/imgs/3bf9f5c6-8434-4151-9a9f-36f96d4eb478.jpg)

总结一下：

**作为接收者：**
作为接收者时，指针或者对象都可以作为接收者调用方法，但是
- 如果定义方法时，接收者为指针：
	- 用**指针**作为接收者调用方法，相应的修改**会**直接修改指针指向的数据
	- 用**对象**作为接收者调用方法，相应的修改**不会**改变对象对应的属性
- 如果定义方法时，接收者为对象（这种说法应该不合理），不论是通过指针还是对象调用方法，方法内的修改不会改变对象的数据

**作为参数：**
- 如果定义方法时，参数类型为指针，则即可传指针也可以传对象，但是传指针是**引用传参**，所有修改都会修改对象的数据，传对象则是**值传参**，方法内的修改不会改变传递对象的数据
- 如果定义方法时，参数类型为对象，则只能传对象，传指针会报编译错误