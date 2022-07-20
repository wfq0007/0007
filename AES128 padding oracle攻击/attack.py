import subprocess
from time import time
from Crypto.Util.number import long_to_bytes

iv="4e9bd8fb5331702fb4a7ea7e0b9ec337"
c1="0e4ac53f9f569e53ccb0e035f9c8ed4f"
c2="ddc0f0c4e4d41b2d3b70a1d73fa6d7f5"
c3="3ac4758c8e179d4a1f1a47978c879205"
b=16 #每个分组的字节数

def ayyy(tt,y):
    
    #以上一组密文tt的前15个字节作为r1-r15,穷举r16找到满足pad的r
    r=tt[:30]
    for i in range(0x00,0x100):
        tp_rb=hex(i)[2:].rjust(2,'0')
        r_y=r+tp_rb+y
        output=subprocess.call(["dec_oracle.exe",r_y])
        if output==200:
            r+=tp_rb
            break
        
        
    #进一步判断填充的长度，一组16字节，逐字节修改
    #本代码的修改方式为逐字节与1异或
    j=0 #j表示从左至右(由1计数）第几个字节开始pad
    for i in range(b):
        a=hex(int(r[2*i],16)^0b0001)[2]
        rr=r[:(2*i)]+a+r[(2*i)+1:]+y
        output=subprocess.call(["dec_oracle.exe",rr])
        if output==500:
            j=i+1
            break

        
    #根据pad长度，得出pad内容，异或计算aj-ab
    a_list=''
    for i in range(j-1):
        a_list+='00'   #对于a1-aj-1先填充0
    pad=b-j+1   
    for i in range(j-1,b):
        a_list+=hex(int(r[2*i:2*(i+1)],16)^pad)[2:].rjust(2,'0')
        

    
    def arrr(n,a_list):#求aj-n
        num=b-j+1+n   #在pad的基础上加n,n依次为1,2,3.....
        rk=''
        for i in range(j-n,b):
            #对原来填充为pad的改为填充为num，并修改r
            rk+=hex(int(a_list[2*i:2*(i+1)],16)^num)[2:].rjust(2,'0')
        for ar in range(0x00,0x100):
            #穷举所求字节的满足填充为num的aj-n
            r_j=hex(ar)[2:].rjust(2,'0')
            r_new=r[:2*(j-n-1)]+r_j+rk+y
            output=subprocess.call(["dec_oracle.exe",r_new])
            if output==200:
                a_j=hex(ar^num)[2:].rjust(2,'0')
                a_list=a_list[:2*(j-n-1)]+a_j+a_list[2*(j-n):]
                return a_list

            
    #调整填充长度及内容，由右向左逐步计算aj-1,aj-2......a1      
    for i in range(1,j):
        a_list=arrr(i,a_list)
        

    #最终确定的a与上一组密文异或的明文。
    p=hex(int(a_list,16)^int(tt,16))[2:]
    return p


start_time=time()
p3=ayyy(c2,c3)
p2=ayyy(c1,c2)
p1=ayyy(iv,c1)
end_time=time()
plaintext=p1+p2+p3
print(plaintext)
pp=int(plaintext,16)
print(long_to_bytes(pp))#最后的\n为0x0a，即填充
print("运行时间：{}s".format(end_time-start_time))
