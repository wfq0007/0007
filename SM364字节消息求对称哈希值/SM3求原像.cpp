#include <iostream>
#include "sm3.h"
using namespace std;

void printt_u8(u8* input);
u8 input[65];
u8 output[33];


bool find(u8* a)
{
	for (int i = 0; i < 32; i++) {
		if (a[i] != a[63 - i]) {
			return 0;
		}
	}
	return 1;
}

void search(int pos)
{
	if (pos < 63) {
		for (int i = 0; i <= 0xff; i++)
		{
			search(pos + 1);
		}
	}
	if (pos == 63) 
	{
		for (int i = 0; i <= 0xff; i++) {
			//printt_u8(input);
			SM3(input, 64, output);
			if (find(output))
			{
				cout << "找到了" << endl;
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
			if (input[pos - tt] != 0xff) {
				input[pos - tt]++;
				ss = true;
			}
		}
	}
}

int main()
{
	for (int i = 0; i < 64; i++) {
		input[i] = 0x00;
	}
	search(0);
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