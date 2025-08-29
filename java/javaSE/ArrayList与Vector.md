tags: #java #arrayList #vector

## Vector & ArrayList 的主要区别 
- **1）同步性**:Vector是线程安全的，也就是说是同步的 ，而ArrayList 是线程序不安全的，不是同步的。 

- **2）数据增长**:当需要增长时,Vector默认增长为原来一倍 ，而ArrayList却是原来的50%，这样,ArrayList就有利于节约内存空间。 
- 如果涉及到堆栈，队列等操作，应该考虑用Vector，如果需要快速随机访问元素，应该使用ArrayList 。

### 扩展知识：
#### 1、 Hashtable & HashMap 

Hashtable和HashMap它们的性能方面的比较类似 Vector和ArrayList，比如Hashtable的方法是同步的,而HashMap的不是。

#### 2. ArrayList & LinkedList

ArrayList的内部实现是基于内部数组Object[],所以从概念上讲,它更象数组，但LinkedList的内部实现是基于一组连接的记录，所以，它更象一个链表结构，所以，它们在性能上有很大的差别：   

从上面的分析可知,在ArrayList的前面或中间插入数据时,你必须将其后的所有数据相应的后移,这样必然要花费较多时间，所以,当你的操作是在一列数据的后面添加数据而不是在前面或中间,并且需要随机地访问其中的元素时,使用ArrayList会提供比较好的性能； 

而访问链表中的某个元素时,就必须从链表的一端开始沿着连接方向一个一个元素地去查找,直到找到所需的元素为止，所以,当你的操作是在一列数据的前面或中间添加或删除数据，并且按照顺序访问其中的元素时，就应该使用LinkedList了。