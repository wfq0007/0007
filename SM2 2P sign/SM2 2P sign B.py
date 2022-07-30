#SM2 2P sign B
from random import randint
from gmssl import sm3,func
import math
import hashlib
import socket


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


HOST=socket.gethostname()
PORT=50007
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#实例化套接字
s.bind((HOST,PORT))#绑定socket
s.listen()
print('Listening on port:',PORT)
while True:
    try:
        conn,addr=s.accept()
    except:
        break
    print('Connected by',addr)
    while(True):
        d2=randint(1,n-1)
        if gcd(d2,n)==1:
            d2_=xcd(d2,n)
            break
    p1=conn.recv(1024).decode()
    p1x=int(p1[:64],16)
    p1y=int(p1[64:],16)
    pxtemp,pytemp=multipoint(p1x,p1y,d2_,a,p)
    px,py=addit(pxtemp,pytemp,GX,-GY,a,p)
    temp=hex(px)[2:].rjust(64,'0')+hex(py)[2:].rjust(64,'0')
    conn.send(temp.encode())
    #接收Q1，e
    q1_e=conn.recv(1024).decode()
    Q1x=int(q1_e[:64],16)
    Q1y=int(q1_e[64:128],16)
    e=int(q1_e[128:],16)
    k2=randint(1,n-1)
    Q2x,Q2y=multipoint(GX,GY,k2,a,p)
    k3=randint(1,n-1)
    tpx,tpy=multipoint(Q1x,Q1y,k3,a,p)
    x1,y1=addit(tpx,tpy,Q2x,Q2y,a,p)
    r=(x1+e)%n
    s2=(d2*k3)%n
    s3=(d2*(r+k2))%n
    #发送r,s2,s3
    r_temp=hex(r)[2:].rjust(64,'0')
    s2_temp=hex(s2)[2:].rjust(64,'0')
    s3_temp=hex(s3)[2:].rjust(64,'0')
    conn.send((r_temp+s2_temp+s3_temp).encode())
    
s.close()



