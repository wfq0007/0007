#调用DES密码库穷举攻击
#在去掉校验位影响的情况下，同一明文下，不同密钥不会加密得到相同密文
from Crypto.Cipher import DES
import time

plaint1=bytes.fromhex('0000000000000000')
cipher1=bytes.fromhex('b788bdfc42d1fdaf')
#遍历密钥找到正确的解
sk=bytes.fromhex('1235789abd')
head=0b000000000000000000000
tail=0b111111111111111111111

start_time=time.time()
for i in range(head,tail+1):
    #设置key
    k=bin(i)[2:].rjust(21,'0')
    kk=k[:7]+'0'+k[7:14]+'0'+k[14:]+'0'#加上校验位的零一比特串
    kkk=hex(int(kk,2))[2:].rjust(6,'0')
    key=bytes.fromhex(kkk)+sk
    #加密
    des=DES.new(key,DES.MODE_ECB)#实例化DES对象
    c1=des.encrypt(plaint1)
    if(c1==cipher1):
        key_true=k
        break #找到后退出
print('穷举攻击时间:{}'.format((time.time()-start_time)))

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
key_all=add_jyw(key_true)
print('密钥个数为：',len(key_all))
print(key_all)

