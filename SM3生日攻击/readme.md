在c++上实现了SM3生日攻击。//
基本思想为确定穷举消息长度。
一半建表一半查表。
本代码一半一半分割方式为前一个字节的最后比特。
本代码的局限性在于穷举长度以字节为单位，只能9，17，25......长。
另一个遗憾的是，由于本人电脑配置与时间，并未找到碰撞。![G4R(VQI$B4FPA3IH~N7W}(L](https://user-images.githubusercontent.com/105547875/180764225-2692c98d-0d44-4da9-9f58-6ca6c72539d5.png)
![3CTPS6LU% 4{CUH$10 VVIF](https://user-images.githubusercontent.com/105547875/180764244-1037b755-ae5f-4320-986d-45e3d488932c.png)
