#include <iostream>
#include "sm3.h"
using namespace std;

void printt_u8(u8* input);

int main()
{
	u8 input[256] = "abc";
	//u8 input[256] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";//输入
	u8 output[32];//256杂凑值输出
	unsigned int len = 3;
	SM3(input, len, output);
	cout << "哈希值为：" << endl;
	printt_u8(output);
	return 0;
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