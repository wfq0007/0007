#实现Miller-Rabin算法
import random
import time

#2048_bit长
p=random.randint(2**2047,2**2048-1)

def pf_multi(x,b,n):
    z=1
    b=bin(b)[2:]
    for i in range(len(b)):
        z=z*z%n
        if b[i]=='1':
            z=z*x%n
    return z


def M_R(n):
    fn=n-1
    u=0
    while(fn%2==0):
        fn=fn>>1
        u+=1
    a=random.randint(2,n-1)
    b=pf_multi(a,fn,n)
    if(b==1):
        #print("p is prime")
        return 1
    for i in range(0,u):
        if(b==n-1):
            #print("p is prime")
            return 1
        b=b*b%n
    #print("p is composite")
    return 0


start_time=time.time()
if_print=False
for i in range(30):#重复30次，降低错误概率
    a=M_R(p)
    if(a==0):
        if_print=True
        print("p is composite")
        num=i+1
        break
if(if_print==False):
    print("p is prime")
    num=30
print("单次Miller-Rabin算法时间为{}s".format((time.time()-start_time)/num))
