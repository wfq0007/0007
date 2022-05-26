#include <iostream>
#include <Windows.h>
#include <thread>
#include <intrin.h>
#include "sm4.h"

using namespace std;
#define size_p 1600000
const unsigned int size_buffer = 1600000;
const u8 thread_num = 8;
//流水线优化一是减少分支的可能
//而是先算后算
//总之是尽可能避免阻塞

u8 key[16] = {
		0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,
		0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10
};

u8 encode_buffer[size_buffer] = { 0 };//加密结果缓冲区
u8 decode_buffer[size_buffer] = { 0 };//解密结果缓冲区

void jjm_thread(int thread_num)
{
	LARGE_INTEGER t1, t2, tc;
	double time;
	QueryPerformanceFrequency(&tc);

	//初始化明文
	u8* plaintext;
	plaintext = (u8*)malloc(size_p);


	/*---------------------------优化-----------------------------------*/

	cout << thread_num << " 线程：" << endl;

	//生成密钥
	QueryPerformanceCounter(&t1);
	rk_gen(key);
	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "生成轮密钥时间：" << time << "ms" << endl;


	//加密
	//为了实现任意长度的加密
	bool a = (size_p % 16) ? 1 : 0;
	int len = (size_p >> 4) + a;//要分几块128bit加密,pad额外算
	int len_n = len / thread_num;//每个线程承担几组加解密
	int size_n = len_n << 4;
	//多线程加密
	QueryPerformanceCounter(&t1);
	thread* th = new thread[thread_num];
	for (int i = 0; i < thread_num - 1; i++) {
		int offset1 = i * size_n;
		th[i] = thread(enc_sm4, 0, size_n, plaintext + offset1, encode_buffer + offset1);
	}
	int offset2 = (thread_num - 1) * size_n;
	int size_np = size_p - offset2;
	th[thread_num - 1] = thread(enc_sm4, a, size_np, plaintext + offset2, encode_buffer + offset2);
	for (int i = 0; i < thread_num; i++) {
		th[i].join();
	}
	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "SM4加密 " << len << " 次运行时间:" << time << "ms" << endl;
	if (thread_num == 1) {
		cout << "延迟时间：" << (double)time / (double)len << "ms" << endl;
	}
	cout << "吞吐量（单位时间（s）加密的字节数）：" << (double)len / (double)time * 16 * 1000 << endl;


	//多线程解密
	QueryPerformanceCounter(&t1);
	thread* th1 = new thread[thread_num];
	for (int i = 0; i < thread_num - 1; i++) {
		int offset3 = i * size_n;
		th1[i] = thread(dec_sm4, len_n, encode_buffer + offset3, decode_buffer + offset3);
	}
	int offset4 = (thread_num - 1) * size_n;
	int len_np = len - (thread_num - 1) * len_n;
	th1[thread_num - 1] = thread(dec_sm4, len_np, encode_buffer + offset4, decode_buffer + offset4);
	for (int i = 0; i < thread_num; i++) {
		th1[i].join();
	}
	QueryPerformanceCounter(&t2);
	//dec_sm4(len, encode_buffer, decode_buffer);
	//cout << "解密结果为：" << endl;
	//printt_u8(size_p, decode_buffer);//解密结果输出去掉补充的“0”

	QueryPerformanceCounter(&t2);
	time = 1000 * ((double)(t2.QuadPart - t1.QuadPart) / (double)tc.QuadPart);
	cout << "SM4解密 "  << len << " 次运行时间:" << time << "ms" << endl;
	if (thread_num == 1) {
		cout << "延迟时间：" << (double)time / (double)len << "ms" << endl;
	}
	cout << "吞吐量（单位时间（s）解密的字节数）：" << (double)len / (double)time * 16 * 1000 << endl;
	cout << endl;
}
int main()
{
	cout << "优化后代码：" << endl;

	jjm_thread(1);
	jjm_thread(2);
	//jjm_thread(3);
	jjm_thread(4);
	//jjm_thread(5);
	//jjm_thread(6);
	//jjm_thread(7);
	jjm_thread(8);
	//jjm_thread(9);
	//jjm_thread(10);
	//jjm_thread(11);
	//jjm_thread(12);
	//jjm_thread(13);
	//jjm_thread(14);
	//jjm_thread(15);
	//jjm_thread(16);
	return 0;
}