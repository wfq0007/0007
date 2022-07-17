#删除E扩展和S盒
#DES加密算法

plaintext=0x02468aceeca86420
key=0xff14717847d8e859

def by_bit(x):#按16进制解析明文密钥翻译为01串
    b_64=bin(x)[2:]
    b_64=b_64.rjust(64,'0')
    return b_64

plt=by_bit(plaintext)
k=by_bit(key)#01字符串

def by_16(x):#16进制输出
    text=''
    for i in range(16):
        a=int(x[4*i])*8+int(x[4*i+1])*4+int(x[4*i+2])*2+int(x[4*i+3])
        text+=hex(a)[2]
    return text
        

#初始IP置换
def IP(p):
    IP=[58,50,42,34,26,18,10,2,
        60,52,44,36,28,20,12,4,
        62,54,46,38,30,22,14,6,
        64,56,48,40,32,24,16,8,
        57,49,41,33,25,17,9,1,
        59,51,43,35,27,19,11,3,
        61,53,45,37,29,21,13,5,
        63,55,47,39,31,23,15,7]
    pp=''
    for i in range(64):
        pp+=p[IP[i]-1]
    #print('IP置换',pp)
    return pp

def IP_invert(p):
    IP=[40,8,48,16,56,24,64,32,
        39,7,47,15,55,23,63,31,
        38,6,46,14,54,22,62,30,
        37,5,45,13,53,21,61,29,
        36,4,44,12,52,20,60,28,
        35,3,43,11,51,19,59,27,
        34,2,42,10,50,18,58,26,
        33,1,41,9,49,17,57,25]
    pp=''
    for i in range(64):
        pp+=p[IP[i]-1]
    return pp

    
#以下是密钥编排方案
def PC_1(k):
    PC=[57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4]
    p=''
    for i in range(56):
        p+=(k[PC[i]-1])
    return p

def movel(k,i):#循环左移
    G=[1,1,2,2,2,2,2,2,
       1,2,2,2,2,2,2,1]
    n=G[i]
    return k[n:]+k[:n]

def PC_2(k):
    PC=[14,17,11,24,1,5,
        3,28,15,6,21,10,
        23,19,12,4,26,8,
        16,7,27,20,13,2,
        41,52,31,37,47,55,
        30,40,51,45,33,48,
        44,49,39,56,34,53,
        46,42,50,36,29,32]
    p=''
    for i in range(48):
        p+=(k[PC[i]-1])
    return p

def key_create(k):
    #去除校验位+PC-1置换
    kk=PC_1(k)
    c=kk[:28]
    d=kk[28:]
    #16轮
    key=['']*16#密钥表
    for i in range(16):
        c=movel(c,i)
        d=movel(d,i)#循环移位
        key[i]=PC_2(c+d)#PC_2置换
    return key


#以下是f函数相关
def P(r):#P置换
    P=[16,7,20,21,
       29,12,28,17,
       1,15,23,26,
       5,18,31,10,
       2,8,24,14,
       32,27,3,9,
       19,13,30,6,
       22,11,4,25]
    p=''
    for i in range(32):
        p+=r[P[i]-1]
    return p
            
def funcf(r,k):
    listt=[]#存储异或加分组
    #改为与密钥前32位异或
    for i in range(8):
        listt.append([])
        for j in range(4):
            n=int(r[4*i+j])^int(k[4*i+j])
            listt[i].append(n)
    textt=''
    for i in listt:
        for j in i:
            textt+=str(j)
    #P置换
    return P(textt)


#DES加密主体部分
def ept(p,k):#一组64bit
    #获取密钥表
    key=key_create(k)
    #初始置换IP
    p=IP(p)
    #左，右
    pl=p[:32]
    pr=p[32:]
    for i in range(6):
        pl_new=pr
        prk=funcf(pr,key[i])#f函数
        #pl与prk异或（32bit)
        pr_new=''
        for j in range(32):
            n=int(pl[j])^int(prk[j])
            pr_new+=str(n)
        #print('第{}轮密文为{}'.format(i+1,by_16(pl_new+pr_new)))
        pl=pl_new
        pr=pr_new
    print('6轮加密后{}'.format(by_16(pl+pr)))
    #IP逆置换
    cipher=IP_invert(pr+pl)
    return cipher


#逐比特修改明文/密钥
print('删除E扩散和S盒')
plt=plt[:64]
k=k[:64]
print('不改变明文')
c_old=ept(plt,k)

#明文由低到高分别改变比特
for i in range(56,64):
    print('改变明文第{}比特'.format(i+1))
    b=int(plt[i])^1
    pp=plt[:i]+str(b)+plt[i+1:]
    c_new=ept(pp,k)
    #异或得出几个比特改变
    n=0
    for i in range(64):
        n+=int(c_old[i])^int(c_new[i])
    print('改变了 {} 个比特'.format(n))
print('\n')

#密钥由低到高分别改变比特
print('不改变密钥')
print(c_old)
for i in range(56,64):
    print('改变密钥第{}比特'.format(i+1))
    b=int(k[i])^1
    kk=k[:i]+str(b)+k[i+1:]
    c_new=ept(plt,kk)
    #异或得出几个比特改变
    n=0
    for i in range(64):
        n+=int(c_old[i])^int(c_new[i])
    print('改变了 {} 个比特'.format(n))
        
        
        
        
        
