#include <iostream>
#include <NTL/ZZ.h>
#include <ctime>
using namespace std;
using namespace NTL;
//现在的问题是有可能遍历所有值都找不到，毕竟环长远小于n
//这大概是这个问题的缺陷？
//看了资料，说是循环期望为根号n，我检测了几个小的，的确如此
//另外好像是检测不出来因子2，要额外判断(我还没试图证明过
int sxjc(ZZ n)//简单Fermat小定理检测素性
{
	srand(time(0));
	ZZ a = to_ZZ(rand()) % n;//产生随机数
	a = PowerMod(a, n - 1, n);
	//cout << "是否为素数"<<"n=" << n << "：" << a<<endl;
	if (a == 1)
		return 1;
	else
		return 0;
}
ZZ f(ZZ x,ZZ n)//递推表达式
{
	//cout << ((x * x + 1) % n) << endl;
	return (x * x + 1) % n;
}
//n为模(也是待分解整数)，ori为起点处的值，len为循环节长度，id为循环节起始处坐标，val为循环节起始处的值
bool FloydCycle(ZZ n,ZZ ori, ZZ& val)//有环返回true，无环返回false,此实验必有环
{
	ZZ slow, fast;//慢指针和快指针
	slow = f(ori,n);//快指针的移动速度是慢指针的2倍
	fast = f(ori, n);
	fast = f(fast, n);
	while (slow != fast )//直到相遇
	{
		//快指针的移动速度是慢指针的2倍
		//cout << "slow:";
		slow = f(slow,n);
		fast = f(fast, n);
		//cout << "fast:";
		fast = f(fast, n);
	}
	if (slow != fast) return false;//无环
    val = slow;
	cout << "环头"<< val << endl;
	return true;
}
void js(ZZ n)
{
	if (sxjc(n) == 1) {//递归终止条件
		cout << "质因子" << n << endl;
		return;
	}
	srand(time(0));
	ZZ a0 = to_ZZ(rand()) % n;
	ZZ a1 = (a0 * a0 + 1) % n;//初始化
	while (a0 == 1 || a0 == 0 || a0 == a1)//调试时发现会出错的情况
	{
		a0 = to_ZZ(rand()) % n;//产生随机数//不能为1/0，否则第一/二次a0-a1=1
	}
	ZZ w = GCD(a0 - a1, n);
	cout << "初始两值"<< a0 << " " << a1 << endl;
	//先看什么值时候出现环
	//应该也能边递推边找出环起始处吗？？
	ZZ val= to_ZZ(1);//val为循环初始值
	FloydCycle(n, a0 ,val);
	while (w == 1 && a1 != val)//递推至环开始
	{
		a0 = a1;
		a1 = (a0 * a0 + 1) % n;
		w = GCD(a0 - a1, n);
		//cout << " " << a1 << " " << w << endl;
	}
	a0 = a1;
	a1 = (a0 * a0 + 1) % n;
	w = GCD(a0 - a1, n);
	//cout << " " << a1 << " " << w << endl;
	while (w == 1 && a1 != val)//递推至第二次环开始
	{
		a0 = a1;
		a1 = (a0 * a0 + 1) % n;
		//cout << " " << a1 << " " << w << endl;
		w = GCD(a0 - a1, n);
	}
	//问题出在遍历所有可能值仍未找到质因子，又会死循环，如何结束
	if (w == 1)
	{
		cout << "遍历所有均未找到" << endl;
		//结束函数
		exit(0);
	}
	js(w);//递归
	n = n / w;//更新n
	cout << "新的n:" << n << endl;
	js(n);//递归
}
int main()
{
	//此算法不是从小到大检测素因子
	ZZ n;
	cout << "请输入待分解的整数n:";
	cin >> n;
	int i = 0;//表示因子中有几个2
	while (n % 2 == 0)
	{
		n = n / 2;
		i++;
	}
	if (i > 0)
	{
		cout << "质因子" << i << "个" << 2 << endl;
	}
	//cout << n << endl;
	js(n);
	return 0;
}