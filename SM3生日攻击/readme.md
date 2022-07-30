project：implement the naïve birthday attack of reduced SM3

在c++上实现了SM3生日攻击。

基本思想为确定穷举消息长度。

一半建表一半查表。

本代码一半一半分割方式为前一个字节的最后比特。

找到的碰撞是从最左端开始，连续num_b字节哈希值相同。

最多是建表/穷举范围2^^16。

碰撞长度32bit。

![X(8L`KAV_A3@0V2_DVB4Q`U](https://user-images.githubusercontent.com/105547875/181907789-21309860-5602-416a-b07d-c6ac737676e3.png)

![GDJIL_VJV{2WRE(8} D$H~8](https://user-images.githubusercontent.com/105547875/181907793-b45b1c87-18ec-44ac-8eb3-320a5e3210ae.png)

![AF03T 6`}3H $KJXMD8M$32](https://user-images.githubusercontent.com/105547875/181907795-243842c1-6a8d-42be-975a-5a79c787bcf7.png)

![SWK8OV73D7RJCICKX`_$HEN](https://user-images.githubusercontent.com/105547875/181907797-e92123d2-b545-4507-a287-3b347eac6fdc.png)
