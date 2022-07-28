#ECMH，将hash求和转换为椭圆曲线上点的和
#未花费的交易输出，UTXO
#这里并不关心UTXO是怎么得到的，随机字符串获得摘要。注重在于实现ECMH
from gmssl import sm3,func
import random
import string
import math

def random_string_generate(size,allowed_chars):
    return ''.join(random.choice(allowed_chars)for x in range(size))

allowed_chars=string.ascii_letters+string.punctuation



#求和

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


def addd(lst,num):
    '''映射相加'''
    lilist=[]
    for i in range(num):
        tp=lst[i]
        #映射方式为，赋值x，求y,若是二次非剩余，则逐次加1
        x1=int(tp,16)
        while(True):
            temp=(pow(x1,3,p)+a*x1+b)%p
            if pow(temp,(p-1)//2,p)==1:
                break
            x1+=1
        y1,y1_=TS(temp,p)
        lilist.append((x1,y1))  
    #print(lilist)
    #相加
    x1=lilist[0][0]
    y1=lilist[0][1]
    for i in range(1,num):
        x2=lilist[i][0]
        y2=lilist[i][1]
        x1,y1=addit(x1,y1,x2,y2,a,p)
    return x1,y1


#所有UTXO
lst=[]
num=10
for i in range(num):
    temp=random_string_generate(50,allowed_chars)
    lst.append(sm3.sm3_hash(func.bytes_to_list(temp.encode())))
X,Y=addd(lst,num)
#转回哈希值，只要X
H=hex(X)[2:].rjust(64,'0')
print("生成:",H)

#修改记录
def xg_UTXO(aa,bb,X,Y):#将a改为b:
    x1=int(aa,16)
    while(True):
        temp=(pow(x1,3,p)+a*x1+b)%p
        if pow(temp,(p-1)//2,p)==1:
            break
        x1+=1
    y1,y1_=TS(temp,p)
    X,Y=addit(X,Y,x1,-y1,a,p)
    x2=int(bb,16)
    while(True):
        temp=(pow(x2,3,p)+a*x2+b)%p
        if pow(temp,(p-1)//2,p)==1:
            break
        x2+=1
    y2,y2_=TS(temp,p)
    X,Y=addit(X,Y,x2,y2,a,p)
    return X,Y

def add_UTXO(aa,X,Y):
    x1=int(aa,16)
    while(True):
        temp=(pow(x1,3,p)+a*x1+b)%p
        if pow(temp,(p-1)//2,p)==1:
            break
        x1+=1
    y1,y1_=TS(temp,p)
    X,Y=addit(X,Y,x1,y1,a,p)
    return X,Y

def delete_UTXO(aa,X,Y):
    x1=int(aa,16)
    while(True):
        temp=(pow(x1,3,p)+a*x1+b)%p
        if pow(temp,(p-1)//2,p)==1:
            break
        x1+=1
    y1,y1_=TS(temp,p)
    X,Y=addit(X,Y,x1,-y1,a,p)
    return X,Y
    
temp=random_string_generate(50,allowed_chars)
bb=sm3.sm3_hash(func.bytes_to_list(temp.encode()))
aa=lst[num-3]
X,Y=xg_UTXO(aa,bb,X,Y)
H=hex(X)[2:].rjust(64,'0')
print("修改:",H)

X,Y=xg_UTXO(bb,aa,X,Y)
H=hex(X)[2:].rjust(64,'0')
print("改回:",H)

temp=random_string_generate(50,allowed_chars)
aa=sm3.sm3_hash(func.bytes_to_list(temp.encode()))
X,Y=add_UTXO(aa,X,Y)
H=hex(X)[2:].rjust(64,'0')
print("添加:",H)


temp=random_string_generate(50,allowed_chars)
aa=sm3.sm3_hash(func.bytes_to_list(temp.encode()))
X,Y=delete_UTXO(aa,X,Y)
H=hex(X)[2:].rjust(64,'0')
print("删去:",H)
    
    
