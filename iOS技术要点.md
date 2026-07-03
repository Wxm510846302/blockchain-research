# iOS技术要点

## UI视图

### UITableView相关

- 重用机制

	- cell = [tableview dequeueReusableCellWithIdentifier:identifer];
重用池（A）

	- [字母索引条](https://www.bilibili.com/video/BV1X1421b7Cb?spm_id_from=333.788.player.switch&vd_source=e856e916730fb430d470384f2ffe041f&p=4)

- 数据源同步

	- 主线程删除UI影响数据源、子线程删除数据源

	- 解决方法1：并发访问，数据拷贝

		- 主线程记录删除操作，子线程同步删除操作

	- 解决方法2：串行访问

		- 创建串行队列，子线程请求数据后，对数据进行排版操作在串行队列中完成，主线程删除数据等串行队列的上一步操作完成后再进行。

### 事件传递&视图响应

- UIView和CALayer

	- MyView有CALayer类型的属性layer和backgroundColor。具体的显示内容是CALayer的contens属性内容。

	- UIView管理子视图的层级和布局，以及负责处理触摸事件，参与响应链
CALayer负责内容渲染，contents内容，处理底层图形操作。
UIView是电视机，CALayer是显示屏

	- 采用了系统设计的单一职责原则

- 事件传递怎么找到C2的响应？

	- -(UIView|*)hitTest:(CGPoint)point withEvent:(UIEvent*)event;
-(BOOL)pointInside:(CGPoint)point withEvent:(UIEvent*)event;

	- 流程，倒序递归遍历子视图

		- // 遍历子视图，先转换坐标到子视图坐标系，然后在调用hitTest方法。
        CGPoint convertedPoint = [self convertPoint:point toView:subview];

	- 方形按钮指定区域接受事件响应

		- 重写以上提到的两个方法。

		- 重写以上提到的两个方法。

- 视图事件响应

	- - (void)touchesBegan:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event{}
- (void)touchesMoved:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event{}
- (void)touchesEnded:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event{}

	- 如果传递到UIApplication仍然没有处理，事件将会被放弃。

### 图像显示原理

- 流程

	-  

		- CPU

		- GPU

- CoreAnimation原理

	- 高性能、异步、基于图层（Layer）树的动画系统。Core Animation 是一个将 UI 层渲染和动画任务从主线程分离出去，由系统底层高效执行（包括 GPU 加速）的动画与合成引擎。

### UI卡顿、掉帧原因

- 16.7ms内没有刷新下一帧画面

- 滑动优化方法【减轻CPU/GPU压力，减少时间】

	- CPU
1.对象创建、调整、销毁 放到子线程
2.预排版（布局计算、文本计算）放到子线程
3.预渲染（文本等异步绘制，图片解码等）

	- GPU
1.纹理渲染（避免触发离屏渲染）
2.视图混合（多个视图层层叠加）用 drawRect: 替代多个子视图组合，如需交互，需手动实现点击检测：touchesBegan方法内检测是否点击了目标元素

		-  

### UI绘制原理/异步绘制

- 流程图，在当前主线程的RunLoop要结束时调用CALayer display

	- 系统绘制流程，uiview drawrect 

	- 异步绘制就是基于系统开的口子
-实现【layer.delegate displayLayer】方法。
通过调用CG函数
1.代理负责生成对应的bitmap
2.设置该bitmap为layer.contents属性的值

### 离屏渲染

- 在屏渲染
当前屏幕渲染，指的是GPU的渲染操作是在当前用于显示的屏幕缓冲器中进行

- 离屏渲染
指的是GPU在当前屏幕缓冲区以外新开辟的一个缓冲区进行渲染操作

	- 何时触发？
1.设置圆角（当和maskToBounds一起使用时）
2.图层蒙版
3.阴影
4.光栅化

		- 根本原因是多图层叠加处理时会导致
只是Contents设置圆角也不一定会触发

	- 为何要避免？
1.会增加GPU工作量
2.创建新的渲染缓冲区
3.触发GPU OpenGL多通道渲染管线，将多通道渲染结果做合成，会涉及上下文的切换，额外开销可能导致CPU和GPU处理总时间超过16.7ms，出现UI卡顿、掉帧。

		- 程序上下文”（Program Context）是操作系统和 CPU 层面中的一个概念，指的是在某个时刻，操作系统为了能够中断并恢复一个程序或线程的执行，需要保存的该程序的所有相关状态信息。“轮流”使用 CPU时所必要的操作。

### 方法对比

### 动画的执行

- [iOS 动画的启动必须在主线程，但实际渲染过程在后台线程执行。](https://juejin.cn/post/6844903763011076110)

- 不同类型动画的线程处理

	- UIView 动画即使你在后台线程调用 UIView.animate，系统也会回到主线程执行视图更新。

	- Core Animation (CALayer 动画)
 主线程提交，渲染在后台线程RenderServer（GPU）

	- 动画性能优化技巧

- UIKit: 包含各种控件，负责对用户操作事件的响应，本身并不提供渲染的能力
Core Animation: 负责所有视图的绘制、显示与动画效果
OpenGL ES: 提供2D与3D渲染服务
Core Graphics: 提供2D渲染服务
Graphics Hardware: 指GPU
动画本质上是由 Core Animation 负责

## OC语言

### 分类

- 分类做了什么？（Category）
1、 给现有类添加实例方法和类方法
2、分解体积庞大的类文件
3、把Framework的私有方法公开

	- 特点
1、 运行时决议
2、可以为系统类添加分类

	- 可以添加哪些内容？
1、 实例方法
2、类方法
3、协议
4、可以声明类属性【需要手动实现存储和访问逻辑】
5、分类无法直接添加实例属性：因为分类不能向类中添加实例变量（ivar）。通过关联对象在分类中“伪添加”实例属性

		- 分类不参与类的内存布局，对象布局是在编译时由类的 主实现
在运行时动态将方法添加到类中，并不会改变类的结构，所以不能直接添加实例属性

- 源码 objc-runtime-940.4版本

	- name：指向分类所属的原始类名的字符串
cls：运行时加载分类后，此字段会指向原始类的类对象。初始时可能为空，动态加载时由运行时填充
WrappedPtr：分类中添加的实例方法和类方法，WrappedPtr 封装指针，用于处理 ARM64e 架构的指针认证（Pointer Authentication），增强安全性。
protocol_list_t*：分类遵循的协议列表。这些协议会被合并到原始类的协议列表中。
property_list_t*：分别存储分类中添加的实例属性和类属性。仅存储声明，不生成实例变量或方法实现

- 最后编译的分类方法生效：
后编译的分类在 cats_list 中靠后，合并时方法被前置，优先级最高。

覆盖规则：
运行时按方法列表顺序查找，后加载的方法覆盖先加载的方法。

分类方法是以 method_list_t 的形式追加到类的 class_rw_t::method_array_t 中

主类方法优先级最低：
主类的方法在所有分类方法之后合并，因此优先级最低。

- 流程图

### 关联对象

- id objc_getAssociatedObject(id object.const void*key);
void objc_setAssociatedObject(id object.const void*key,id value,objc_AssociationPolicy policy);
void objc_removeAssociatedObjects(id object);

	- 关联对象的数据结构

		-  

- 成员变量被添加到哪里了？
没有添加到元宿主类，而是有AssociationsManager管理在AssociationsHashMap存储。所有对象的关联内容都在同一个全局容器中，运行时动态绑定

	- 操作 `AssociationsHashMap` 时使用自旋锁（`spinlock_t`）保证线程安全。

- 核心api

### 扩展、代理

- 一般用扩展做什么？
1、 声明私有属性和方法
2、声明私有成员变量
属性是对成员变量的封装，提供存取方法和内存管理

	- 特点
1、 编译时决议
2、以声明形式存在，多数情况下寄生于宿主类的.m文件中
3、不能为系统类添加扩展

- 代理（delegate）是什么？
1、是一种软件设计模式，在iOS中以@protocol形式体现
2、传递方式一对一
可以定义哪些内容？
方法和属性

	- 流程

	-  

- 代理一对多的方式

	- 1、封装 MulticastDelegate 类，使用 NSHashTable.weakObjects() 避免强引用，防止内存泄漏。

	- 2、定义协议（事件）

	- 3、使用方式

	- 4、添加多个监听者

	- 5、使用

### NSNotification

- 1、是使用观察者模式来实现的用于跨层传递消息的机制
2、传递方式为一对多。
3、通知的发送是同步的，但通知的处理可以是同步或异步的，取决于监听者的实现。

	-  

- 如何实现通知机制？
通知中心维护一个表【Notification_Map】两层hash表，内层哈希表：Key=发送对象，Value=观察者链表

	-  

### KVO、KVC

- 1、KVO是Key-value observing的缩写
2、KVO是OC对观察者设计模式的又一实现
3、Apple使用了isa混写（isa-swizzling）来实现KVO

	- isa混写方式，调用addobserver时，系统在运行时动态生成一个A类的子类，isa指向新的类

		-  

		-  

- KVC是key-value coding的缩写
KVC（键值编码）是一种通过字符串 key 访问对象属性的机制
-(id)valueForKey:(nsstring*)key;
-(void)setValue:(id)value forKey:(nsstring*)key

	- 如果知道对象属性的话，直接调用setvalueforkey可以直接改变其值。

	- getvalue流程

		- setvalue流程

- 1、通过KVC设置value 能否使KVO生效？为什么?
可以生效
实现原理：最终会调用到setter方法
2、通过成员变量直接赋值value能否生效？
不能生效（_value += 1）

	- 仿写kvo

### 属性关键字

- 1、原子性
atomic
保证成员属性线程安全。【对数组属性的存取时保证，但是对数组的加减不保证】。
nonatomic
2、引用计数
retain/strong
assign/unsafe_unretained
copy
weak

	- assign特性
1、通常用于基本数据类型，比如int、float，或者结构体
2、修饰对象类型时，不改变其引用计数
3、会产生悬垂指针

	- weak特性
1、不改变被修饰对象引用计数
2、所指对象在被释放后指针自动置为nil

		- 如何实现的？

- copy
可变对象的copy和mutableCopy都是深拷贝
不可变对象的copy是浅拷贝，mutableCopy是深拷贝
copy方法返回的都是不可变对象

	- 浅拷贝，会增加对象的引用计数，并没有分配内存

	- 深拷贝
不会增加被拷贝对象的引用计数，产生了新的内存分配

### MRC下如何重写retain修饰变量的setter方法？
必须进行不等判断，否则原来的obj被释放了无法再retain

### struct 和class区别

-  

-  

- struct如果在内部方法修改属性，需要添加mutating关键字修饰Swift 会将带有 mutating 的方法，自动把 self 视为 inout 参数

-  

-  

## [RunTime](https://www.bilibili.com/video/BV1X1421b7Cb?spm_id_from=333.788.videopod.episodes&vd_source=e856e916730fb430d470384f2ffe041f&p=6)

### Runtime 就是 Objective-C 的运行时机制，是一个 C 语言写的动态库 libobjc.A.dylib，它负责在程序运行期间进行类、对象、方法等操作

### runtime数据结构
对象、类对象、元类对象
cache_t是一个结构体，内部维护一个类似哈希表的数据结构，内部有bucket_t，指针指向一个数组。
class_rw_t下的methods等元素都是二维数组【准确说是一个嵌套链表/多级指针结构】method_array_t类型的methods

struct class_rw_t {
    ...
    method_array_t methods; 
// 方法列表（注意是多个method_list_t）
    ...
};
typedef Array<method_list_t> method_array_t;

struct method_list_t {
    uint32_t entsizeAndFlags;
    uint32_t count;
    method_t first; // 实际上是一个数组的开始
};

数组内的第二层数组元素是method_t类型的元素
class_ro_t下的元素是一维数组。


Read-Only：类在编译期就已确定的只读信息，如方法名、属性、父类名等
Read-Write：类在运行时可能发生变化的信息，比如方法缓存、动态添加方法、分类扩展方法等


如果 methods 是一个单一数组，那么每次加载分类、添加方法时都要进行数组拷贝、重建索引，效率低。
设计成多个 method_list_t 的集合后：
加载新方法时只需要 append 一个新的列表块。分类方法是以 method_list_t 的形式追加到类的 class_rw_t::method_array_t 中
查找时按顺序遍历 method_list_t，直到找到为止。
更加灵活、动态、安全。
多个列表块按照加载顺序组成链表，后加载的优先级高（如 Category 方法可以覆盖原始类方法）。

- OC中的id 类型的对象都是对应runtime的objc_object结构体，isa_t是共用体

	- OC中的Class类，对应runtime中的objc_class结构体。Class也是个对象，是类对象。
bits 定义的变量，属性和方法、协议都在这里。

- OC中的isa_t对应runtime中的isa指针

	- 类对象存储实例方法列表等信息
元类对象存储类方法列表等信息
类对象和元类对象都是objc_class数据结构的，继承objc_object所以都有isa指针。

	- isa指向
调用实例的实例方法，调用实例的isa指针到类对象中去查找。调用类对象的方法，是调用类对象的isa指针到元类对象中去查找该方法。

- 分类的方法列表以及class_rw_t中的方法列表中的method_t数据结构

- cache_t方法缓存，
1.用于快速查找方法执行函数
2.是可增量扩展的哈希表结构
3.是局部性原理的最佳应用

	- cache_t结构是由bucket_t结构体组成的。key是SEL，value是IMP

- 实例对象、类对象、元类对象
类方法在所有元类中找均不到时，会在根类对象中寻找同名实例方法。[MyClass testMethod];找不到就会在 NSObject 本类（也就是根类）中查找同名实例方法

	- 一般常用类的继承关系

		- 根类 NSObject
所有类的最终基类
提供基本的内存管理机制（引用计数）
实现 retain, release, autorelease 方法
提供运行时系统接口（如 isKindOfClass:, respondsToSelector:）
实现对象的基本行为（如 description, hash, isEqual:）

		- 特殊根类 NSProxy
用于实现消息转发和虚代理
典型应用场景：
延迟加载
分布式对象
面向切面编程(AOP)

			- NSTimer为了避免出现循环引用，使用中间类weak引用target。这个中间类建议用NSProxy。
那么原因就是这个类专门用于实现消息转发和虚代理
与NSObject区别就是省去了objc_sendMsg中的一些耗时。效率更高。
但是Swift 不支持直接继承 NSProxy虽然你可以在 Swift 中声明 class XMProxy: NSProxy，但： Swift 类型系统和 NSProxy 的动态转发机制不兼容Swift 中继承 NSProxy 很容易崩溃或行为异常

### 消息传递机制

- class是实例方法，在nsobject里有实现，结果都是phone，super只是跳过了phone类的方法查找。接收者还是phone

- void objc_msgSend(void/*id self，SEL op , ...*/)
void objc_msgSendSuper(void/*struct objc_super *super，SEL op , ...*/)
super 结构体里有receiver。接收者仍然是当前对象。

- 流程图

	- 缓存命中根据hash查找，当前类方法列表是否命中根据方法是否已排序判断，是则采用二分法，不是则采用一般遍历法。逐级父类根据superclass指针，再次重复以上步骤

### 方法缓存

- 缓存查找步骤
通过hash函数：f(hash) = hash & mask 位与运算。查找给定选择器因子，找到bucket_t在数组中的位置。mask必须是 2 的幂减 1。所以哈希表设计时通常将容量 capacity 设为 2 的幂。
如果冲突怎么办？（同一个 index 上已经有了其他 key）
Runtime 使用 线性探测（Linear Probing index = (hash + i) & mask ）或 Robin hood hash
即：如果 index 上的 key 不是目标 sel，就试下一个：index + 1，再 index + 2，直到找到目标或遇到空位

	- Robin hood hash

- 当前类中查找
对于已排序好的列表，采用二分查找算法查找方法对应执行函数。
对于没有排序的列表，采用一般遍历查找方法对应执行函数。

	- 父类逐级查找

### 消息转发流程

- 1.  -(bool)resolveinstanceMethod：1. 动态添加方法的实现
2. -(void)forwardingTargetForSelector: 2. 转发给别人
3. -(methodSignatur)methodSignatureForSelector:3. 获取签名完整消息转发
4.-(void)forardInvocation:4. 自定义转发调用，
进入消息转发流程后，可以动态添加方法，防止crash

### Method-Swizzling

- 此时已经做了方法替换，所以调用otherTest，就是调用了test。
场景：Hook UIViewController 的 viewWillAppear: 方法，在不修改每个子类的前提下实现统一日志打印（用于埋点或统计），常见做法是使用 Method Swizzling（方法交换）

### 动态添加方法和解析

- 添加

	- 第一种

	- 第二种

- 解析

- 能否向编译后的类中增加实例变量？不能
可以在动态添加后的类中增加实例变量。
但可以通过 关联对象（Associated Object） 的方式，为编译后的类“模拟”出实例变量

	- 示例：动态创建一个类并添加 ivar
objc

Class NewClass = objc_allocateClassPair([NSObject class], "MyDynamicClass", 0);
BOOL success = class_addIvar(NewClass, "_myVar", sizeof(NSString *), log2(sizeof(NSString *)), @encode(id));

if (success) {
    objc_registerClassPair(NewClass);

    id instance = [[NewClass alloc] init];
    Ivar ivar = class_getInstanceVariable(NewClass, "_myVar");
    object_setIvar(instance, ivar, @"Hello");

    NSLog(@"%@", object_getIvar(instance, ivar)); // 输出 Hello
}


### isa指针分为：指针类型的isa 和 非指针类型的isa

## 内存管理

### iOS 图片所占内存的计算方式

- 内存大小 = 图片宽度 × 图片高度 × 每像素字节数

- 图片内存优化

### 内存布局结构

### 内存管理方案

- TaggedPointer （优化 小对象（如 NSNumber, NSDate, NSString 等）对象数据直接编码在指针值中，不需要额外申请内存。）

- NONPOINTER_ISA（将多种元数据压缩存储到 isa 指针中）

	- 第一位1代表非常用指针，存储了内存管理内容。0代表isa指针只存了当前类对象的地址。
第二位是否有关联对象
第三位当前对象是否使用了c++内容
接下来的33位表示当前对象的类对象的指针地址。

	-  

- 散列表（引用计数表，弱引用表，自旋锁控制并发访问）SideTables

	- hash表结构

	-  

		- 自旋锁Spinlock_t 忙等的锁，被其他线程获取，那么当前线程会不断查询锁的状态。适用于轻量访问

		- 引用计数表（hash表）

			- 引用计数的数据结构

		- 弱引用表（hash表）

	- 为何不是一个sidetable表？
效率问题，多线程引用情况需加锁

		- 分离锁方案，提高效率

		- StripedMap<SideTable> 是多个 SideTable 的集合（类似哈希桶数组），用于：
将对象分散到多个 SideTable，以避免锁竞争；
提高引用计数、weak 管理等操作的并发性能；

- ARC

	- 🈶编译器和运行时共同协作的结果，编译器自动插入retain和Release

		- 编译器插入调用逻辑（什么时候保留、什么时候释放）；

Runtime 提供执行支持（怎么 retain/release/weak 处理）；

二者缺一不可，ARC 无法仅由编译器或 Runtime 独立实现。

- MRC

	- 特有方法是红色方法

### 引用计数管理

- 经过两次hash查找，非+=1 是因为前几个字节是别的含义

	- 总结：两次哈希的必要性
并发优化：第一级哈希减少锁竞争

内存效率：二级结构优化小对象存储

性能平衡：

单次查找平均 < 50ns

比全局单哈希表快 3-5 倍（在 8 核设备上）

可扩展性：支持数万个对象的高效弱引用管理

- dealloc实现

	- 为何要进行5个条件判断？

	- 第一步

		- 第二步

			- 第三步

### 弱引用管理

- 流程图

	-  

- 添加weak指针
hash算法快速查找对象指针所在数组中的位置，然后判断是否正确，否则继续线性探测查找

	- hash查找之后，判断对应的weak地址数组，有就插入，没有就创建一个，再添加。weak指针数组元素个数默认是4

		- 如果引用数 ≤ 4，直接用 inline_referrers[4] 存
超过 4，就动态分配堆内存，转移所有引用到新的 referrers 数组，referrers（使用哈希 + 探测冲突处理）

- 清除weak指针，同样使用hash查找快速找到弱引用表中的弱引用数组

### AutoReleasepool

- 实现原理

	-  

	- 数据结构，链表的parent和child都怎么指向？
指向上一个和下一个poolpage
next不是链表的 next，而是当前 page 中下一个可用对象槽位的指针（即对象栈的“栈顶”）
哨兵对象（即 POOL_BOUNDARY）实际上是放在每个 Page 的对象栈区域内（也就是 next 指向的数组起始处）

	- 发送了Release消息后，next重新指向id obj(3)

- 为何可以嵌套使用？
多次插入哨兵对象

	- 每一层 @autoreleasepool 都对应一个新的「自动释放池栈帧」，并使用「哨兵对象」来分隔管理。你提到的「多次插入哨兵对象」正是它能嵌套的核心机制。
自动释放池的本质是一个栈结构，每次进入 @autoreleasepool，都会：
push 一个新的 pool（插入哨兵对象）；
在这个 pool 中，记录所有自动释放对象；
离开 @autoreleasepool 时，drain 清理该帧内的所有对象（pop 到上一个哨兵为止）；

- 释放时机

	- 注意主线程的自动释放池

		- 主线程自动释放池在RunLoopp 即将休眠时释放
每次事件处理都在独立的池中进行

### 循环引用

- 自循环引用

- 相互循环引用

	- 代理

	- block

	- NSTimer

		- RunLoop也会强引用NSTimer，这点需要注意

	- 大环引用

- 多循环引用

- 破除思路

	- 避免产生循环引用

		- __weak
__block
__unsafe__unretained

		-  

		-  

		- __unsafe__unretained

	- 在合适的时机手动断环

### 常见问题

## Block

### Block本质

- block本质就是将函数及其执行上下文封装起来的结构体形式的对象
它既可以像函数一样调用，又可以像对象一样传递和存储。

- Block（块）是 Objective-C 和 C 中的一种将函数和数据封装在一起的结构体，本质上是一个结构体，并自动捕获上下文变量。其底层实现涉及 结构体封装、函数指针、自动变量捕获 和 内存管理（栈、堆、全局）。

### 截获变量

- 笔试真题

- 局部变量

	- 基本数据类型

		- 截获其值
默认情况下，block 会将捕获的变量复制一份（值捕获）

	- 对象类型

		- 连同所有权修饰符一起截获

- 静态局部变量

	- 以指针形式截获 

		- 如果在block调用之前，修改了其值，那么block内部会拿到最新值

- 全局变量

- 静态全局变量

### __block修饰符

- 赋值不是使用

	- 不需要，block只是使用了变量

	- 需要给array添加修饰符

	- 静态局部变量、全局变量、静态全局变量赋值时不需要__block修饰符

	- 局部变量赋值时需要__block修饰符

		- __block修饰的整型变量变成了对象

			- __forwarding指针是什么作用？

- __block 变量转换为一个 特殊结构体
变量被封装在一个结构体里（不是简单栈变量）
block 捕获的是这个结构体的地址（共享引用）
如果 block 被拷贝（从栈到堆），结构体也随之移动（支持 __forwarding）

	-  

### Block内存管理

- Block 有 3 种类型（取决于变量捕获方式）

	-  

	-  

### 循环引用

- MRC模式下，不会产生循环引用
ARC模式下，会产生循环引用

	- 在return前，将blockSelf = nil会断开，但是在不调用_blk的情况下不会断开大环。

###  

### Swift中的block和OC中的block

- 语法

- 内存管理

- 变量捕获

-  

-  

### __weak和__block的区别
__block最初是分配在栈上的结构体对象，只有当 block 本身从栈复制到堆时（即被“拷贝”时），__block 变量也会被复制到堆在 ARC 下：会强引用对象（可能导致循环引用）
编译器会将 __block 变量转换为一个 特殊结构体指针。

-  

- inout关键字基本原理，逃逸闭包不能捕获 inout 参数，参数仅在函数执行期间有效

## 多线程

### 避免主线程阻塞，提升 UI 响应性

利用多核 CPU 资源并发处理

处理耗时任务（如网络请求、IO、图像处理等）

### GCD

- 同步/异步 和 串行/并发

	- 死锁的原因是【队列引起的循环等待】主队列是串行队列，即使是async也不会新开线程，也会在主线程执行，但是由于是异步，不需要立即执行，所以不会造成死锁。

	- performSelector需要在RunLoop下执行。默认GCD的RunLoop没有开启。

	- async：可以稍后执行
sync：立即执行

	- 关于线程是否创建

- dispatch_barrier_async

	- 使用GCD多读单写的实现方式，所以叫栅栏

		- 多线程读的时候，需要立即获取，所以用sync

		- 注意sync时死锁

		- 注意使用范围，要添加的队列

			-  

- dispatch_group

	- 三个任务并发完成后，再执行第四个任务
dispatch_group_async 本身就封装了 enter 和 leave。相当于dispatch_group_enter(group);
dispatch_async(queue, ^{
    // 任务代码
    dispatch_group_leave(group);
});

	- 调度组允许您跟踪一组任务，并在所有任务完成时收到通知。

- 基本原理，源码

- 原理和特性：
1.按需创建/销毁线程
2.线程缓存机制 (有限重用)
3.基于队列的优先级系统
4.手动内存管理

### NSOperation/NSOperationQueue

- NSOperation：表示单个任务单元

NSOperationQueue：管理操作执行的队列

NSBlockOperation：基于闭包的操作

NSInvocationOperation：基于选择器的操作（Swift中不可用）

- 优势
1、 添加任务依赖
2、任务执行状态的控制
3、最大并发量的控制

	- isReady、isExecuting、isFinished、isCanceled四种状态。
重新start方法可以自行控制任务状态，达到多个异步网络请求相互依赖情况下依次执行的要求

	- 系统通过KVO的方式来移除一个isFinished为yes的NSOpreation的

- 有几种方式回到主线程中调用NSLog

	- 在 Operation 中显式回到主线程，在自定义的NSOpreation的main函数中调用dispatch_async(dispatch_get_main_queue(), ^{})
或使用 performSelectorOnMainThread

	- 使用OperationQueue.main.addOperation
OC中是[[NSOperationQueue mainQueue] addOperationWithBlock:^{
        
    }];

	- 使用 completionBlock + 回到主线程

- GCD对比

- 自定义Operation的话

### Thread

- 启动流程以及线程常驻

### SwiftConcurrency

- [从 Swift5.5开始引入，Swift 引入了协程机制 async/await 和 Task
 actor 内部实现了数据访问的同步机制](https://juejin.cn/post/7076738494869012494)

	- 特性：
固定大小线程池 (通常 = CPU 核心数)
任务挂起时不阻塞线程
自动任务优先级管理
结构化并发防止任务泄漏

- 性能对比
1. 上下文切换成本
Swift Concurrency: ~100 纳秒 (挂起/恢复任务)
GCD: ~1-10 微秒 (线程切换)
差异: Swift Concurrency 比 GCD 快 10-100 倍

2. 内存开销 (10,000 个并发任务)
Swift Concurrency: ~5MB (500 字节/任务)
GCD: ~5GB (512KB/线程)
差异: Swift Concurrency 内存效率高 1000 倍

3.并行任务吞吐量测试 (10,000 个睡眠任务)
Swift Concurrency: ~50ms 完成
GCD: ~500ms 完成 (10 倍慢于 Swift Concurrency)

	-  

### 线程同步、资源共享

### 互斥锁、自旋锁、递归锁、条件锁、信号量等

- NSRecursiveLock
递归锁

	- 通过递归锁解决死锁问题

	- 可以重入，比普通互斥锁慢10-15%

- @synchronized  对象关联的递归互斥锁 
比NSLock慢4-8倍（需两次哈希查找+锁管理）
线程同步的关键字

	- 一般在创建单例对象的时候使用，多线程创建保持唯一。但相较于 dispatch_once 来说，效率更低。
1. 写文件
2.保护静态变量

- 各个锁的对比

- 自旋锁：
`OSSpinLock`（已废弃，因为优先级反转问题），`os_unfair_lock`（替代OSSpinLock，非忙等但也不是传统自旋锁，而是休眠等待）

	- OSSpinLock自旋锁
循环等待询问，不释放当前资源

	- os_unfair_lock在无竞争时会避免上下文切换，但在竞争激烈时会触发上下文切换
先短暂自旋1000次，约1μs，后休眠

- 互斥锁 (Mutex)

	- pthread_mutex_t阻塞型互斥锁
// 加锁过程
pthread_mutex_lock(&mutex);  // 如果锁已被占用→线程休眠
// 临界区操作...
pthread_mutex_unlock(&mutex);

上下文切换开销：~5-20μs（两次切换）
内存开销：~64字节/锁
支持属性：PTHREAD_MUTEX_NORMAL/ERRORCHECK/RECURSIVE
通过属性配置可以支持递归

-  条件锁 (Condition Lock)

	- 条件变量+互斥锁

- 信号量 (Semaphore)

	- 信号量是一种同步工具，用于控制对有限数量资源的访问或序列化执行

	- 计数器+线程队列。比互斥锁快30%（Grand Central Dispatch优化）

- 读写锁 (Read-Write Lock)

	- 多读单写，
// 读锁
pthread_rwlock_rdlock(&lock); // 可多线程同时读
// 写锁
pthread_rwlock_wrlock(&lock); // 独占访问
读多写少场景比互斥锁快5-10倍

- 性能对比

###  

### 优先级反转

- 优先级反转是指高优先级任务被低优先级任务阻塞，因为低优先级任务持有了高优先级任务需要的资源（如锁），而低优先级任务又可能被中等优先级任务抢占，导致高优先级任务被延迟执行。

- 解决方案：
**优先级继承**的核心思想是：当低优先级任务持有高优先级任务需要的资源时，临时将低优先级任务的优先级提升到与高优先级任务相同，以防止它被中等优先级任务抢占，从而让高优先级任务尽快完成。

- 使用场景

### 计时器

- 常用计时器对比

### 多线程数据不安全体现在哪

- 执行结果依赖于线程调度的随机性（即每次运行结果可能不同）。

- 多个线程并发访问同一份数据时
至少有一个线程在写数据，其他线程在同时读或写这份数据，且没有适当的同步机制。数组可能越界。

## RunLoop

### 什么是Runloop

- 通过内部维护的事件循环来对事件/消息进行管理的一个对象
没有消息处理，休眠避免资源占用【用户态-》内核态】
有消息需要处理，立刻唤醒【内核态-》用户态】

- main函数保持原因，UIApplication会启动主线程的RunLoop

### 数据结构

- CFRunLoop

	- pthread

		- 一一对应（和线程的关系）

	- currentMode

		- CFRunLoopMode

			- name

				- NSDefaultRunLoopMode

			- sources0
CFRunLoopSource 需要手动唤醒线程
用户事件（手动唤醒），不能自动触发，需要通过其他方式主动唤醒 RunLoop

			- sources1
CFRunLoopSource 具备唤醒线程的能力
系统事件，如端口、Mach 消息、系统回调等，内核可以唤醒线程（通常与系统通信）

			- observers

			- timers

	- modes

		- NSMutableSet<CFRunLoopMode*>

	- commonModes

		- NSMutableSet<NSString*>存的名字

	- commonModeItems

		- 集合里包含observer、timer、source

- CFRunLoopMode

- Source/Timer/Observer

	- kCFRunLoopEntry

	- kCFRunLoopBeforeTimers

	- kCFRunLoopBeforeSources

	- kCFRunLoopBeforeWaiting

	- kCFRunLoopAfterWaiting

	- kCFRunLoopExit

- 数据结构1对多的关系

	- 当运行在mode1上时，只能处理mode1上的事件，其他mode事件有回调是不会被处理的。
假如需要将timer添加到多个mode怎么处理？

		- NSRunLoopCommonModes

### 事件循环机制

- 流程

### RunLoop与NSTimer

- 由于uitableview滑动时，RunLoop mode会进行切换，从defaultMode到UITrackingMode，所以需要添加到commonMode下

### RunLoop与多线程

- 线程和RunLoop是一一对应的
当前线程的RunLoop默认是关闭的

### 常驻线程

- 1、当前线程开启一个RunLoop
2、向RunLoop中添加一个Port/Source等维持RunLoop的事件循环
3、启动该RunLoop

	- while不会造成死循环，而是经过用户态到核心态的转换后，RunLoop就休眠了，不会死循环

### 题目

- 子线程数据包装提交到NSDefaultMode，不影响滑动

### RunLoop如何检测卡顿？

- 监听 RunLoop 状态
在 .beforeSources 和 .afterWaiting 之间设置一个 超时定时器
如果长时间没有进入 .beforeWaiting，就说明 RunLoop 卡住了
50~100ms 是经验值，太短容易误判，太长延迟发现
使用mach_task_basic_info获取内存

	- 可在卡顿时使用如下方法采集主线程堆栈：
Thread.callStackSymbols  // 或更底层的 mach/thread_get_state
用于排查阻塞代码或死循环。

	- 获取内存

	-  

	- 卡顿检测基本原理

## 网络

### 分层协议

### HTTP协议

- 1、请求/响应报文

	- 请求报文

	- 响应报文

	- 请求方式：
GET、POST、HEAD、PUT、DELETE、OPTIONS六种

		- get和post区别的初级回答

		- 标准回答，

			- 安全：
不应引起server端的任何状态变化
GET HEAD OPTIONS

			- 幂等性：
同一个请求方法执行多次和执行一次的效果完全相同
PUT DELETE

			- 可缓存性：
请求是否可以被缓存
GET HEAD

			- 数据大小不一样

			- 状态码：
1xx 信息性状态码（少用）
2xx 成功
3xx 重定向
4xx 客户端错误
5xx 服务器错误

- 2、连接建立流程

	- 三次握手、四次挥手

		- 三次握手建立链接
在此基础上开始正式请求
然后经过四次挥手断开

			- 为何是三次？
如果超时，客户端超时重传，会被服务端认为又一次建立链接

		- 为何进行两方面断开？（客户端和服务端）

			-  

- 3、http特点

	- 无连接
HTTP的持久连接补偿无连接

		- 持久连接提升了网络连接的效率

			- 原理图

			- 头部字段：
Connection:keep-alive 客户端期许采用持久连接
time:20 20s内请求可以复用已打开的链接，不会发生4次挥手。
max:10 该连接最多发生10个http响应。

			- 怎样判断一个请求是否结束？
从两个角度
1、响应报文头部字段：Content-length：1024
客户端根据接收数据字节数判断
2、chunked，最后会有一个空的chunked

	- 无状态
Cookie/Session来解决

- Charls抓包原理？

	- 中间人攻击，中间人可以篡改请求和响应数据

		- 常见实现方式

		- ARP 欺骗（局域网中）

			- ARP 协议不验证身份。
攻击者伪装成网关，让受害者将数据发给攻击者，再由攻击者转发。
场景：局域网 Wi-Fi 中的“蹭网者”可以伪装网关。

		- DNS 欺骗

			- 篡改 DNS 返回结果，把原本要去的服务器地址替换成攻击者的。
用户访问 example.com，被引导到攻击者控制的服务器。

				-  

		- HTTPS 中证书伪造

			- 攻击者伪造服务器的 SSL 证书，诱使客户端建立加密连接（但实际连接的是攻击者）。
需要客户端信任攻击者的伪造证书（例如安装了攻击者控制的根证书）。

		- Wi-Fi 热点劫持

			- 攻击者建立一个免费 Wi-Fi 热点（例如“Starbucks Free”），诱导用户连接。
所有流量都经过攻击者设备。

		- 通过设备越狱和root，编写 Frida 脚本，注入到目标 App 进程中

### HTTPS与网络安全

- https = http + ssl/tls

	-  

	- TLS 1.3 的 0-RTT

		- 安全性风险

- 连接建立流程 TLS1.2版本

	- 会话秘钥 =  random S + random C + 预主秘钥

		- 两个随机数的作用

	- 通过密钥交换算法（如RSA、DH、ECDH）生成预主密钥（Pre-Master Secret）。注意，在RSA密钥交换中，预主密钥由客户端生成并用服务器公钥加密后发送；在DH/ECDH中，双方通过交换参数协商出预主密钥。

		- TLS 1.3：仅支持 ECDHE（椭圆曲线 DH），密钥交换过程通过非对称加密保护。

		- 服务端生成一对 ECDHE 公钥/私钥对，发给客户端（ServerKeyExchange）

客户端生成自己的 ECDHE 公钥/私钥对，发给服务端（ClientKeyExchange）

双方用对方公钥 + 自己私钥计算出相同的 Pre-Master Secret

	-  

- TLS1.2和TLS1.3版本

	- 客户端发送 ClientHello，包含支持的协议版本、密码套件以及用于密钥协商的“密钥分享（Key Share）”数据（如椭圆曲线公钥）。

服务器接收到后，立即返回 ServerHello + 证书 + Finished。服务器也发送自己的密钥分享数据。

- 攻破TLS的情况

	-  

	-  

	-  

	-  

	-  

	- 还有就是基于权限的动态二进制注入和Hook攻击

- 都使用了哪些加密手段，为什么？

	- 连接建立过程使用非对称加密，非对称加密很耗时。
后续通讯过程使用对称加密

		- 非对称加密

		- 对称加密

### 传输层协议

- UDP：用户数据报协议

	- 特点

		- 1、无连接，不需要建立通道

		- 2、尽最大努力交付（非可靠传输）

		- 3、面向报文：既不合并也不拆分

	- 功能

		- 1、复用

		- 2、分用
根据接收到的数据，分发到目的端口

		- 3、差错检测，16位（两个字节）

			- 二进制反码计算

			- 接收方校验，如果不为1，则说明传输出错

- TCP：传输控制协议

	- 特点

		- 1、面向连接

			- 数据传输开始前，需要3次握手建立链接
数据传输结束后，需要4次挥手断开连接

		- 2、可靠传输（有序、重传）

			- 无差错

				- 通过停止等待协议实现

				- 无差错情况

				- 超时重传

				- 确认丢失

				- 确认迟到

			- 不丢失

			- 不重复

			- 按序到达

		- 3、面向字节流

		- 4、流量控制

			- 滑动窗口协议

				- 接收方可以动态调整发送窗口的大小，这两个是在TCP头部的报文中的字段

				-  

		- 5、拥塞控制

			- 慢开始、拥塞避免

			- 快恢复、快重传

### DNS解析

- 域名到IP地址的映射，DNS解析请求采用的UDP数据报，且明文。

- 查询方式

	- 递归查询

	- 迭代查询

- 存在哪些问题

	- DNS劫持和Http没有关系，解析发生在建立连接前，使用UDP数据报，端口号53

		- httpDNS：解决DNS劫持
使用HTTP协议向DNS服务器的80端口进行请求

		- 长链接：解决DNS劫持

	- DNS解析转发

### Session/Cookie

- 对HTTP协议无状态特点的补偿

- Cookie主要用来记录用户状态，区分用户；状态保存在客户端。在http请求报文的Cookie首部字段。服务器端设置http响应报文的Set-Cookie首部字段。

	-  

	-  

	- 保证Cookie安全

- Session主要用来记录用户状态，区分用户；状态保存在服务器端。

	- session是依赖Cookie的

### 网络请求流程

### 问题

### socket通讯

- 应用层与传输层之间的桥梁，一种“通信端点”的抽象，提供接口让开发者使用 TCP 或 UDP 进行网络通信。

- Stream Socket：TCP 浏览器访问网页、聊天

- Datagram Socket ：UDP 视频通话、直播等实时通信

- 如何设计一个 Socket 通信框架（IM）？
模块包括：

连接管理器：建立连接、断线重连

协议封装器：处理消息头、压缩、加密等

发送队列：支持可靠投递、重试机制

消息分发器：根据 msgType 派发给业务层

心跳机制：定时发送保活包

状态管理：监听前后台、网络切换事件


- 如何优化 Socket 性能？
消息合并与打包

异步 IO（GCD、NSStream）

保持 TCP keepalive 设置

减少无效心跳包（只在活动时间发送）

后台优化与保活（合规方式）

-  

- CocoaAsyncSocket

- Starscream

-  

### 进程间的通信，CFNotificationCenter也可以。同时可以携带参数

- 线程间的通信

## 设计模式

### 六大设计原则

### 责任链

### 桥接

### 适配器

### 单例

### 命令

### Protocol-Oriented Programming（协议导向编程）组件化

## 架构/框架

### 图片缓存框架

- 模块

- 图片用什么方式读写？
以图片的URL的单向Hash值作为key

- 内存的设计上需要考虑哪些问题？

	- 存储的size

	- 淘汰策略：

		- 队列先进先出方式

		- LRU算法策略（30分钟内是否使用过）定时检查比较耗性能

- 磁盘设计需要考虑哪些问题？

	- 存储方式

	- 大小限制

	- 淘汰策略（如某一图片存储距今超过7天）

- 网络部分的设计需要考虑哪些问题？

	- 图片请求的最大并发量

	- 请求超时策略

	- 请求优先级

- 图片解码，不同格式的图怎么做？

	- 应用策略模式对不同图片格式进行解码

	- 在哪个阶段做图片解码？
在磁盘读取后，或者网络请求返回后，在加载内存前

- 线程处理

	-  

	-  内存缓存（Memory Cache） - 通常主线程或串行队列

		- 通常是一个线程安全的 NSCache 或自定义 LRU 容器（加锁或使用并发队列）

访问非常快，可直接在主线程操作

也可以用 GCD 的串行队列隔离，避免锁竞争

	- 磁盘缓存（Disk Cache） - 异步串行或并发 IO 队列

		- 涉及文件系统读写，绝不能在主线程处理

	- 图片解码（Image Decoding） - 异步解码线程

		- 解码通常耗时（如 JPEG → bitmap），必须放在后台线程处理
部分框架会使用独立的解码队列或 OperationQueue
有时会提前解码（prepareForDisplay）优化滑动性能

	- 图片下载（Network Fetch） - URLSession 默认后台线程

	-  回调主线程更新 UI

### 时长统计框架

- 不同类型的记录器：
基于不同的分类场景提供的关于记录的封装、适配

- 记录的数据会由于某种原因丢失？如何处理？降低丢失率

	- 定时写磁盘（每隔15min）

	- 限定内存缓存条数，超过即写磁盘

- 关于延时上传的具体场景有哪些

	- 前后台切换

	- 从无网到有网的变化

	- 通用轻量接口捎带

- 上传时机

	- 立刻上传

	- 延时上传

	- 定时上传

### 复杂页面架构

- MVVM

- RN数据流思想，子节点没有自我更新的权利，根节点自上向下更新

### 客户端整体架构

- 业务之间的解耦通信方式

	- OpeURL

	- 依赖注入：通过依赖注入，一个类所依赖的对象（即依赖）由外部传递给它，而不是在类内部自己创建。这样可以降低类之间的耦合度，提高代码的可维护性和可测试性。
有三种方式：构造函数注入、属性注入和方法注入

## 算法

### 字符串反转

- 当begin>= end时结束

	- c语言，strlen(cha) 是字符串长度，不包含终止符 '\0'。

	- Swift

### 链表反转

- 头插法原理

	- 声明

	- 翻转算法

		- 打印

		- 创建链表

			-  

### 有序数组合并

- 原理

	- 具体算法

		-  

		-  

		-  

		- 演示

### Hash算法

- 思路

-  

	- C语言

	- Swift利用dic的hash算法

### 查找两个子视图的共同父视图

- 思路

	- 要点：
找到view1和view2的所有父视图数组。
倒序遍历，条件为遍历完其中小的数组。

### 求无序数组当中的中位数

- 基础排序算法

	- func findMedian(_ nums: [Int]) -> Double {
    let sorted = nums.sorted()
    let n = sorted.count
    if n % 2 == 1 {
        return Double(sorted[n / 2])
    } else {
        return Double(sorted[n / 2 - 1] + sorted[n / 2]) / 2.0
    }
}


- 快排
任意挑选一个元素，以该元素为支点，划分集合为两部分。
如果左侧集合长度（即任意挑的元素的下标）恰为count/ 2,那么支点恰为中位数。
如果下标< count/2,那么中位点在右侧，反之，中文数在左侧。
进入相应的一侧继续寻找中位点。

	- 核心

	- 粗略排序，找到索引值为k的数

	- 如果数组是奇数，找到索引值为n/2的元素即可，否则就找到再前一个n / 2 - 1元素，取平均。

### 给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。 nums = [100, 4, 200, 1, 3, 2]，最长连续序列为 [1, 2, 3, 4]，返回长度 4

- 方法1

- 方法2

### 大数运算

## 第三方库

### AFNetWorking

- 框架基于 Apple 的 NSURLSession 和 NSOperation 封装的高层网络通信库。

	- 主要类的关系图

		-  

	- 核心类

### SDWebImageView

- 框架

	- 流程

### Reactive Cocoa

- 函数响应式编程框架

	- 信号：RACSignal
代表一连串的状态，状态改变时，对应的订阅者会收到通知执行相应的指令

		-  

	- 订阅：RACSubscriber

### ASyncDisplayKit

- 提升iOS界面渲染性能的框架
通过减轻主线程压力，把以上三个方面的事务放到子线程处理。

	- 基本原理

	-  

### APPFlyers

### Firebase

### MJExtension

- 轻量级的模型转换工具，可将 JSON 转换为 Model，也可以将 Model 转为 JSON

- 核心原理

### FMDB（SQLite 封装库）

- FMDB 是对 Apple 原生 SQLite3 C API 的封装，提供更易用的 Objective-C 操作方式

- 核心原理

### SVProgressHUD

- 是一个轻量的 HUD 提示框库，用于显示加载、成功、错误等状态。

- 核心原理

## Swift语言

### SwiftUI

### SwiftConcurrency

- 基础概念

	- await 不会阻塞线程，它会挂起函数，并让出线程资源。
Swift 编译器自动把 async 函数变成状态机。

	-  actor 是 Swift 提供的语言级线程安全机制，能自动序列化对内部状态的访问，避免手动加锁带来的复杂性和错误。

		- actor 能跨线程访问吗？
能，但会自动“排队执行”，即使在不同线程访问，actor 也只会串行执行内部逻辑，确保线程安全。
actor 是否是串行的？
是的。actor 的本质就是串行化对其内部状态的访问，防止并发冲突。

	- Swift 为了保证类型在并发环境中传递是安全的，引入了 Sendable 协议。

	-  

		-  

			- 实例

		- addTask {} 中的代码是并发执行的
for await result in group 会按完成顺序遍历（不是提交顺序）
抛错会中止整个 group（withThrowingTaskGroup）

还有 withTaskGroup（非 throwing 版本）
await withTaskGroup(of: Int.self) { group in
    ...
}

- 常见问题

### [Combine](https://juejin.cn/post/7218550671833940005)

- Combine 是苹果推出的响应式编程框架，主要用于处理异步事件流，比如网络请求、UI 事件、定时器等等。它的核心思想是：

数据是流动的（Stream），你订阅（Subscribe）它，处理（Transform）它，最终拿到结果（Sink）。

	- Publisher	负责发布事件或数据（数据源）
Subscriber	负责接收事件或数据（监听者）
Operator	在中间转换/过滤/组合数据流

	-  Just 是最简单的 Publisher，只发送一次值。

✅ sink 是最常用的 Subscriber，直接接收值。

-  

-  

-  

### 泛型

- Swift 的泛型（Generics）是语言的核心特性之一，允许你编写 复用性强、类型安全、性能优秀 的代码。

- 泛型协议

- 泛型约束（where / :）

	-  限制泛型必须遵守某个协议

	- 使用 where 限定多个条件

	- 泛型扩展使用 where

- 系统应用

-  

### [Mirror：提供一种安全、有限的方式来探索对象结构，便于调试、序列化等任务。](https://mp.weixin.qq.com/s/xPeBOU51NvPQKqYvgGdi5g)

## flutter

### 不同类型的flutter工程的主要区别

- 无状态组件【StatelessWidget】

	- 用于 UI 内容固定、不依赖用户交互或状态变化的组件。
特点：
只在构建时渲染一次
状态不发生变化（不可变）
一旦需要变化，必须重新构建整个 widget

- 有状态组件【StatefulWidget】

	- 用于需要响应用户交互或状态变化的场景。
特点：
包含两个类：StatefulWidget 和 State
状态保存在 State 对象中
调用 setState() 可触发 build() 重建

### [学习flutter官网](https://docs.flutterchina.club/tutorials/)

## 静/动态库封装

###  静态库的特点
**静态库（.a 文件）**在编译阶段已经被“打包进你的可执行文件”。
编译器将静态库的目标代码链接进最终的可执行文件（Mach-O 文件）。
所以在 App 启动时，dyld 无需再处理这些静态库：
➤ 不需要加载
➤ 不需要重定位
➤ 不需要符号绑定

### 动态库的加载流程

- 1.解析依赖：
dyld 读取 Mach-O 文件的 LC_LOAD_DYLIB 命令。递归加载所有依赖的动态库（UIKit → Foundation → libSystem 等）

- 2.Rebase 修正：
// 由于 ASLR，所有指针要加上偏移量
slide = actual_address - preferred_address
遍历 __DATA 段修正内部指针

- 3.符号绑定：
Lazy Binding：首次调用时绑定（如函数调用）
Non-Lazy Binding：立即绑定（如全局变量）

- 4.运行初始化：
按依赖顺序执行：
所有 __attribute__((constructor)) C 函数
C++ 全局对象构造函数
Objective-C 的 +load 方法（按父类→子类→分类顺序）

- 5.进入 main()：
完成所有初始化后跳转到程序入口

### iOS14 对象内存优化

### 如何hook所有类的+load方法

- 1、执行时机：
使用 __attribute__((constructor)) 在 main() 前执行
需在 +load 触发前完成 hook

- 2、特殊类处理：
// 跳过系统私有类
if ([NSStringFromClass(cls) hasPrefix:@"_"]) continue;
// 跳过元类
if (class_isMetaClass(cls)) continue;

- 3、多次 Hook 防护：
if (objc_getAssociatedObject(cls, "hook_flag")) return;
objc_setAssociatedObject(cls, "hook_flag", @YES, OBJC_ASSOCIATION_RETAIN);

### Swift创建的Freamework静态库与OC混编

- 框架目标不支持创建桥接文件（Xcode 会忽略框架项目中的桥接文件设置）Xcode 会忽略该设置，即使路径正确也无效⚠️

- 建立一个module.modulemap文件，在里面添加需要混编的OC头文件支持。并且头文件要和该module文件同级
前往Build Settings下的Swift Compiler - Search paths，添加文件夹路径。

## CI/CD

## 蓝牙

### 蓝牙有哪些工作模式？BLE 和传统蓝牙有何区别？

- BLE：低功耗蓝牙，主要用于短距离、小数据量通信。
传统蓝牙：数据传输速率高，但功耗大。
BLE 使用 GATT（通用属性配置文件）进行通信。

### iOS 的蓝牙开发框架是什么？说说其核心类？

- 框架：CoreBluetooth
关键类：
CBCentralManager：中心设备管理器（主设备）
CBPeripheral：外设对象
CBPeripheralManager：外设管理器
CBService / CBCharacteristic：服务与特征值

### 蓝牙中 GATT、Characteristic、Service 是什么？

- GATT：Generic Attribute Profile，定义了设备之间如何通信。
Service：一组相关的 Characteristic。
Characteristic：数据的基本单元，包含值和权限。

### iOS 后台能否进行蓝牙通信？

- 可以，需在 Info.plist 中声明 bluetooth-central / bluetooth-peripheral，但能力受限。
需要设置后台模式，保持连接或接收通知。

### 蓝牙设备断开连接了怎么处理？如何重连？

- 监听 didDisconnectPeripheral
使用 connect(_:options:) 重连
可以保存 UUID 并使用 retrievePeripherals 或 retrieveConnectedPeripherals 重连

### CoreBluetooth 有哪些常见坑？如何排查？

- 授权未开启：未提示权限
peripheral.discoverServices 返回 nil
多线程回调时状态错乱（尽量在主线程处理）
notify 特征未设置好就监听导致失败

### 如何设计一个 iOS 蓝牙数据交互系统？

- 分层架构：扫描连接管理层、服务特征层、数据处理层、UI控制层
支持断线重连、消息缓存、CRC校验、加密传输等

### 如何处理 BLE 传输数据过长？

- 分包发送，通常 BLE 一次最多只能发 20 字节
使用帧协议，定义帧头/帧尾/校验位，接收端做拼包

## 局域网图传

## 录制与直播

### 直播推流卡顿如何优化

- 视频采集端优化

- 视频编码优化

- 网络推流优化

- 渲染线程/帧同步优化

- 动态性能监控与自适应调整

- 调试方法建议

### 视频流处理

- [ 采集 ] → [ 预处理/滤镜 ] → [ 编码 ] → [ 推流/存储 ]
                             ↓
                        [ 解码 ] ← [ 拉流 ]
                             ↓
                         [ 渲染 ]


	-  

	-  

	-  

	-  

	-  

	-  

- 常见问题

	- 工具

## 性能优化

### 高分辨率下功耗、发热、内存

- 过度使用优先级继承可能导致：

高优先级任务过多，削弱系统调度能力

电池消耗增加

热管理问题（设备过热降频）

	- 耗电优化
程序的耗电主要在以下四个方面：CPU 处理、定位、网络、图像。

		- 尽可能降低 CPU、GPU 的功耗；
尽量少用定时器；
优化 I/O 操作：
不要频繁写入小数据，而是积攒到一定数量再写入；
读写大量的数据可以使用 Dispatch_io，GCD 内部已经做了优化；
数据量比较大时，建议使用数据库；
网络方面的优化：
减少压缩网络数据（XML -> JSON -> ProtoBuf），如果可能建议使用 ProtoBuf；
如果请求的返回数据相同，可以使用 NSCache 进行缓存；
使用断点续传，避免因网络失败后要重新下载；
网络不可用的时候，不尝试进行网络请求；
长时间的网络请求，要提供可以取消的操作；
采取批量传输。下载视频流的时候，尽量一大块一大块的进行下载，广告可以一次下载多个；
定位层面的优化：
如果只是需要快速确定用户位置，最好用 CLLocationManager 的 requestLocation 方法。定位完成后，会自动让定位硬件断电；
如果不是导航应用，尽量不要实时更新位置，定位完毕就关掉定位服务；
尽量降低定位精度，比如尽量不要使用精度最高的 kCLLocationAccuracyBest；
需要后台定位时，尽量设置 pausesLocationUpdatesAutomatically 为 YES，如果用户不太可能移动的时候系统会自动暂停位置更新；
尽量不要使用 startMonitoringSignificantLocationChanges，优先考虑 startMonitoringForRegion:

- 功耗与发热优化

	- 根据当前负载动态调整分辨率。

	- 硬件加速优先（Metal / VideoToolbox）

		- 使用 Metal 替代 CoreGraphics/UIImage。

		- 使用 VideoToolbox 编码视频而非软件编码。

	- 后台任务及时中断

		- 录制/渲染结束后要立即释放资源（如停止会话、释放缓冲区、销毁上下文）。

		- 延迟释放是功耗与内存飙升的常见原因。

- 内存优化策略

	- 避免图像频繁解码

		- 不要频繁用 UIImage(contentsOfFile:) 加载大图，推荐：
使用 CGImageSourceThumbnail 生成缩略图；
缓存解码后的数据。

	- 分片处理大图或视频帧

		- 比如将 4K 图像分成小块进行处理，避免内存一次性爆炸

	- 使用 Metal Texture 替代 UIImage/CGImage

		- UIImage 占用内存较大，频繁转码效率低；

MTLTexture 可直接在 GPU 上操作，且可复用。

	- 避免多余图层合成（CALayer/UIView）

		- 控制层级和动画数量，特别是在 scrollView、tableView 中不要使用超量的复杂视图。

	- 内存检测工具

		- instrument 如何使用，如何定位问题函数？

		- RunLoop检测卡顿如何实现？

		- 第三方检测工具

- 硬解码VS软解码

### 包体积优化

### app启动流程

- 1、系统加载阶段（系统层）

	-  

- 2、应用初始化阶段（运行时和系统库）

	-  

- 3、业务初始化阶段（开发者可控）

	-  

- 优化方向

### 优化启动时间

- 一、启动时间分析工具

	- Xcode 内置工具

		- 其他

- Pre-Main 阶段优化

	- 1. 减少动态库加载

		- 2、优化 rebase/binding

			- 3. 优化 +load 方法

				- 4. 减少 C++ 静态初始化

				- initialized和load的区别

					- 执行时机

						- +load 是在程序启动过程中，dyld 加载可执行文件和动态库后立即执行。

+initialize 是在类或其子类 第一次被使用（接收消息）时 才执行。

					-  调用频率

						- +load	每个类/分类 只调用一次，且不受子类影响。
+initialize	每个类 也只调用一次，但子类在使用前，如果没实现，会调用父类的。

					- 用途 & 场景

						- +load	初始化运行时环境、方法交换（Swizzling）等早期操作。
+initialize	延迟初始化一些类级别的资源或变量（线程安全）。

	- 模块组件化，打包成静态库，加速编译
未被使用的静态库符号不会参与编译结果，减小体积、加快注册。静态库中未引用的类不会注册到 runtime，可减轻启动负担

		- 即使打包成静态库，如果你仍然在 AppDelegate 或 +load 中初始化它们，启动速度不会有本质提升。

		- 但是在工程构建（编译 + 出包）的效率上，将模块打成 静态库（静态 Framework 或 .a） 会显著加快主工程的编译速度，尤其是在 大型项目、多模块、多团队协作场景下，静态库的优势非常明显。

- Main() 之后阶段优化

	- 使用 UIStoryboard 替代代码创建视图（系统自动优化）

分步渲染：先显示静态内容，再加载动态数据

使用 LazyVStack/LazyHStack（SwiftUI）或 ASDK（UIKit）

		- 编译时优化：Storyboard 在构建时被编译为高效的二进制格式（nib 文件）

运行时优势：系统可以直接加载预编译的视图结构，无需在运行时解析 XML

对比代码创建：纯代码需要执行大量 alloc/init 和 addSubview: 调用

			- 系统级优化
预取技术：iOS 会提前解析 Storyboard 结构

内存映射：二进制 nib 文件通过内存映射加载，减少内存拷贝

布局预计算：Auto Layout 约束在编译时部分优化

		- Storyboard什么时候加载？
时间点：main() 函数执行后，application(_:didFinishLaunchingWithOptions:) 调用前
触发条件：// Info.plist 配置
<key>UIMainStoryboardFile</key>
<string>Main</string>

		- 微信方案

- 高级优化技术

	- 二进制重排 (Order Files)
让启动过程中最先使用的函数、类、方法等，紧密排列在可执行文件的前部，减少内存页跳转，提高加载命中率和缓存效率。

		- 通过分析应用的启动路径，调整目标二进制文件中函数、符号、类等的布局顺序，从而提高 CPU 取指效率、减少页缺失、加快冷启动速度。
通过重新排列代码在可执行文件中的物理位置来优化应用启动时间的核心技术。它通过减少 Page Fault（缺页中断） 次数来显著提升启动性能。

			- 启动相关代码分散在不同内存页
启动时需要加载大量不连续的页
频繁的 Page Fault（约 0.5-5ms/次）

			- 将启动相关代码集中在连续内存页
减少 Page Fault 次数
降低 30%-50% 的启动时间

		- 实施流程

			- 步骤1：收集函数调用顺序

				- 1.1 启用链接映射文件
Build Settings > Write Link Map File = YES

				- 1.2 添加插桩代码
在工程的 Prefix Header 或 AppDelegate 中添加：

				- 1.3 生成调用顺序文件
在首屏渲染完成后收集数据

			- 步骤2：创建 Order 文件

				- 2.1 获取函数调用轨迹
在模拟器或真机上启动应用

完成启动流程（到首屏可交互状态）

调用 generateOrderFile() 生成 .order 文件

				- 2.2 优化 Order 文件内容

					- 优化后

			- 步骤3：配置 Xcode 项目

				- 3.1 添加 Order 文件
将生成的 app.order 文件拖入项目

确保在 Build Phases > Copy Bundle Resources 中

				- 3.2 配置构建设置
Build Settings > Order File = $(PROJECT_DIR)/app.order

				- 3.3 验证配置
# 检查链接器参数
xcrun clang -### -o output input.m 2>&1 | grep order

			- 步骤4：验证优化效果

				-  

			- 高级优化技巧

				- 1. 多场景采样

					- 合并脚本

		- 二进制重排中动态符号与 dyld 依赖问题的深度解析

			-  

				- 2. 解决方案
方案 1：将动态修改的符号排除在重排之外
在 Order File 中不包含被 swizzling 的符号，避免重排影响其地址：

				-  

				-  

			-  

				-  

				-  

### 弱网优化方案

- NSURLSessionTaskMetrics
提供了丰富的计时信息，包括DNS查询、TCP连接、TLS握手等各个阶段的耗时。

	- 时间计算
TCP连接耗时：如果使用了TLS，则还包括TLS握手时间

- DNS 优化

	- 使用 IP 直连 或 DNS 预解析
本地缓存 DNS，例如通过配置 NSURLSessionConfiguration.connectionProxyDictionary 或在请求中预设 Host-IP 映射

- 连接优化

	- 启用 keep-alive，避免频繁创建连接

支持 HTTP/2、QUIC（降低握手时间）

- 请求压缩

	- 启用 GZIP/Deflate (Accept-Encoding) 减少响应体大小

对 JSON 请求体启用压缩，尤其在移动网络下非常有效

- 上传优化

	- 断点续传、批量上传、合并小请求、延迟提交（如打点埋点缓存在内存中）

- 缓存策略

	- 正确设置 URLCache，或使用 ETag/Last-Modified 减少重复数据请求

	- 避免弱网下重复加载资源

- 弱网检测

	- Ping 延迟测试（RTT）
测量访问目标服务器或 DNS 的延迟时间（Round Trip Time）

	- 下载/上传速度测试
下载或上传一个小文件或打点请求，计算带宽。

	- TCP 连接时间
测量连接目标服务器（如 API 网关）的耗时

	- 视频首帧/缓冲时间
对于视频/直播 App，首帧耗时 & 缓冲频率能直接体现网络质量。
关键指标：
首帧时间 > 5s：弱网；缓冲次数 > 3 次/分钟：弱网

	- 丢包率（Packet Loss）

### 多线程线程池

- 超过 (CPU核心数 × 4) 线程时调度效率急剧下降

-  

### 常见crash

- EXC_BAD_ACCESS (SIGSEGV/SIGBUS):
访问已释放对象（野指针）
内存越界访问
多线程竞争访问

- Exception Type: EXC_BAD_INSTRUCTION (SIGILL):Swift 强制解包 nil (!)失败

- Exception Type: EXC_CRASH (SIGABRT)
Application Specific Information:
*** Terminating app due to uncaught exception 'NSRangeException', 
reason: '*** -[__NSArray0 objectAtIndex:]: index 5 beyond bounds for empty array'
数组越界
字典 key 为 nil
未实现协议方法

- Exception Type: EXC_RESOURCE
Exception Subtype: CPU
CPU 占用超过 80% 持续 180 秒
内存使用超过系统阈值

- Termination Reason: Namespace SPRINGBOARD, Code 0x8badf00d
主线程阻塞超过 20 秒
启动超时（iOS 15+ 要求启动 ≤ 1.5 秒）

- Termination Reason: Namespace JETSAM, Code 0x11
系统内存不足终止应用

- Exception Type: EXC_BAD_ACCESS (SIGSEGV)
Exception Codes: KERN_INVALID_ADDRESS at 0x7ffe00000000
特征：线程堆栈地址接近边界
主线程栈：512KB（iOS 15 前）/ 1MB（iOS 15+）
子线程栈：默认 512KB
典型案例：递归无终止条件

- Termination Reason: Namespace THERMAL, Code 0xc0000086
原因：设备过热保护
优化方向：
降低 CPU/GPU 使用率
减少频繁网络请求
优化动画帧率

### llvm

- 用于构建编译器和相关工具链的框架
LLVM 是一个模块化、可复用的编译器基础设施项目，支持将高级语言转换为中间表示（IR），进行优化并生成目标机器码。
源码 → [clang/swiftc] → LLVM IR → 优化 → 汇编 → 链接 → 可执行文件

- LLVM 的核心组件有哪些？
Clang: C/C++/Objective-C 前端

LLVM IR: 中间表示

opt: 优化器

llc: 后端汇编生成器

lld: 链接器

llvm-as, llvm-dis: IR 编码/解码工具

llvm-pass: 插件系统，支持自定义优化

### 卡顿问题

- 卡顿场景分析

### 如何检测延迟，xcode中有哪些工具可以分析性能瓶颈

-  

## 版本更迭

###  

### 数据库选择

- 高数据量查询10w数据在20-100ms内，内存50m以内

	- 简单查询：直接使用数据库索引 + fetchLimit=1000
中等复杂度：预计算字段 + 索引查询
高复杂度：批量分块处理 + 提前终止
实时更新需求：Realm 结果监听 + 自动更新

- 业务场景

- 决策树

- 总结

### 语言对比

### 在线更新

- [一切更新需要遵循苹果审核指南](https://developer.apple.com/app-store/review/guidelines/#introduction)

- [通过Uniapp的UniSDK更新iOS工程内的小程序](https://cloud.tencent.com.cn/developer/news/894081)

- 通过Lua脚本对代码做动态调整

## 其他技术栈

### Python

### kotlin

### [Ai编码应用](https://github.com/intitni/CopilotForXcode)

- [免费](https://cloud.tencent.com/developer/article/2466661)

	- 安装后，在xcode设置快捷键

- [付费](https://juejin.cn/post/7320431099607285786)

	- 安装后，在xcode设置快捷键

## 技能要求

### 初级工程师

- 精通OC基础

- 精通UIKit等Cocoa Freamework

- 熟悉网络通讯机制以及常用数据传输协议

- 具备主流开源框架的使用经验

### 中级工程师

- 扎实的编程、数据结构、算法基础

- 深入理解语言机制、内存管理、网络、多线程、GUI

- 精通常用设计模式、框架、架构

- 良好的分析、解决问题的能力

### 高级工程师

- 解决研发过程中的关键问题和技术难题

- 调优设备流量、性能、电量

- 较强的软件设计能力

- 对iOS内部原理有深刻理解

### 资深工程师

- 精通高性能编程以及性能调优

- 灵活运用数据结构、算法解决复杂程序设计问题

- 提供性能优化、日志搜集、统计分析等方案

- 架构、模块设计

## question：历史项目的难点和亮点

### 集团数字化转型项目（朗致集团）

- 难点：跨部门协调：统筹5+战略项目，需协调6个业务部门和3个技术团队
硬件-软件融合：主导"小盒子"微型服务器项目（涉及电路/架构/外观设计）
AI垂直领域落地：基于LLM训练医药行业专属客服模型
传统行业转型阻力：推动40+医药生产环节数字化改造

- 亮点 & 解决方案：效率提升40%：通过分布式服务器架构优化区域数据处理
智能客服机器人：设计无人值守群管理工具（结合BoardMix工作流）
行业白皮书输出：主导编写《医药电商中台优化白皮书》获集团推广
动销模型优化：重构直销数据分析逻辑，指导采购生产决策

### 蓝港平台BI App & SDK（蓝港互动）

- 难点
高并发稳定性：支撑千万级用户游戏SDK（登录/支付掉单率8%）
跨平台兼容：Unity/自研引擎与iOS交互层开发（覆盖20+游戏项目）
Web3资产整合：多链钱包地址+协议分类+公司主体数据融合
全球化SDK适配：Facebook/Google/Adjust等50+第三方SDK兼容

- 亮点 & 解决方案
掉单率降至3%：重构OC-Swift混编静态库，引入事务补偿机制
资管系统商业化：开发即时通讯模块，支撑Element/NAGA平台生态闭环
跨平台中间件：设计通用交互协议，减少各游戏接入成本60%
实时决策看板：构建CEO级Web3资产多维度报表系统

### 麦思加数学（蓝港旗下）

- 难点
性能瓶颈：游戏课件加载卡顿导致日活流失
架构缺陷：《麦思乐园》ScrollView+ImageView背景图联动
跨端协作：需同步iOS/安卓/Web/小程序多端功能
教育合规：完成等保测评与教育类备案

- 亮点 & 解决方案
日活提升150%：WKWebView请求拦截+本地缓存策略
内存优化70%：分段背景图（大图拆成 tile）+ 跟随偏移加载（进阶）
MVVM架构落地：YTKNetwork+RAC实现网络层统一管理
Crash监控体系：本地化邮件报错机制提升Debug效率40%

### 爬梯朗读（神州佳教）

- 难点
实时音频处理：在线PK需毫秒级语音评分
技术债务重构：遗留代码需支持班级/打赏/内购等新功能
体验优化：头像框等UI元素动态加载性能差

- 亮点 & 解决方案
零延迟PK系统：CocoaAsyncSocket长连接+FreeStreamer音频处理
动态注入技术：Runtime Hook SDWebImage实现头像框无侵入加载
社交裂变增长：UMeng分享体系带来30%用户自然增长

## iOS 架构师成长

### 成为一名合格的 iOS 架构师，不仅仅是会写代码，更关键的是能够从整体上规划项目架构、把握技术选型、提升团队效率、保障代码质量与系统稳定性。

### 职责

- 架构场景

	- VIPER简述

	- 大型项目/多人协作

### 核心能力矩阵

- 项目模块化
使用 Swift Package、CocoaPods、XCFramework 拆分项目
支持动态下发（热修、动态模块加载）
接口隔离：protocol + extension + DI 解耦模块

- 网络架构
基于 URLSession、Alamofire、Moya 等封装请求层
支持多环境切换、接口 Mock、缓存策略、断点续传等

- 音视频/图像处理
AVFoundation、VideoToolbox、Metal 渲染优化
视频缓存、硬解码优先、分辨率动态调节

- 性能优化
卡顿检测（RunLoop + 信号量）
内存泄漏检测（Instrument / MLeaksFinder）
FPS / 内存 / CPU / 网络实时监控

	- 卡顿检测

- 崩溃分析
自定义 Crash Handler（如 PLCrashReporter）
dSYM 符号化、崩溃上报系统搭建（腾讯Bugly、Sentry）

### 项目工程能力

- 多环境管理（Debug/Release/Staging）

- 自动打包上传（Fastlane + GitLab CI/CD）

- 接入三方 SDK 的统一封装与监控

- 热更新策略（JSBridge、模块热插拔）

### 团队协作与制度

- 制定代码规范（SwiftLint、代码格式化）

- 建立模块文档、组件说明、技术选型记录

- 组织架构评审会、CodeReview、知识分享

## iOS架构师面试技巧

### 问题类型

-  

	- 1. 你如何设计一个大型 IM / 直播 / 商城 App 的架构？

回答思路：以模块化、解耦、高可扩展为导向，展示系统拆分、技术选型和核心问题处理。

示例：

对于大型 IM App，我采用模块化架构，将项目划分为：登录模块、好友模块、消息模块、会话模块、音视频模块、设置模块等。主框架使用 MVVM + Coordinator（或 VIPER）模式，确保每个模块解耦可测试。网络层使用 Moya 封装，数据持久层用 Realm/SQLite，IM SDK 封装成统一协议适配腾讯云或环信。为应对消息推送、离线消息处理、音视频编解码等问题，我引入 WebSocket 长连接、消息收发中间件、本地缓存与未读计数系统，支持多端登录、消息漫游等。

2. VIPER 架构你如何落地？遇到的最大问题是什么？

回答思路：讲清楚模块间分工、装配过程、怎么解决代码分散、文件繁多问题。

示例：

VIPER 结构清晰，适合多人协作和大型模块。每个页面我按 View-Interactor-Presenter-Entity-Router 分层，使用 Router.assembleModule 构建依赖，Interactor 专注业务逻辑，Presenter 处理展示逻辑，View 只负责 UI。最大挑战是文件数过多、新人难以上手。为此我建立了 VIPER 模板脚本（基于 Plist+脚本自动生成五个文件），并用 SwiftLint 做了分层规范检查，确保团队统一风格。

3. 如果你来主导，我们应该如何设计模块化？

回答思路：分层 + 分模块 + 可插拔，谈谈 CocoaPods / Swift Package / 动态库拆分经验。

示例：

我会以业务维度进行模块划分，如：LoginKit、UserKit、MessageKit、UIModule 等，配合 CoreKit 层存放基础能力（网络、缓存、日志）。每个模块独立维护 podspec，支持独立编译和测试。公共模块使用 Swift Package 管理，主 App 用 CocoaPods 汇总。在构建 CI/CD 时，通过 GitLab Pipeline 设定变更检测与按需打包机制，提升工程编译效率和可维护性。

4. Swift 泛型和协议的本质区别？

回答思路：从编译期/运行期、性能、用途上对比。

示例：

Swift 泛型在编译期确定类型，具备零开销抽象（zero-cost abstraction），性能优异；协议采用类型擦除，编译期不固定类型，灵活性强但有运行时开销。泛型适合算法、数据结构通用化，协议更适合解耦接口。例如数组是 Array，可精确知道元素类型，而协议如 Collection 运行期处理，适配更广但需注意性能与方法调度限制。

5. 如何用 RunLoop 检测卡顿？结合内存快照怎么做？

回答思路：RunLoop 阶段监听 + 卡顿打点 + 汇报。

示例：

我通过监听主线程 RunLoop 的 beforeWaiting 与 afterWaiting 两个阶段时间差，判断主线程是否卡顿（如超过 100ms）。使用一个 background thread 注册 CFRunLoopObserver，周期性记录 tick。如果发现连续多帧卡顿（如 5 次以上），则立即记录卡顿堆栈（通过 backtrace + mach thread API），并配合 Instruments 设置 Memory Snapshot 定时生成报告，供后续分析。

6. 你在 XX 项目中遇到的最大技术挑战是什么？如何解决的？

回答思路：用 STAR 法则（场景、任务、行动、结果）表达。

示例：

在某电商直播 App 中，我们遇到严重的内存泄漏和闪退。通过 Crashlytics 定位是播放器模块问题。我用 Instruments 内存分析工具找到了 VideoToolbox 未释放的 decode buffer，以及 AVPlayerItem 的循环引用问题。我重构了播放器生命周期管理，使用弱引用 delegate，并在退出播放页时手动释放资源，Crash 次数下降了 97%，用户反馈明显改善。

7. 有没有推动过基础组件沉淀或核心库重构？

示例：

我主导封装了我们团队内部的 UI 组件库，包括统一按钮、空状态视图、加载框、toast、弹窗等。组件支持暗黑模式、国际化、无侵入接入。同时我推动将网络层从 URLSession 重构为基于 Moya 的协议式请求，便于测试与 mock，并减少了 60% 重复代码。

8. 你怎么与产品沟通技术限制？有没有强硬或妥协的时候？

示例：

我坚持用数据和场景做决策。例如直播间要求同时渲染 6 路视频流，我说明了硬件限制和掉帧风险，并提供了两套方案：限制显示数量+切换 OR 降分辨率+裁剪。我们最终采用了自动降级策略，既保证体验也平衡资源。产品信任度提高，我也学会了用业务语言讲技术。

9. 和后端接口出问题时怎么协商？

示例：

我倾向于先内部定位问题本质。如果是接口文档与实际不一致，我会先本地打印请求与响应，并联系后端给出调用日志。通过整理复现步骤、明确期望返回结构或状态码，确保对方能快速排查问题。若是接口设计不合理，我会提出优化建议或约定新的字段结构，并主动协助联调，推动接口文档同步更新。

10.和设计对接动画时，怎么让他们妥协？

示例：

我会先明确动效目标，是美观还是功能引导。然后我用 Lottie、CoreAnimation 或 UIViewPropertyAnimator 实现初版。如果动画成本过高、设备卡顿、适配复杂，我会演示实际效果，让设计看到成本与体验的取舍点。多数设计看到真实效果后会愿意调整帧数、简化路径。也有一次我建议改为帧动画+渐变遮罩替代 3D 曲线，设计很认可。

11. 有没有带新人？带人方式是什么？

示例：

我曾带过实习生和转岗的初级工程师。我会为他们制定入职一周/一个月目标，例如熟悉模块、参与一个小需求、看懂一份架构图。代码上我坚持 pair programming、code review 和每周一次技术小分享，帮助他们从工具掌握、编码习惯到架构理解逐步进阶。我也关注心理支持，鼓励他们大胆提问和 demo 自己成果。

12. 你有使用 Fastlane 吗？如何在项目中落地自动化流程？

示例：

我在多个项目中引入 Fastlane 来实现自动打包上传、TestFlight 分发、截图生成、版本号管理等功能。使用 match 管理证书共享，gym 执行构建，pilot 上传到 TestFlight，sigh 下载 profile，结合 .env 文件做环境变量配置，并通过 GitLab CI 或 Jenkins 接入 Fastlane 自动触发构建流程。这样极大地减少了人工打包出错率，提高了测试协作效率。

-  

- 我曾主导优化了启动速度。启动时我们发现主线程阻塞达 1.5 秒，影响用户体验（S）。我调研了 Instrument、Time Profiler，发现 AppDelegate 中业务初始化过多（T）。我将其移至后台并用 GCD 优化异步链路，并配合主线程卡顿监控模块（A）。最终将启动时间从 2.2 秒降到 0.8 秒（R）。

## 谈薪资技巧和话术

### 非常感谢面试官和公司对我的认可，也很高兴能够通过面试环节。
我对公司和这个岗位都非常感兴趣，尤其是在公司目前快速发展的阶段，有机会参与架构层面是我非常看重的点。
结合目前市场情况和我对本岗位的理解。薪资方面确实和我的期望值有点小差距。如果公司录用我，根据我和前面面试官的交流，我过往的技术经验和管理经验，都是和公司比较匹配的。我还是想给自己争取一个对自己比较满意的薪资的，这样能够让我没有任何顾虑和负担全心投入。我相信入职后能很快的履行好岗位的职责。
我也看了一下目前的行情，类似架构师岗位目前我的薪资属于中等偏下的水平。所以说虽然涨幅有，但是也在合理的水平。
如果是最高预算，那我们试用期是多久？试用期薪资是全额吗？我历任公司试用期都是全额。
工资的结构？五险一金的基数？其他福利？

## Hi, my name is Xueming Wang.
I have ten years of experience in software development,
including nine years focused on iOS,
and five years in technical leadership roles.

I've worked as a technical assistant to CEOs and CIOs in listed companies,
and also in blockchain investment research
at a VC firm called LK Venture.

I'm strong in iOS low-level development and performance architecture（er kei tai ke cher）,
and I’ve led(lai de) benchmark projects in Web3, education, and SDK development.

I’ve led teams of three or more engineers,
and I’m used to driving products from idea to launch.
I enjoy solving (sao wu ling)business problems through technology.

I'm now looking for a role
where I can bring both technical depth and strategic(streeti gi ke) thinking
to help build impactful products.
tanks.


