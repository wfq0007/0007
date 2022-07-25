#include <iostream>
#include <cmath>
#include "sm3.h"
using namespace std;

int n_length = 2;
//固定消息长度为32字节
//生日攻击，选择位数，半个存储，半个穷举查

unsigned int postion_it = 0;
unsigned int postion_ot = 0;
unsigned int num_ot = pow(2, n_length * 8) * 32;
char* table = new char[num_ot];//哈希值为32字节长
unsigned int num_it = pow(2, n_length * 8) * (n_length + 1);
char* inputtb = new char[num_it];//输入值表，位置一一对应
void printt_u8(u8* input);
unsigned int find(u8* a);
void search(int pos);
void setup(int pos);
u8 input[33];
u8 output[33];

int main()
{
	cout << num_ot << endl;
	cout << num_it << endl;
	//选择查找位数(字节为单位）
	cout << "此次生日攻击长度为" << 256 * n_length << "bit" << endl;
	//为了操作方便，这里的一半一半手动设置固定消息长度最后一比特依次为0和1
    //一半建表
	for (int i = 0; i < 31 - n_length; i++){
		input[i] = 0x66;
	}
	input[31 - n_length] = 0b00101100;
	for (int i = 32 - n_length; i < 32; i++) {
		input[i] = 0x00;
	}
	printt_u8(input);
	setup(32 - n_length);
	cout << "建表完毕" << endl;

	//一半查找
	//setup内最后给前一位进1了
	printt_u8(input);
	search(32 - n_length);
	return 0;
}
void printt_u8(u8* tt) {
	for (int i = 0; i < 32; i++)//16进制输出
	{
		int a = tt[i];
		if (a < 16)
			cout << "0" << hex << a;
		else
			cout << hex << a;
	}
	cout << endl;
}
void setup(int pos)
{
	if (pos < 31) {
		for (int i = 0; i <= 0xff; i++)
		{
			setup(pos + 1);
		}
	}
	if (pos == 31)
	{
		for (int i = 0; i <= 0xff; i++) {
			//printt_u8(input);
			SM3(input, 32, output);
			//执行完output后存入大table中
			//存入位置？
			//其实input可以只存不固定的
			for (int i = 0; i < 32; i++) {
				table[postion_ot + i] = output[i];
			}
			for (int i = 31 - n_length; i < 32; i++) {
				inputtb[postion_it + i] = input[i];
			}
			postion_ot += 32;
			postion_it += (n_length + 1);
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
void search(int pos)
{
	if (pos < 31) {
		for (int i = 0; i <= 0xff; i++)
		{
			search(pos + 1);
		}
	}
	if (pos == 31)
	{
		for (int i = 0; i <= 0xff; i++) {
			printt_u8(input);
			SM3(input, 32, output);
			//查表
			unsigned int temp = find(output);
			if (temp!=-1)
			{
				cout << "找到了" << endl;
				cout << "第一个输入值：";
				for (int i = 0; i < 32; i++) {
					int hhh = inputtb[temp + i];
					if (hhh < 16) {
						cout << "0";
					}
					cout << hhh;
				}
				unsigned int temp2 = (temp / 32) * (n_length + 1);
				for (int i = 31-n_length; i < 32; i++){
					int hhh = inputtb[temp2 + i];
					if (hhh < 16) {
						cout << "0";
					}
					cout << hhh;
				}
				cout << endl;
				cout << "第二个输入值：";
				printt_u8(input);
				printt_u8(output);
				//return;
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
unsigned int find(u8* a)//查表
{
	unsigned int tp;
	for (unsigned int i = 0; i < postion_ot; i += 32)
	{
		tp = 0;
		for (int j = 0; j < 32; j++)
		{
			if (a[j] != table[i + j]) {
				break;
			}
			else {
				tp++;
				if (tp == 32) {
					return i;//返回位置。
				}
			}
		}
	}
	return -1;
}