#PGP B
#接收方解密

import socket
from random import randint
from gmssl import sm3,func
import math
import hashlib
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT



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
db=0x5E35D7D3F3C54DBAC72E61819E730B019A84208CA3A35E4C2E353DFCCB2A3B53

xb=0x245493D446C38D8CC0F118374690E7DF633A8A4BFB3329B5ECE604B2B4F37F43
yb=0x53C0869F4B9E17773DE68FEC45E14904E0DEA45BF6CECF9918C85EA047C60A4C
#A的公钥
xa=0x3099093BF3C137D8FCBBCDF4A2AE50F3B0F216C3122D79425FE03A45DBFE1655
ya=0x3DF79E8DAC1CF0ECBAA2F2B49D51A4B387F2EFAF482339086A27A8E05BAED98B

def get_Z(ID,xB,yB):
    #预处理计算Z值
    ENTL=len(ID)*8#两字节的ID的比特长度
    ID=hex(int(ID.encode().hex(),16))[2:].rjust(ENTL//4,'0')
    ENTL=hex(ENTL)[2:].rjust(4,'0')
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

def keyexchange_B(IDa,IDb):
    #IDa='ALICE123@YAHOO.COM'
    #IDb='BILL456@TAHOO.COM'
    Za=get_Z(IDa,xa,ya)
    Zb=get_Z(IDb,xb,yb)
    w=math.ceil(math.ceil(math.log2(n))/2)-1
    klen=128

    #密钥交换，获得会话密钥
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
        rb=randint(1,n-1)
        Rbx,Rby=multipoint(GX,GY,rb,a,p)
        x2_=pow(2,w)+(Rbx&(pow(2,w)-1))
        tb=(db+x2_*rb)%n
        #接收Ra
        Ra=conn.recv(1024).decode()
        Rax=int(Ra[:64],16)
        Ray=int(Ra[64:],16)
        if pow(Ray,2,p)==(pow(Rax,3,p)+a*Rax+b)%p:
            print("Ra满足曲线方程")
        else:
            print("协商失败")
        #第五步
        x1_=pow(2,w)+(Rax&(pow(2,w)-1))
        V_tx,V_ty=multipoint(Rax,Ray,x1_,a,p)
        V_tx,V_ty=addit(xa,ya,V_tx,V_ty,a,p)
        xv,yv=multipoint(V_tx,V_ty,h*tb,a,p)
        xv='{:0256b}'.format(xv)
        yv='{:0256b}'.format(yv)
        #判断是否为无穷远点
        #第七步
        Kb=KDF(xv+yv+Za+Zb,klen)
        print(hex(int(Kb,2))[2:])
        #第八步
        tempsb=hex(int(xv,2))[2:].rjust(64,'0')+hex(int(Za,2))[2:].rjust(64,'0')+hex(int(Zb,2))[2:].rjust(64,'0')
        tempsb=tempsb+Ra+hex(Rbx)[2:].rjust(64,'0')+hex(Rby)[2:].rjust(64,'0')
        tempsb=sm3.sm3_hash(func.bytes_to_list(tempsb.encode()))
        tpsb='02'+hex(int(yv,2))[2:].rjust(64,'0')+tempsb
        Sb=sm3.sm3_hash(func.bytes_to_list(tpsb.encode()))
        #将Rb,Sb发送给A
        temp = hex(Rbx)[2:].rjust(64, '0') + hex(Rby)[2:].rjust(64, '0')
        conn.send((temp+Sb).encode())
        #计算S2
        tps2='03'+tpsb[2:]
        S2=sm3.sm3_hash(func.bytes_to_list(tps2.encode()))
        #接收Sa
        Sa=conn.recv(1024).decode()
        #验证S2==SA
        if S2==Sa:
            print("从A到B的密钥确认成功")
        else:
            print("协商失败")   
        s.close()
    return hex(int(Kb,2))[2:]


def decrypt(dB,c,a,b,p):
    '''解密'''
    #首先提取c1,c2,c3
    plen=len(hex(p)[2:])
    c1=c[:(2*plen+2)][2:]#并去掉'04'
    c2=c[(2*plen+2):-64]
    c3=c[-64:]
    klen=(len(c)-2-plen*2-64)*4
    #验证C1是否满足曲线方程y2=x3+ax+b
    x1=int(c1[:plen],16)
    y1=int(c1[plen:],16)
    if pow(y1,2,p)!=(pow(x1,3,p)+a*x1+b)%p:
        print('aa')
        return False
    #计算x2,y2
    x2,y2=multipoint(x1,y1,dB,a,p)
    x2='{:0256b}'.format(x2)
    y2='{:0256b}'.format(y2)
    #计算t
    t=KDF(x2+y2,klen)
    if t==0:
        print('aa')
        return False
    #计算M'
    m=bin(int(c2,16)^int(t,2))[2:].rjust(klen,'0')
    #验证hash
    temp=hex(int(x2+m+y2,2))[2:].encode()#转为字节串
    u=sm3.sm3_hash(func.bytes_to_list(temp))
    if u!=c3:
        print('ab')
        return False
    m=hex(int(m,2))[2:]
    m=str(bytes.fromhex(m))
    return m



#Generate session key：SM2 key exchange
IDa='ALICE123@YAHOO.COM'
IDb='BILL456@TAHOO.COM'
key=keyexchange_B(IDa,IDb)
#接收，依次解密
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
    c=conn.recv(1024).decode()
    conn.send("received".encode())
    encrypt_value=conn.recv(1024)
    keyy=decrypt(db,c,a,b,p)#解密密钥
    #解密数据
    crypt_sm4=CryptSM4()
    crypt_sm4.set_key(key.encode(),SM4_DECRYPT)
    decrypt_value=crypt_sm4.crypt_ecb(encrypt_value)
    print("解密获得的数据")
    print(decrypt_value.decode())
    conn.send("received".encode())
s.close()
    
    
