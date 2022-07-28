#Merkle tree实现
#基于sm3
from gmssl import sm3,func
import random
import string
import math
import time

def create(record_list):
    #层级hash节点也要存储
    table=[]
    lst=[]
    for i in record_list:#i的格式为字符串
        temp=sm3.sm3_hash(func.bytes_to_list(i.encode()))
        lst.append(temp)
    table.append(lst[:])
    #print(lst)
    #print("叶子节点建立完毕")
    if len(lst)<=1:
        print("no tracnsactions to be hashed")
        return False
    height=1#高度
    while len(lst)>1:
        height+=1
        if len(lst)%2==0:#偶数个节点
            lstt=[]
            while len(lst)>1:
                a=lst.pop(0)
                b=lst.pop(0)#逐个取出
                temp=sm3.sm3_hash(func.bytes_to_list((a+b).encode()))
                lstt.append(temp)#往上一层
            lst=lstt#更新lst
            #print("第{}层:".format(height))
            #print(lst)
        else:#奇数个点，复制最后一个，凑成偶数个
            lstt=[]
            lst.append(lst[-1])
            while len(lst)>1:
                a=lst.pop(0)
                b=lst.pop(0)#逐个取出
                temp=sm3.sm3_hash(func.bytes_to_list((a+b).encode()))
                lstt.append(temp)#往上一层
            lst=lstt
            #print("第{}层:".format(height))
            #print(lst)
        table.append(lst[:])
    return lst,height,table
                
            
            

record_list=['a','b','wang','dd','dddd','w','aa','n','ddd','e','ee','qq','wfag','aaa','bb']
listt,height,table=create(record_list)
print("proof:",listt)
#print("所有层级哈希值:",table)
print("height:",height)

'''
#十万叶子节点,计时
def random_string_generate(size,allowed_chars):
    return ''.join(random.choice(allowed_chars)for x in range(size))

allowed_chars=string.ascii_letters+string.punctuation

record_list=[]
num=100000
for i in range(num):
    record_list.append(random_string_generate(5,allowed_chars))
print("ok")
t_start=time.time()
listt,height,table=create(record_list)
t_end=time.time()
print("height:",height)
print("创建{}叶子节点的merkle tree所需时间为{}s".format(num,t_end-t_start))
'''


#节点包含证明
def include_proof(tx,pos,height,table):
    lls=[]
    for i in range(height):
        lls+=[pos]
        pos=pos//2
    #相邻位置列表
    ls=[]
    for i in lls[:-1]:
        if i%2==0:
            ls.append(i+1)
        else:
            ls.append(i-1)
    ls.append(0)#添加proof
    T_list=[]
    for i in range(height):
        if(ls[i]>=len(table[i])):##若越界，则是填充重复的
            T_list.append(table[i][-1])
        else:
            T_list.append(table[i][ls[i]])
    a=tx
    #a=sm3.sm3_hash(func.bytes_to_list(tx.encode()))
    for i in range(height-1):
        b=T_list[i]
        if lls[i]%2==0:
            a=sm3.sm3_hash(func.bytes_to_list((a+b).encode()))
        else:
            a=sm3.sm3_hash(func.bytes_to_list((b+a).encode()))
    if a!=T_list[-1]:
        return False
    return True
        
                    
tx='bb'
print(tx)
pos=record_list.index(tx)
tx=sm3.sm3_hash(func.bytes_to_list(tx.encode()))
print(tx,pos)
if_exist=include_proof(tx,pos,height,table)
if if_exist==True:
    print("该节点存在")
else:
    print("该节点不存在")

    


'''
#节点不包含证明，有序初始记录
#通过证明其两端相邻即可
#ID即为我们的初始顺序0，1，2，，
def exclude_proof(pos1,pos2,table):
    try:
        #问题是，既然有3.5存在的可能，也就是pos1,pos2不代表索引，那就不能根据//2找上一个
        #或直接判断父节点是否相同，应该都尝试
        #if(pos1%2==0):#父节点相同，一个hash变成上一层的存在性证明
        temp=sm3.sm3_hash(func.bytes_to_list((table[0][pos1]+table[0][pos2]).encode()))
        try:
            pos=table[1].index(temp)
            if_exist=include_proof(temp,pos,height-1,table[1:])
            return if_exist
        except:
            #print("父节点不相同")
            #else:
            #两端节点父节点不相同,
            #那么直到两个节点汇总到一起，hash位置均处于右左，即分别找前一个和后一个hash
            for i in range(height-1):
                a=table[i][pos1-1]
                b=table[i][pos1]
                c=table[i][pos2]
                d=table[i][pos2+1]
                h1=sm3.sm3_hash(func.bytes_to_list((a+b).encode()))
                h2=sm3.sm3_hash(func.bytes_to_list((c+d).encode()))
                #print(h1,h2)
                #尝试hash(h1+h2)，看看汇总是否存在
                temp=sm3.sm3_hash(func.bytes_to_list((h1+h2).encode()))
                #print(temp)
                for j in range(len(table[i+1])):
                    if_exist=include_proof(temp,j,height-2-i,table[2+i:])
                    if if_exist==True:
                        return True
                #不相连的话，再次尝试下一轮
                pos1=table[i+1].index(h1)
                pos2=table[i+1].index(h2)
    except:
        return False
    
    




pos1=5
pos2=6
print(pos1,pos2)
if_note=exclude_proof(pos1,pos2,table)
if if_note==True:
    print("两端节点相邻，该节点不存在")
else:
    print("该节点存在")

'''


