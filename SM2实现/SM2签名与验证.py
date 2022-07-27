#SM2签名与验证
from random import randint
from gmssl import sm3,func
import math
import hashlib


#推荐使用素数域256位椭圆曲线
#ECC参数
#方程y2=x3+ax+b

p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
GX=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
GY=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0


def gcd(p,q):
    '''欧几里得算法求最大公因子'''
    if q>p:
        p,q=q,p
    while(q!=0):
        p,q=q,p%q
    return p


def xcd(p,n):#前提n,p互质
    '''扩展欧几里得算法求模逆'''
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


def addit(x1,y1,x2,y2,a,p):
    '''两点相加'''
    if(x1==x2 and y1==p-y2):
        return false
    elif(x1==x2):#倍点
        lmd=(((3*x1*x1+a)%p)*xcd(2*y1,p))%p
    else:#两个非互逆的不同点
        lmd=((y2-y1)%p*xcd((x2-x1)%p,p))%p
    x3=(lmd*lmd-x1-x2)%p
    y3=(lmd*(x1-x3)-y1)%p
    return x3,y3
        
    
def multipoint(x,y,k,a,p):
    '''计算椭圆曲线点'''
    k=bin(k)[2:]#变成二进制字符串,获得二进制长度
    xp,yp=x,y
    #类似平方-乘模幂算法
    for i in range(1,len(k)):#循环长度减1次
        xp,yp=addit(xp,yp,xp,yp,a,p)#"平方"
        if k[i]=='1':
            xp,yp=addit(xp,yp,x,y,a,p)#"乘"
    return xp,yp


def KDF(st,klen):
    '''密钥派生函数'''
    ct=1
    k=''
    for i in range(math.ceil(klen/256)):
        tp=hex(int(st+'{:032b}'.format(ct),2))[2:]
        tp1=sm3.sm3_hash(func.bytes_to_list(tp.encode()))
        k+=bin(int(tp1,16))[2:].rjust(256,'0')
        ct+=1
    '''
    #填充
    if klen/256!=klen//256:
        tpp=klen-(256*(klen//256))
        k=k[:(-256+tpp)]
    '''
    return k[:klen]


def sign(ID,dB,xB,yB,m):
    #预处理计算Z值
    ENTL=len(ID)*8#两字节的ID的比特长度
    ID=bin(int(ID.encode().hex(),16))[2:].rjust(ENTL,'0')
    ENTL=bin(ENTL)[2:].rjust(16,'0')
    aa=bin(a)[2:].rjust(256,'0')
    bb=bin(b)[2:].rjust(256,'0')
    aa='{:0256b}'.format(a)
    bb='{:0256b}'.format(b)
    gx='{:0256b}'.format(GX)
    gy='{:0256b}'.format(GY)
    xb='{:0256b}'.format(xB)
    yb='{:0256b}'.format(yB)
    temp=ENTL+ID+aa+bb+gx+gy+xb+yb
    temp=hex(int(temp,2))[2:].rjust(len(temp)//4,'0')#temp必整除4
    Z=getattr(hashlib,'sha256')(temp.encode()).hexdigest()
    Z=bin(int(Z,16))[2:].rjust(256,'0')
    #预处理计算H
    m=bin(int(m.encode().hex(),16))[2:].rjust(len(m)*8,'0')
    temp=hex(int(Z+m,2))[2:].encode()
    H=sm3.sm3_hash(func.bytes_to_list(temp))
    #签名
    #产生随机数k
    while(True):
        k=randint(1,n-1)
        x1,y1=multipoint(GX,GY,k,a,p)
        e=int(H,16)
        r=(e+x1)%n
        if r!=0 and (r+k)!=n:
            s=(xcd(1+dB,n)*(k-r*dB))%n
            if s!=0:
                break
    return Z,r,s
    

def verify(Z,r,s,xB,yB,m):
    #检验数据大小范围
    if r<1 or r>(n-1) or s<1 or s>(n-1):
        return False
    m=bin(int(m.encode().hex(),16))[2:].rjust(len(m)*8,'0')
    temp=hex(int(Z+m,2))[2:].encode()
    H=sm3.sm3_hash(func.bytes_to_list(temp))
    t=(r+s)%n
    if t==0:
        return False
    x11,y11=multipoint(GX,GY,s,a,p)
    x12,y12=multipoint(xB,yB,t,a,p)
    x1,y1=addit(x11,y11,x12,y12,a,p)
    e=int(H,16)
    R=(e+x1)%n
    if R==r:
        return True
    else:
        return False
    

    

#第一步,产生私钥
dB=randint(1,n-1)
#第二步，计算公钥
xB,yB=multipoint(GX,GY,dB,a,p)

print('------------签名------------')
ID='202000460007'
m='wangfangqi'#签名消息
Z,r,s=sign(ID,dB,xB,yB,m)
print("数字签名为:(r={},s={})".format(r,s))

print('------------验证------------')
if_t=verify(Z,r,s,xB,yB,m)
if if_t==True:
    print("验证通过")
else:
    print("验证未通过")
