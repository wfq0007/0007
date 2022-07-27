#Deduce public key from signature
#从签名推出公钥
from random import randint
from gmssl import sm3,func
import math
import hashlib

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


def TS(n,p):
    '''Tonelli-Shanks算法开平方'''
    tp=p-1
    S=0
    while(tp%2==0):
        tp=tp//2
        S+=1
    if S==1:
        R1=pow(n,(p+1)//4,p)
        R2=(-R1)%p
        return R1,R2
    while(True):
        z=randint(1,p)
        L=pow(z,(p-1)//2,p)
        if L==p-1:
            break
    c=pow(z,tp,p)
    R=pow(n,(tp+1)//2,p)
    t=pow(n,tp,p)
    m=S
    if t==1:
        return R,p-R
    else:
        i=0
        while t%p!=1:
            temp=pow(t,2**(i+1),p)
            i+=1
            if temp%p==1:
                b=pow(c,2**(m-i-1),p)
                R=R*b%p
                c=b*b%p
                t=t*c%p
                m=i
                i=0
        return R,p-R
            


def get_pa(Z,r,s,m):
    '''Deduce public key from signature'''
    #PA=(s+r)-1*(kG-sG)
    #获得KG,首先求e,之后求x1,求y1,(x1,y1)=[k]G
    m=bin(int(m.encode().hex(),16))[2:].rjust(len(m)*8,'0')
    temp=hex(int(Z+m,2))[2:].encode()
    H=sm3.sm3_hash(func.bytes_to_list(temp))
    e=int(H,16)
    x1=(r-e)%n
    #计算y1
    #方程y2=x3+ax+b
    temp=(pow(x1,3,p)+a*x1+b)%p
    #Tonelli-Shanks算法
    y1,y1_=TS(temp,p)
    #计算公钥，两组
    tp1=xcd((r+s)%n,n)
    xs,ys=multipoint(GX,GY,s,a,p)
    x_1,y_1=addit(x1,y1,xs,-ys,a,p)
    x_2,y_2=addit(x1,y1_,xs,-ys,a,p)
    pax1,pay1=multipoint(x_1,y_1,tp1,a,p)
    pax2,pay2=multipoint(x_2,y_2,tp1,a,p)
    return pax1,pay1,pax2,pay2



#第一步,产生私钥
dB=randint(1,n-1)
#第二步，计算公钥
xB,yB=multipoint(GX,GY,dB,a,p)
print(xB,yB)

print('------------签名------------')
ID='202000460007'
m='wangfangqi'#签名消息
Z,r,s=sign(ID,dB,xB,yB,m)
print("数字签名为:(r={},s={})".format(r,s))

print('------------从签名中获取公钥------------')
PAX1,PAY1,PAX2,PAY2=get_pa(Z,r,s,m)
if(PAX1==xB and PAY1==yB):
    print("成功提取1")
    print("公钥为:(x={},y={})".format(PAX1,PAY1))
elif(PAX2==xB and PAY2==yB):
    print("成功提取2")
    print("公钥为:(x={},y={})".format(PAX2,PAY2))

