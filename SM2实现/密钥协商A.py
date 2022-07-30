#密钥协商A
import socket
import sys
from random import randint
from gmssl import sm3,func
import math
import hashlib

#推荐使用素数域256位椭圆曲线
#ECC参数
#方程y2=x3+ax+b

p=0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a=0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b=0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n=0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
GX=0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
GY=0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
h=1

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




#私钥与公钥
da=0x6FCBA2EF9AE0AB902BC3BDE3FF915D44BA4CC78F88E2F8E7F8996D3B8CCEEDEE
xa=0x3099093BF3C137D8FCBBCDF4A2AE50F3B0F216C3122D79425FE03A45DBFE1655
ya=0x3DF79E8DAC1CF0ECBAA2F2B49D51A4B387F2EFAF482339086A27A8E05BAED98B
#B的公钥
xb=0x245493D446C38D8CC0F118374690E7DF633A8A4BFB3329B5ECE604B2B4F37F43
yb=0x53C0869F4B9E17773DE68FEC45E14904E0DEA45BF6CECF9918C85EA047C60A4C



def get_Z(ID,xB,yB):
    #预处理计算Z值
    ENTL=len(ID)*8#两字节的ID的比特长度
    ID=hex(int(ID.encode().hex(),16))[2:].rjust(ENTL//4,'0')
    ENTL=hex(ENTL)[2:].rjust(4,'0')
    #print(ENTL)
    aa = hex(a)[2:].rjust(64, '0')
    bb = hex(b)[2:].rjust(64, '0')
    gx = hex(GX)[2:].rjust(64, '0')
    gy = hex(GY)[2:].rjust(64, '0')
    xb = hex(xB)[2:].rjust(64, '0')
    yb = hex(yB)[2:].rjust(64, '0')
    temp=ENTL+ID+aa+bb+gx+gy+xb+yb
    Z=sm3.sm3_hash(func.bytes_to_list(temp.encode()))
    Z=bin(int(Z,16))[2:].rjust(256,'0')
    return Z


IDa='ALICE123@YAHOO.COM'
IDb='BILL456@TAHOO.COM'
Za=get_Z(IDa,xa,ya)
Zb=get_Z(IDb,xb,yb)
w=math.ceil(math.ceil(math.log2(n))/2)-1
klen=128

#密钥交换，获得会话密钥
HOST=socket.gethostname()
PORT=50007
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((HOST,PORT))#连接服务器
except Exception as e:
    print('B not found or not open')
    sys.exit()
else:
    # 产生随机数ra
    ra = randint(1, n - 1)
    #ra=0x83A2C9C8B96E5AF70BD480B472409A9A327257F1EBB73F5B073354B248668563
    Rax, Ray = multipoint(GX, GY, ra, a, p)
    temp = hex(Rax)[2:].rjust(64, '0') + hex(Ray)[2:].rjust(64, '0')
    s.send(temp.encode())
    x1_=pow(2,w)+(Rax&(pow(2,w)-1))
    ta=(da+x1_*ra)%n
    js=s.recv(1024).decode()
    Sb=js[128:]
    Rb=js[:128]
    Rbx=int(Rb[:64],16)
    Rby=int(Rb[64:],16)
    if pow(Rby, 2, p) == (pow(Rbx, 3, p) + a * Rbx + b) % p:
        print("Rb满足曲线方程")
    else:
        print("协商失败")
    #第六步
    x2_ = pow(2, w) + (Rbx & (pow(2, w) - 1))
    U_tx, U_ty = multipoint(Rbx, Rby, x2_, a, p)
    U_tx, U_ty = addit(xb, yb, U_tx, U_ty, a, p)
    xu, yu = multipoint(U_tx, U_ty, h * ta, a, p)
    xu = '{:0256b}'.format(xu)
    yu = '{:0256b}'.format(yu)
    #以上数据都没问题
    #判断是否为无穷远点
    Ka = KDF(xu + yu + Za + Zb, klen)
    print(hex(int(Ka,2))[2:])
    temps1=hex(int(xu,2))[2:].rjust(64,'0')+hex(int(Za,2))[2:].rjust(64,'0')+hex(int(Zb,2))[2:].rjust(64,'0')
    temps1=temps1+hex(Rax)[2:].rjust(64,'0')+hex(Ray)[2:].rjust(64,'0')+Rb
    tps1=sm3.sm3_hash(func.bytes_to_list(temps1.encode()))
    tps1='02'+hex(int(yu,2))[2:].rjust(64,'0')+tps1
    S1=sm3.sm3_hash(func.bytes_to_list(tps1.encode()))
    if S1 == Sb:
        print("从B到A的密钥确认成功")
        tpsa='03'+tps1[2:]
        Sa=sm3.sm3_hash(func.bytes_to_list(tpsa.encode()))
        s.send(Sa.encode())
    else:
        print("协商失败")


s.close()
