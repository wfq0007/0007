#调用DES密码库
#这里假定明文密钥均为64
from Crypto.Cipher import DES
import time
from os import urandom

'''
plaintext=0x02468aceeca86420
key=0xff14717847d8e859
#DES密码库接受字节形式的明文，要对明文密钥进行处理
def by_byte(x):#按16进制解析明文密钥翻译为字节串
    x=hex(x)[2:]
    x=x.rjust(16,'0')
    #print(x)
    byte_8=b''
    for i in range(8):
        a=x[2*i:2*(i+1)]
        byte_8+=bytes.fromhex(a)
    return byte_8

plt=by_byte(plaintext)
k=by_byte(key)#01字符串
'''
#plt=bytes.fromhex('0000000000000000')
plt=bytes.fromhex('83b5e3f5f7902d8f')
k=bytes.fromhex('ac4a4a1235789abd')

#加密函数（调用密码库
def ept(p,k):
    des=DES.new(k,DES.MODE_ECB)#实例化DES对象
    x=des.encrypt(p)#encrypt
    '''
    cipher=''
    for i in x:#二进制输出
        a=bin(i)[2:]
        a=a.rjust(8,'0')
        cipher+=a
    #print(cipher)
    return cipher
    '''
    print(x.hex())
    print(type(x.hex()))
    return x

ept(plt,k)

'''
start_time=time.time()
for i in range(1000):
    pltt=urandom(8)
    keyy=urandom(8)
    ept(pltt,keyy)
print('平均1次所需时间:{}'.format((time.time()-start_time)/1000))
'''
