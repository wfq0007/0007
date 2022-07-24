#include <iostream>
#include <string>
#include "sm3.h"
using namespace std;


u8 input[256];//先限制在256内
unsigned int len = 25;
u8 output[32];//256杂凑值输出

void printt_u8(u8* input);
int* find_next(string p);//计算模式串的next
int KMP(string t, string p, int* n);//匹配

int pp(u8* output) {
	//匹配字符串
	string outt = "sdu_cst_20220610";
	string s = "00000000000000000000000000000000";
	for (int i = 0; i < 32; i++) {
		s[i] = *(output + i);
	}
	//计算next
	int* next = new int[16];//创建next数组
	next = find_next(outt);//调用函数计算模式串的next
	//kmp模式匹配
	int n = KMP(s, outt, next);
	return n;
	//不存在返回-1
}

void search(int pos, int e1, int s2)
{
	if (pos == 0) {
		if (pos == e1) {
			search(pos + 24, e1, s2);
		}
		else {
			search(pos + 1, e1, s2);
		}
	}
	else if (pos < (len - 1))
	{
		for (int i = 0; i < 0xff; i++) {
			//printt_u8(input);
			if (pos == e1) {
				search(pos + 24, e1, s2);
			}
			else {
				search(pos + 1, e1, s2);
			}
		}
	}
	if (pos == len - 1)
	{
		for (int j = 0; j <= 0xff; j++)
		{
			SM3(input, len, output);
			if (pp(output) != -1)
			{
				std::cout << "找到了" << endl;
				printt_u8(output);
				exit(0);
			}
			input[pos]++;
		}
		bool ss = false;
		int tt = 0;
		while (!ss)
		{
			input[pos - tt] = 0x00;
			tt++;
			if ((pos - tt) == (s2 - 1)){
				tt += 24;
			}
			if (tt == len) {
				ss = true;
			}
			else if (input[pos - tt] != 0xff) {
				input[pos - tt]++;
				ss = true;
			}
			//printt_u8(input);
		}
	}
}
int main()
{
	u8 iin[25] = "Fangqi Wang 202000460007";
	//u8 input[256] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";//输入
	//修改输入，以64字节长为基准
	//输入数据串的长度由24开始依次尝试
	SM3(iin, 24, output);
	if (pp(output) != -1)
	{
		std::cout << "找到了" << endl;
		printt_u8(output);
		exit(0);
	}
	while (1)
	{
		for (int xx = 0; xx < (len - 24); xx++)
		{
			int w = 0;
			for (int i = xx; i < xx + 24; i++) {
				input[i] = iin[w];
				w += 1;
			}
			for (int i = 0; i < xx; i++) {
				input[i] = 0x00;
			}
			for (int i = xx + 24; i < len; i++) {
				input[i] = 0x00;
			}
			search(0, xx, xx + 24);
			/*
			if (xx != 0) {
				search(0, 0, xx);
			}
			if ((xx + 24) != len) {
				search(xx + 24, xx + 24, len);
			}*/
		}
		std::cout << "此时长度为:" << len << endl;
		len++;
	}
	return 0;
}

void printt_u8(u8* output) {
	for (int i = 0; i < 64; i++)//16进制输出
	{
		int a = output[i];
		if (a < 16)
			std::cout << "0" << hex << a;
		else
			std::cout << hex << a;
	}
	std::cout << endl;
}
