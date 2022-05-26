#include <iostream>
#include <intrin.h>
using namespace std;

#define u8 unsigned char
#define u32 unsigned long
u32 RK[32] = { 0 };//轮密钥
__m128i indexx = _mm_setr_epi8(3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12);


//一些函数
void enc_sm4(bool pad, int size_p, u8* input, u8* output);//加密
void dec_sm4(int len, u8* input, u8* output);//解密
void rk_gen(u8* key);//轮密钥生成
void u8_32(u8* in, u32* out);//字节转字
void T_key(u8 i, u32 a, u32 b, u32 c, u32 d);//密钥生成的T函数
u32 T_plain(u8 i, u32 a, u32 b, u32 c, u32 d);//轮加密/轮解密的T函数
void printt_u8(int len, u8* input);

//一些固定参数
/******************************定义系统参数FK的取值****************************************/
const u32 FK[4] = {
	0xa3b1bac6,
	0x56aa3350,
	0x677d9197,
	0xb27022dc
};

/******************************定义固定参数CK的取值****************************************/
const u32 CK[32] = {

	0x00070e15,0x1c232a31,0x383f464d,0x545b6269,
	0x70777e85,0x8c939aa1,0xa8afb6bd,0xc4cbd2d9,
	0xe0e7eef5,0xfc030a11,0x181f262d,0x343b4249,
	0x50575e65,0x6c737a81,0x888f969d,0xa4abb2b9,
	0xc0c7ced5,0xdce3eaf1,0xf8ff060d,0x141b2229,
	0x30373e45,0x4c535a61,0x686f767d,0x848b9299,
	0xa0a7aeb5,0xbcc3cad1,0xd8dfe6ed,0xf4fb0209,
	0x10171e25,0x2c333a41,0x484f565d,0x646b7279
};

/******************************SBox参数列表****************************************/
const u8 S_BOX[256] = {

	0xd6,0x90,0xe9,0xfe,0xcc,0xe1,0x3d,0xb7,0x16,0xb6,0x14,0xc2,0x28,0xfb,0x2c,0x05,
	0x2b,0x67,0x9a,0x76,0x2a,0xbe,0x04,0xc3,0xaa,0x44,0x13,0x26,0x49,0x86,0x06,0x99,
	0x9c,0x42,0x50,0xf4,0x91,0xef,0x98,0x7a,0x33,0x54,0x0b,0x43,0xed,0xcf,0xac,0x62,
	0xe4,0xb3,0x1c,0xa9,0xc9,0x08,0xe8,0x95,0x80,0xdf,0x94,0xfa,0x75,0x8f,0x3f,0xa6,
	0x47,0x07,0xa7,0xfc,0xf3,0x73,0x17,0xba,0x83,0x59,0x3c,0x19,0xe6,0x85,0x4f,0xa8,
	0x68,0x6b,0x81,0xb2,0x71,0x64,0xda,0x8b,0xf8,0xeb,0x0f,0x4b,0x70,0x56,0x9d,0x35,
	0x1e,0x24,0x0e,0x5e,0x63,0x58,0xd1,0xa2,0x25,0x22,0x7c,0x3b,0x01,0x21,0x78,0x87,
	0xd4,0x00,0x46,0x57,0x9f,0xd3,0x27,0x52,0x4c,0x36,0x02,0xe7,0xa0,0xc4,0xc8,0x9e,
	0xea,0xbf,0x8a,0xd2,0x40,0xc7,0x38,0xb5,0xa3,0xf7,0xf2,0xce,0xf9,0x61,0x15,0xa1,
	0xe0,0xae,0x5d,0xa4,0x9b,0x34,0x1a,0x55,0xad,0x93,0x32,0x30,0xf5,0x8c,0xb1,0xe3,
	0x1d,0xf6,0xe2,0x2e,0x82,0x66,0xca,0x60,0xc0,0x29,0x23,0xab,0x0d,0x53,0x4e,0x6f,
	0xd5,0xdb,0x37,0x45,0xde,0xfd,0x8e,0x2f,0x03,0xff,0x6a,0x72,0x6d,0x6c,0x5b,0x51,
	0x8d,0x1b,0xaf,0x92,0xbb,0xdd,0xbc,0x7f,0x11,0xd9,0x5c,0x41,0x1f,0x10,0x5a,0xd8,
	0x0a,0xc1,0x31,0x88,0xa5,0xcd,0x7b,0xbd,0x2d,0x74,0xd0,0x12,0xb8,0xe5,0xb4,0xb0,
	0x89,0x69,0x97,0x4a,0x0c,0x96,0x77,0x7e,0x65,0xb9,0xf1,0x09,0xc5,0x6e,0xc6,0x84,
	0x18,0xf0,0x7d,0xec,0x3a,0xdc,0x4d,0x20,0x79,0xee,0x5f,0x3e,0xd7,0xcb,0x39,0x48
};

