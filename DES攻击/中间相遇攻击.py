#2重DES的中间相遇攻击
#一头加密，一头解密，碰撞
#加密存表，解密每轮在线查表
from Crypto.Cipher import DES
import time

plaint1=bytes.fromhex('0000000000000000')
cipher1=bytes.fromhex('c51383ff56e6f967')
sk=bytes.fromhex('1235789abd')
head=0b000000000000000000000
tail=0b111111111111111111111
cipher_list=[]#明文加密的存储表格

start_time=time.time()
#预先建立明文的一轮DES密文密钥表
for i in range(head,tail+1):
    #设置key
    k=bin(i)[2:].rjust(21,'0')
    kk=k[:7]+'0'+k[7:14]+'0'+k[14:]+'0'#加上校验位的零一比特串
    kkk=hex(int(kk,2))[2:].rjust(6,'0')
    key=bytes.fromhex(kkk)+sk
    #加密
    des=DES.new(key,DES.MODE_ECB)#实例化DES对象
    c1=des.encrypt(plaint1)
    #存表
    cipher_list.append(c1)#根据密文的索引可求出密钥
print('table finished')
print('建表时间{}'.format(time.time()-start_time))

start2_time=time.time()
#密文解密方向在线穷举并查找明文方向密文密钥表
for i in range(head,tail+1):
    #设置key
    k=bin(i)[2:].rjust(21,'0')
    kk=k[:7]+'0'+k[7:14]+'0'+k[14:]+'0'#加上校验位的零一比特串
    kkk=hex(int(kk,2))[2:].rjust(6,'0')
    key=bytes.fromhex(kkk)+sk
    #解密
    des=DES.new(key,DES.MODE_ECB)
    p2=des.decrypt(cipher1)
    #查表
    if p2 in cipher_list:
        index_c=cipher_list.index(p2)
        k1_true=bin(index_c)[2:].rjust(21,'0')
        k2_true=bin(i)[2:].rjust(21,'0')#最后手动转换一下索引即为密钥
        break #找到后退出
print('中间相遇攻击时间{}'.format(time.time()-start2_time))

def add_jyw(k):#加上校验位后的8个密钥
    k_all=[]
    a=k[:7]+'0'+k[7:14]+'0'+k[14:]+'0'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'0'+k[7:14]+'0'+k[14:]+'1'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'0'+k[7:14]+'1'+k[14:]+'0'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'0'+k[7:14]+'1'+k[14:]+'1'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'1'+k[7:14]+'0'+k[14:]+'0'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'1'+k[7:14]+'0'+k[14:]+'1'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'1'+k[7:14]+'1'+k[14:]+'0'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    a=k[:7]+'1'+k[7:14]+'1'+k[14:]+'1'
    k_all.append(hex(int(a,2))[2:].rjust(6,'0')+'1235789abd')
    return k_all
key1_all=add_jyw(k1_true)
print('密钥个数为：',len(key1_all))
print(key1_all)
key2_all=add_jyw(k2_true)
print('密钥个数为：',len(key2_all))
print(key2_all)

