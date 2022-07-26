添加了SIMD与循环扩展，以及运算符替换（乘除改为移位），减少引用次数。

不过由于优化的是部分部件，效率并未达到明显提高。

杂凑运算的迭代下一轮使用上一轮的结果，无法多线程并行。


![6{$ZOF2ECL9FVYX6VFQA02F](https://user-images.githubusercontent.com/105547875/180986854-171e34ea-f723-4b37-9fdd-56b601dd25a9.png)

![V7U}PP_LV2OUXEM2EO`Z31Y](https://user-images.githubusercontent.com/105547875/180986940-de4b4b5a-870d-4138-a013-88b92994f936.png)
