#RSA加密算法

import math
import random
import time

#编写求最大公因子的函数
def gcd(p,q):
    #欧几里得算法。
    if q>p:
        p,q=q,p
    while(q!=0):
        p,q=q,p%q
    return p

#编写求模逆的扩展欧几里得算法
def xcd(p,n):#前提n,p互质
    #扩展欧几里得算法
    s=[1,0]
    t=[0,1]
    r=[n,p]
    rr=n%p
    while(rr!=0):
        q=r[0]//r[1]
        r.append(rr)
        s.append(s[0]-q*s[1])
        t.append(t[0]-q*t[1])#边做带余除法边线性表出
        r.pop(0);s.pop(0);t.pop(0)
        rr=r[0]%r[1]
    return t[1]#r=s*n+t*p,t[1]为模逆

#编写rabin-miller素性检测算法函数
def is_prime(p):
    d=p-1
    s=0
    while(d%2==0):
        d=d//2
        s+=1
    a=random.randint(2,p-1)
    if(s==0):#p为偶数时
        return False 
    for r in range(s-1,-1,-1):
        z=pow(a,(2**r)*d,p)
        if(z==p-1):
            return True
        if(z!=p-1 and z!=1):
            return False
        #z=1继续循环，开平方
    return True
          
#编写生成大素数的算法函数
def get_prime(key_size=1024):
    while True:
        num=random.randrange(2**(key_size-1),2**key_size)
        if is_prime(num):
            return num

#编写生成RSA公私钥对的函数
def create_RSA():
    global p,q,N,fn,e,d
    #公开N,e,私密p,q,d
    p=get_prime()
    q=get_prime()
    N=p*q
    fn=(p-1)*(q-1)
    #随机生成公钥
    while True:
        e=random.randint(2,fn-1)
        if gcd(e,fn)==1:
            break
    d=xcd(e,fn)#求私钥
    if(d<0):
        d=d+fn
    return True

#编写RSA加密和解密函数
#明文为
#为了统一，测试时的明文长度先规定为hash256，即256bit，当然也可随便调整
m=random.randrange(2**(256-1),2**256)
p=q=N=fn=e=d=0

start_time=time.time()
create_RSA()
print('生成公私钥对时间:{}\n'.format(time.time()-start_time))
#print('p:{}\nq:{}\nN:{}\ne:{}\nd:{}\n'.format(p,q,N,e,d))
print("d",d)

def encrypt(plaintext):#公钥加密
    global p,q,N,fn,e,d
    return pow(plaintext,e,N)

def decrypt(ciphertext):#私钥解密
    global p,q,N,fn,e,d
    return pow(ciphertext,d,N)

def sign(text):#私钥签名
    global p,q,N,fn,e,d
    return pow(text,d,N)

def verify(textt,text):#公钥验证
    global p,q,N,fn,e,d
    if pow(textt,e,N)==text:
        return True
    return False

start_time=time.time()
ct=encrypt(m)
print('加密耗时:{}\n'.format(time.time()-start_time))

start_time=time.time()
pt=decrypt(ct)
print('解密耗时:{}\n'.format(time.time()-start_time))

start_time=time.time()
sm=sign(m)
print('签名耗时:{}\n'.format(time.time()-start_time))

start_time=time.time()
vm=verify(sm,ct)#true为验证通过，false不通过
print('验证耗时:{}\n'.format(time.time()-start_time))

























    
