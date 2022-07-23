#include <iostream>
#include <string>
#include "sm3.h"
using namespace std;

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

int main()
{
	u8 iin[25] = "Fangqi Wang 202000460007";
	u8 output[32];//256杂凑值输出
	//u8 input[256] = "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd";//输入
	//修改输入，以64字节长为基准
	//输入数据串的长度由24开始依次尝试
	SM3(iin, 24, output);
	if (pp(output) != -1)
	{
		cout << "找到了" << endl;
		printt_u8(output);
		exit(0);
	}
	unsigned int len = 25;
	while (1)
	{
		u8 input[256];//先限制在256内
		for (int xx = 0; xx < len - 24; xx++)
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
			//cout << xx << "次" << endl;
			//printt_u8(input);
			for (int i = 0; i < xx; i++) {
				for (int j = 0; j < 0xff; j++)
				{
					SM3(input, len, output);
					if (pp(output) != -1)
					{
						cout << "找到了" << endl;
						printt_u8(output);
						exit(0);
					}
					input[i]++;
				}
				//cout << i << "  又完成了256次" << endl;
			}
			for (int i = xx + 24; i < len; i++) {
				for (int j = 0; j < 0xff; j++)
				{
					SM3(input, len, output);
					if (pp(output) != -1)
					{
						cout << "找到了" << endl;
						printt_u8(output);
						exit(0);
					}
					input[i]++;
				}
				//cout << i << "  又完成了256次" << endl;
			}
		}
		cout << "此时长度为:" << len << endl;
		len++;
	}
	return 0;
}

void printt_u8(u8* output) {
	for (int i = 0; i < 64; i++)//16进制输出
	{
		int a = output[i];
		if (a < 16)
			cout << "0" << hex << a;
		else
			cout << hex << a;
	}
	cout << endl;
}