void u8_32(u8* in, u32* out) {
	/*
	for (u8 i = 0; i < 4; i++) {
		int ii = i << 2;
		u32 temp = ((u32)in[ii] << 24);//循环稍微展开一下
		temp = temp ^ ((u32)in[ii + 1] << 16);
		temp = temp ^ ((u32)in[ii + 2] << 8);
		temp = temp ^ (u32)in[ii + 3];
		out[i] = temp;
	}*/
	__m128i tp = _mm_loadu_epi8(&in[0]);
	tp = _mm_shuffle_epi8(tp, indexx);//指定个顺序避免大端小端
	_mm_storeu_epi32(&out[0], tp);
}
void T_key(u8 i, u32 a, u32 b, u32 c, u32 d) {
	u32 temp;
	temp = a ^ b ^ c ^ CK[i];
	//过函数T
	//32——8,过S盒
	u8 a0, a1, a2, a3;
	a0 = S_BOX[(u8)(temp >> 24)];
	a1 = S_BOX[(u8)(temp >> 16)];
	a2 = S_BOX[(u8)(temp >> 8)];
	a3 = S_BOX[(u8)(temp)];
	u32 B, B13, B23;
	B = (u32)a0 << 24 ^ (u32)a1 << 16 ^ (u32)a2 << 8 ^ (u32)a3;
	B13 = (B << 13) ^ (B >> 19);
	B23 = (B << 23) ^ (B >> 9);
	//RK[i] = B ^ B13 ^ B23 ^ d;
	//流水线优化一下，越早算的越有效果（不过这里面指令太多，谁知道。。。。。）
	RK[i] = d ^ B ^ B13 ^ B23;
}
void rk_gen(u8* key) {
	u8 i;
	u32 K[4] = { 0 };
	u8_32(key, K);//密钥由字节转为字
	u32 K0, K1, K2, K3;//循环展开外加使用变量不是数组
	K0 = K[0] ^ FK[0];
	K1 = K[1] ^ FK[1];
	K2 = K[2] ^ FK[2];
	K3 = K[3] ^ FK[3];
	T_key(0, K1, K2, K3, K0);
	T_key(1, K2, K3, RK[0], K1);
	T_key(2, K3, RK[0], RK[1], K2);
	T_key(3, RK[0], RK[1], RK[2], K3);
	for (i = 4; i < 32; i++) {
		T_key(i, RK[i - 3], RK[i - 2], RK[i - 1], RK[i - 4]);
	}
}
u32 T_plain(u8 i, u32 a, u32 b, u32 c, u32 d) {
	u32 temp;
	temp = a ^ b ^ c ^ RK[i];
	//过函数T
	//32——8,过S盒
	u8 a0, a1, a2, a3;
	a0 = S_BOX[(u8)(temp >> 24)];
	a1 = S_BOX[(u8)(temp >> 16)];
	a2 = S_BOX[(u8)(temp >> 8)];
	a3 = S_BOX[(u8)(temp)];
	u32 B, B2, B10, B18, B24, C;
	B = (u32)a0 << 24 ^ (u32)a1 << 16 ^ (u32)a2 << 8 ^ (u32)a3;
	B2 = (B << 2) ^ (B >> 30);
	B10 = (B << 10) ^ (B >> 22);
	B18 = (B << 18) ^ (B >> 14);
	B24 = (B << 24) ^ (B >> 8);
	//C = B ^ B2 ^ B10 ^ B18 ^ B24 ^ d;
	C = d ^ B ^ B2 ^ B10 ^ B18 ^ B24;
	return C;
}
void enc_sm4(bool pad, int size_p, u8* input, u8* output) {
	//要实现任意长度的明文加密
	//int len = size_p / 16;
	int len = size_p >> 4;//整除也变成右移
	//轮加密
	for (int num = 0; num < len; num++)//对不用补丁的组
	{
		int tp_num16 = num << 4;
		u32 P[4] = { 0 };
		u8_32((input + tp_num16), P);//明文由字节转为字
		//中间结果放在临时变量中
		u32 X1, X2, X3, X4;
		X1 = P[0];
		X2 = P[1];
		X3 = P[2];
		X4 = P[3];
		u32 temp;
		for (u8 i = 0; i < 32; i++) {
			temp = T_plain(i, X2, X3, X4, X1);
			X1 = X2;
			X2 = X3;
			X3 = X4;
			X4 = temp;
		}
		//最后一轮反序变换
		//合成，并变成u8
		//用到了一点点循环展开？
		for (u8 i = 0; i < 4; i++) {
			u8 j = 24 - (i << 3);
			u8 tpp = tp_num16 + i;
			output[tpp] = (u8)(X4 >> j);
			output[tpp + 4] = (u8)(X3 >> j);
			output[tpp + 8] = (u8)(X2 >> j);
			output[tpp + 12] = (u8)(X1 >> j);
		}
	}
	if (pad)//最后一组
	{
		//乘法应该会自动编译成移位吧？，要不手动改？
		int tp_len16 = len << 4;//len*16
		int n = size_p - tp_len16;
		u8 plt[16] = { 0 };
		for (int i = 0; i < n; i++) {
			plt[i] = input[tp_len16 + i];
		}
		//加密
		u32 P[4] = { 0 };
		u8_32(plt, P);//明文由字节转为字
		u32 X1, X2, X3, X4;
		X1 = P[0];
		X2 = P[1];
		X3 = P[2];
		X4 = P[3];
		u32 temp;
		for (u8 i = 0; i < 32; i++) {
			temp = T_plain(i, X2, X3, X4, X1);
			X1 = X2;
			X2 = X3;
			X3 = X4;
			X4 = temp;
		}
		//最后一轮反序变换
		//合成，并变成u8
		for (u8 i = 0; i < 4; i++) {
			u8 j = 24 - (i << 3);
			u8 tpp = tp_len16 + i;
			output[tpp] = (u8)(X4 >> j);
			output[tpp + 4] = (u8)(X3 >> j);
			output[tpp + 8] = (u8)(X2 >> j);
			output[tpp + 12] = (u8)(X1 >> j);
		}
	}
}
void dec_sm4(int len, u8* input, u8* output) {
	//要实现任意长度的密文解密
	//轮解密
	for (int num = 0; num < len; num++)
	{
		int tp_num16 = num << 4;
		u32 P[4] = { 0 };
		u8_32((input + tp_num16), P);//密文由字节转为字
		u32 X1, X2, X3, X4;
		X1 = P[0];
		X2 = P[1];
		X3 = P[2];
		X4 = P[3];
		u32 temp;
		for (u8 i = 0; i < 32; i++) {
			temp = T_plain(31 - i, X2, X3, X4, X1);
			X1 = X2;
			X2 = X3;
			X3 = X4;
			X4 = temp;
		}
		//最后一轮反序变换
		//合成，并变成u8
		for (u8 i = 0; i < 4; i++) {
			u8 j = 24 - (i << 3);
			u8 tpp = tp_num16 + i;
			output[tpp] = (u8)(X4 >> j);
			output[tpp + 4] = (u8)(X3 >> j);
			output[tpp + 8] = (u8)(X2 >> j);
			output[tpp + 12] = (u8)(X1 >> j);
		}
	}
}
void printt_u8(int len, u8* input) {
	for (int i = 0; i < len; i++)//16进制输出
	{
		int a = input[i];
		if (a < 16)
			cout << "0x0" << hex << a << " ";
		else
			cout << "0x" << hex << a << " ";
		if ((i + 1) % 8 == 0)
			cout << endl;
	}
	cout << endl;
}