#e,N已知，不断计算e/N的收敛因子k/d
#之后利用N-(ed-1)//k+1计算p+q
#N=pq,解一元二次方程
#p、q同比特长度，p<q<2p
#收敛因子k1=a1,k2=a2a1+1,pt=atpt-1+pt-2,t>=3
#d1=1,d2=a2,dt=atdt-1+dt-2
#e/N=temp
#b2=1/(w-e),a2=b2向下取整，但是b2的值要保存，可用同一个变量存储，b2用列表
#但是我们追求的只是每个渐进因子的验算，3长的列表即可，甚至2长（要两个）队列
#a.append(新的),a.pop(0)
#from math import sqrt
#发现确定e后再求d大小不能确定其满足条件，所以我们声明满足条件的e，求d，之后交换
#另外，sage中非整数不能取模运算（分数表达/无理数），比较取int与正常计算是否相等
p1=random_prime(2^1024-1,False,2^1023)
q1=random_prime(2^1024-1,False,2^1023)
N=p1*q1
n=(p1-1)*(q1-1)#必为偶数
e=random_prime(int(sqrt(sqrt(N))/6))
dd=xgcd(e,n)[1]
if(dd<0):
    dd=dd+n
e,dd=dd,e
def attack(k,d,N,e):
    tq=N-(e*d-1)/k+1
    T=int(tq)#tq也可能不是整数
    if(tq!=T):
        return False
    #解x^2-Tx+N=0
    tt=T*T-4*N
    if tt>=0:#方程可能有解
        #a可能不是有理数，这种情况下取模计算会出错
        a=int(sqrt(tt))
        if (T+a)%2==0 and (a^2-tt)==0:#在此处加上a是整数的条件
            print('p=',(T+a)/2,'\n','q=',(T-a)/2)
            return True
    return False
def aat(e,N):
    #第一个渐进分数
    jdg=False
    k=[0]
    d=[0]#不断更新
    temp=e/N
    a=int(temp)
    k.append(a)
    d.append(1)
    #第二个渐进分数
    temp=1/(temp-a)
    a=int(temp)
    k.append(a*k[1]+1)
    pp=k.pop(0)
    d.append(a)
    pp=d.pop(0)#k,d数组保持2长
    jdg=attack(k[1],d[1],N,e)
    while(jdg==False):
        temp=1/(temp-a)#循环
        a=int(temp)
        k.append(a*k[1]+k[0])
        pp=k.pop(0)
        d.append(a*d[1]+d[0])
        pp=d.pop(0)
        #print(k,d)#更新列表
        jdg=attack(k[1],d[1],N,e)
%time aat(e,N)


    



    
