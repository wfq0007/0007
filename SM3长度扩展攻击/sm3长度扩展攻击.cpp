#include <iostream>
#include "sm3.h"
using namespace std;

void printt_u8(u8* input);
//已知消息长度，确定填充，扩展消息与填充，获得合法的伪造的哈希值（内容无意义）

int main()
{
	u8 input[256] = "abc";
	u8 output_t[256];
	unsigned int len = 3;//合法消息长度为3字节。
	SM3(input, len, output_t);//正确哈希值
	cout << "攻击前正确哈希值为：" << endl;
	printt_u8(output_t);
	//敌手获得len与output_t
	//消息分组为521bit(64字节)，哈希值为256bit
	u8 fake[5] = "fake";//添加的伪造消息
	unsigned int llen = 4;
	unsigned int len_f = ((len / 64) + 1) * 64;
	len_f += 4;
	u8 output_f[256];
	//void SM3_length_attack(u8 * op_t, u8 * input, unsigned int len, u8 * output, unsigned int len_pad)
	SM3_length_attack(output_t, fake, llen, output_f, len_f);
	cout << "长度扩展攻击后哈希值为：" << endl;
	printt_u8(output_f);
}

void printt_u8(u8* output) {
	for (int i = 0; i < 32; i++)//16进制输出
	{
		int a = output[i];
		if (a < 16)
			cout << "0x0" << hex << a << " ";
		else
			cout << "0x" << hex << a << " ";
		if ((i + 1) % 8 == 0)
			cout << endl;
	}
	cout << endl;
}