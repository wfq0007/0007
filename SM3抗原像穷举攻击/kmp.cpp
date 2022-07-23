//KMP算法
//abcddabcababcdaabcababcdaabcabaa
//abcdaabcac
#include <iostream>
using namespace std;

int* find_next(string p);//计算模式串的next
int KMP(string t, string p, int* n);//匹配


int* find_next(string p)
{
	int a = p.length();//模式串长度
	if (a <= 0)
		exit(0);//模式串不为空串
	int* next = (int*)malloc(sizeof(int) * a);
	if (!next)
		exit(0);//判断内存是否分配成功
	unsigned int j = 0;
	int k = -1;
	next[0] = -1;//初始化next[0]=-1
	while (j < a)
	{
		while (k >= 0 && p[j] != p[k])
			k = next[k];
		j++;
		k++;
		if (j == a)break;//跳出
		if (p[j] == p[k])
			next[j] = next[k];//递推,优化
		else
			next[j] = k;
	}
	return next;//返回next
}
int KMP(string t, string p, int* n)//匹配
{
	int tlen = t.length();
	int plen = p.length();
	if (tlen < plen)
		return -1;
	int i = 0;
	int j = 0;
	while (i < tlen && j < plen)//未到字符串尾
	{
		if (j == -1 || t[i] == p[j])
		{
			j++;
			i++;
		}
		else//不匹配移动模式串
			j = n[j];//next指针
	}
	if (j >= plen)
		return (i - plen);//返回首元素位置
	else
		return -1;
}