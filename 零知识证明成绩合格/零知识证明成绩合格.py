#零知识证明成绩合格，交互式
#利用哈希抗原像特性，基于可信第三方进行操作
#流程：
#MOE（官方考试机构）已知成绩，
#计算commit_first=sha256(cn_id,grade,year,sig_by_moe,r)，发给证明方
#其中cn_id为用户id，grade为成绩，year为年份，sig_by_moe为可信第三方MOE的签名，r为随机数
#hash(grade)次,获得commit_end=H()，发给验证方
#假设成绩为450，证明方自己对commit_first做450-425，即25次hash后将结果发给验证方
#验证方收到结果后做425次hash，验证是否与commit_end相等。
#整个交互流程中的身份验证不是本文重点，暂不关注。
#本代码仅演示思想与流程，不关注对三方设立客户端服务端交互。
import hashlib
import random
import string

def hash_many_times(hash_value,times):
    commit=hash_value
    for i in range(times):
        #256bit哈希值在数上随机，按ASCII码翻译成32字节字符串
        #将上一轮的16进制哈希值改为字符串，ascii码翻译
        mm=''
        for j in range(32):
            mm+=chr(int(commit[j*2:(j+1)*2],16))
        commit=getattr(hashlib,'sha256')(mm.encode()).hexdigest()
    return commit

#初始化
cn_id='202000460007'
grade='300'
year='2022'
print("成绩为{}分".format(grade))

def random_string_generate(size,allowed_chars):
    return ''.join(random.choice(allowed_chars)for x in range(size))

allowed_chars=string.ascii_letters+string.punctuation

#不关注交互与身份验证，任意赋值演示零知识证明流程
#这两处均赋随机字符串
sig_by_moe=random_string_generate(50,allowed_chars)
r=random_string_generate(50,allowed_chars)
message=cn_id+grade+year+sig_by_moe+r
print("message: ",message)

#MOE计算commit_first，发给证明方
commit_first=getattr(hashlib,'sha256')(message.encode()).hexdigest()
print("commit_first: ",commit_first)

#MOE计算commit_last,发给验证方
#对commit_first进行(grade+1)次hash
commit_last=hash_many_times(commit_first,int(grade))
print("commit_last: ",commit_last)

#证明方知道成绩，对commit_first进行(grade-425)次hash，发给验证方
resp=hash_many_times(commit_first,int(grade)-425)
print("resp: ",resp)

#验证方对收到的resp进行425次哈希，若与commit_last一致，则证明成绩合格
result=hash_many_times(resp,425)
if(result==commit_last):
    print("证明通过，成绩合格")
else:
    print("证明不通过，成绩不合格")


#证明方伪造成功概率基于hash抗原像特性
#理论上对一个消息hash300次的摘要是无法获得425次前的原像的

        
    



