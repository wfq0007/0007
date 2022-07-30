#include <iostream>
#include "sm3.h"
using namespace std;

void printt_u8(u8* input);

unsigned int num_b = 3;

int main()
{
	cout << "此次攻击长度为" << 8 * num_b << "bit" << endl;
	//存储简化的pollard_rho算法。
	u8 input[33] = "a";
	unsigned int len = 32;
	u8 output1[32];
	u8 output2[32];
	SM3(input, 1, output1);
	//cout << "步长为1：";
	//printt_u8(output1);
	SM3(output1, 32, output2);
	//cout << "步长为2：";
	//printt_u8(output2);
	unsigned int num = 0;
	while (1)
	{
		num++;
		//cout << "第" << dec << num << "次" << endl;
		u8 temp1[32];
		u8 temp2[32];
		SM3(output1, 32, temp1);
		for (int i = 0; i < 32; i++) {
			output1[i] = temp1[i];
		}
		//cout << "步长为1：";
		//printt_u8(output1);
		SM3(output2, 32, temp2);
		SM3(temp2, 32, output2);
		//cout << "步长为2：";
		//printt_u8(output2);
		//比较是否相同
		int tp = 0;
		for (int i = 0; i < num_b; i++) {
			if (output1[i] != output2[i]) {
				break;
			}
			tp++;
		}
		if (tp == num_b) {
			cout << "哈希值前" << num_b << "字节相同" << endl;
			cout << "两个输入:" << endl;
			printt_u8(temp1);
			printt_u8(temp2);
			cout << "两个输出:" << endl;
			printt_u8(output1);
			printt_u8(output2);
			cout << "成功";
			exit(0);
		}
		if (num % 65536 == 0) {
			cout << "第" << dec << num << "次" << endl;
		}
	}
	//运算为hash，一个步长为1，一个步长为2。
	/*
	u8 input[256] = "abc";
	//u8 input[256] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";//输入
	u8 output[32];//256杂凑值输出
	unsigned int len = 3;
	SM3(input, len, output);
	cout << "哈希值为：" << endl;
	printt_u8(output);
	*/
	return 0;
}

void printt_u8(u8* output) {
	for (int i = 0; i < 32; i++)//16进制输出
	{
		int a = output[i];
		if (a < 16)
			cout << "0" << hex << a ;
		else
			cout << hex << a ;
	}
	cout << endl;
}
