#include <iostream>
#include <Windows.h>
#include "sm4.h"

using namespace std;
#define size_p 16000000
const int size_buffer = 16000000;

u8 key[16] = {
		0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,
		0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10
};

u8 encode_buffer[size_buffer] = { 0 };//加密结果
u8 decode_buffer[size_buffer] = { 0 };//解密结果

int main()
{
	LARGE_INTEGER t1, t2, tc;
	double time;
	QueryPerformanceFrequency(&tc);

	//初始化明文
	u8* plaintext;
	plaintext = (u8*)malloc(size_p);

	/*---------------------------原始-----------------------------------*/

	cout << "原始代码：" << endl;

	//生成密钥
	QueryPerformanceCounter(&t1);
	rk_gen(key);
	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "生成轮密钥时间：" << time << "ms" << endl;


	//加密
	//为了实现任意长度的加密
	bool a = (size_p % 16) ? 1 : 0;
	int len = size_p / 16 + a;//要分几块128bit加密,pad额外算
	QueryPerformanceCounter(&t1);
	enc_sm4(a, size_p, plaintext, encode_buffer);
	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "SM4加密" << len << "次运行时间:" << time << "ms" << endl;
	cout << "延迟时间：" << (double)time / (double)len << "ms" << endl;
	cout << "吞吐量（单位时间（s）加密的字节数）：" << (double)len / (double)time * 16 * 1000 << endl;
	//cout << "加密结果为：" << endl;//输出好占时间
	//printt_u8(16 * len, encode_buffer);//加密结果输出包含“补丁”


	//解密
	QueryPerformanceCounter(&t1);
	dec_sm4(len, encode_buffer, decode_buffer);
	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "SM4解密" << len << "次运行时间:" << time << "ms" << endl;
	cout << "延迟时间：" << (double)time / (double)len << "ms" << endl;
	cout << "吞吐量（单位时间（s）解密的字节数）：" << (double)len / (double)time * 16 * 1000 << endl;
	//cout << "解密结果为：" << endl;
	//printt_u8(size_p, decode_buffer);//解密结果输出去掉补充的“0”


	return 0;
}