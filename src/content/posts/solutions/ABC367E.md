---
title: ABC367 E - Permute K times 题解
published: 2024-08-18
description: First E Accepted; Binary Lifting Classic Problem.
tags: [OI]
category: Notes
draft: false
---

[Atcoder Beginner Contest 367 E - Permute K times](https://atcoder.jp/contests/abc367/tasks/abc367_e)

[AC Record](https://atcoder.jp/contests/abc367/submissions/56848064)

# 题目翻译

### 问题陈述
给定一个长度为 $N$ 的序列 $X$ ，其中每个元素介于 $1$ 和 $N$ 之间（含两个元素），以及一个长度为 $N$ 的序列 $A$ 。

打印对 $A$ 执行以下操作 $K$ 次的结果。

- 将 $A$ 替换为 $B$ ，使得 $B_i = A_{X_i}$ 。
### 数据范围

- 所有输入值均为整数。
- $1 \le N \le 2 \times 10^5$
- $0 \le K \le 10^{18}$
- $1 \le X _ i \le N$
- $1 \le A _ i \le 2 \times 10^5$
# 解题思路

对于这类进行**单一重复操作**且**数据范围异常大** $(0 \le K \le 10^{18})$ 的题目，我们可以考虑倍增。

以 $Testcase$ $1$ 为例。

原输入为：
```
7 3
5 2 6 3 1 4 6
1 2 3 5 7 9 11
```
我们先模拟 $1$ 次操作：
```
7 2 9 3 1 5 9
```
在上面的基础上再模拟 $1$ 次：
```
1 2 5 9 7 3 5
```
这样，我们就可以将两步合并为一步，跳过第 $1$ 次的模拟，只需要 $\dfrac k 2$ 次操作即可获得我们需要的数组。

继续进行合并，$4$ 步、 $8$ 步、 $16$ 步、 $32$ 步…… $k$ 次操作便能很快完成。

如果 $k$ 为奇数，需要先操作一次将其转换为偶数再进行倍增。

时间复杂度：$O(n\log _k)$。

倍增思想在快速幂算法、求 $LCA$ (最近公共祖先) 中均有应用，可以大大降低重复操作的时间复杂度。

此外，本题还有时间复杂度为 $O(n)$ 的图论做法，可自行阅读[官方题解](https://atcoder.jp/contests/abc367/editorial/10719)。
# 完整代码
```cpp
#include<bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'
int n, k;

signed main(){
	ios::sync_with_stdio(false); cin.tie(0); cout.tie(0); //cin cout 优化
	cin >> n >> k;
	vector<int> x(n);
	vector<int> y(n);
	for(int i = 0; i < n; i++){
		cin >> x[i];
		x[i]--; //下标从0开始
	}
	iota(y.begin(), y.end(), 0); //将 y 赋值为0 ~ n-1
	while(k > 0){
		if(k % 2 == 1){ //k为奇数则操作一次
			for(int i = 0; i < n; i++){
				y[i] = x[y[i]]; 
			}
		}
		
		vector<int> tmp(n);
		for(int i = 0; i < n; i++){
			tmp[i] = x[x[i]];
		}
		x = move(tmp); //将tmp直接覆盖到x上，时间复杂度 O(1)
		k /= 2; //倍增
	}
	vector<int> a(n);
	vector<int> b(n);
	for(int i = 0; i < n; i++){
		cin >> a[i];
	}
	for(int i = 0; i < n; i++){
		b[i] = a[y[i]];
		cout << b[i] << " \n"[i == N - 1];
	}
	return 0;
}

```
# 参考
[Submission #56848064 - jiangly](https://atcoder.jp/contests/abc367/submissions/56848064)

[E - Permute K times Editorial - physics0523](https://atcoder.jp/contests/abc367/editorial/10707)

[3分でAtCoder Beginner Contest 367 A-E - evima lab](https://www.youtube.com/watch?v=DwvywXofusc)
