//KMP�㷨
//abcddabcababcdaabcababcdaabcabaa
//abcdaabcac
#include <iostream>
using namespace std;

int* find_next(string p);//����ģʽ����next
int KMP(string t, string p, int* n);//ƥ��


int* find_next(string p)
{
	int a = p.length();//ģʽ������
	if (a <= 0)
		exit(0);//ģʽ����Ϊ�մ�
	int* next = (int*)malloc(sizeof(int) * a);
	if (!next)
		exit(0);//�ж��ڴ��Ƿ����ɹ�
	unsigned int j = 0;
	int k = -1;
	next[0] = -1;//��ʼ��next[0]=-1
	while (j < a)
	{
		while (k >= 0 && p[j] != p[k])
			k = next[k];
		j++;
		k++;
		if (j == a)break;//����
		if (p[j] == p[k])
			next[j] = next[k];//����,�Ż�
		else
			next[j] = k;
	}
	return next;//����next
}
int KMP(string t, string p, int* n)//ƥ��
{
	int tlen = t.length();
	int plen = p.length();
	if (tlen < plen)
		return -1;
	int i = 0;
	int j = 0;
	while (i < tlen && j < plen)//δ���ַ���β
	{
		if (j == -1 || t[i] == p[j])
		{
			j++;
			i++;
		}
		else//��ƥ���ƶ�ģʽ��
			j = n[j];//nextָ��
	}
	if (j >= plen)
		return (i - plen);//������Ԫ��λ��
	else
		return -1;
}