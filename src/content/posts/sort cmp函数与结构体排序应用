---
title: sort cmp函数与结构体排序应用
published: 2024-05-07
description: First blog published on Luogu OJ.
image: 
tags: [OI]
category: Front-end
draft: false
---
# 起因
补[ABC348C](https://www.luogu.com.cn/problem/AT_abc348_c)中，发现：
1. 开二维数组空间时间双爆;
1. vector<pair<int, int>>操作过于麻烦。

于是翻题解，发现此知识漏洞，遂记录。
# 正文
## sort中的cmp函数
sort函数在不使用cmp函数下，**默认**使用升序排序的cmp函数。我们需要对cmp函数稍加定义，即可实现**自定义排序**。\
以下面的**降序**排序为例：
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

bool cmp(int left, int right){
    return left > right;
}

signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

    int a[8] = {1, 3, 2, 4, 6, 5, 7, 8};
    sort(a, a + 8, cmp);
    for(int i = 0; i < 8; i++)
        cout << a[i] << " ";
    return 0;
}
```
可以得到输出结果为：
```
8 7 6 5 4 3 2 1
```
## 结构体排序(分级排序)
直接使用**sort函数**对结构体进行**升序排序**往往在算法竞赛中无法满足解题需求。**cmp函数**能够弥补这一问题。\
以[ABC348C](https://www.luogu.com.cn/problem/AT_abc348_c)为例。
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

const int N = 2e5 + 5;
struct d{ //定义结构体
    int a, c;
} b[N];
int n;
int ans = 0;

bool cmp(d x, d y){ //cmp函数
    if(x.c == y.c) return x.a < y.a; //颜色相同,按照美味度升序排序
    else return x.c < y.c; //颜色不同,按照颜色升序排序
}

signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

    //输入
    cin >> n;
    for(int i = 1; i <= n; i++)
        cin >> b[i].a >> b[i].c;

    sort(b + 1, b + n + 1, cmp); //排序
    for(int i = 1; i <= n; i++){
        if(b[i].c != b[i - 1].c) //如果颜色改变,此时b[i].a为颜色为b[i].c的豆子的最小美味度
            ans = max(ans, b[i].a); //记录所有豆子中最大的最小美味度
    }
    cout << ans << endl;
    return 0;
}
```
[AC Record](https://atcoder.jp/contests/abc348/submissions/53218546)\
\
另一道例题([P1104 生日](https://www.luogu.com.cn/problem/P1104))。\
通过**年、月、日、输入顺序**的四层排序，能够非常简单地解决这一题。\
其中cmp函数的if语句嵌套需要以**符合自己的逻辑顺序**的方法书写，否则容易**思路打结**。\
AC Code:
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

int n;
const int N = 105;
struct b{
    int id; 
    string s;
    int y;
    int m;
    int d;
} a[N];

bool cmp(b left, b right){ //以年、月、日、输入顺序的顺序依次排序
    if(left.y == right.y){ //年份相等则进入下一层比较，不相等则得出比较顺序。月、日同理
        if(left.m == right.m){
            if(left.d == right.d){
                return left.id > right.id; //年月日全部相同，比较输入顺序
            } else {
                return left.d < right.d;
            }
        } else {
            return left.m < right.m;
        }
    } else {
        return left.y < right.y;
    }
}

signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> a[i].s >> a[i].y >> a[i].m >> a[i].d;
        a[i].id = i; //输入顺序需要手动标记
    }
    sort(a + 1,a + n + 1, cmp); //排序
    for(int i = 1; i <= n; i++){
        cout << a[i].s << endl;
    }
    return 0;
}
```
[AC Record](https://www.luogu.com.cn/record/158606587)
## 引用&参考
[题解：AT_abc348_c [ABC348C] Colorful Beans - klyj1](https://www.luogu.com.cn/article/q3rswefa)\
[sort函数中的cmp函数使用 - thlzzz, CSDN](https://blog.csdn.net/thlzzz/article/details/109695582)\
[C++/C sort函数用法（详细),cmp的构造--一学就会，一用就对 - 渣渣高不会写Java， CSDN](https://blog.csdn.net/m0_52410356/article/details/113802527)
## Changelog
2024/5/10： 添加第二条例题
