# ABC354 C - Atcoder Magics
## 题目翻译
### 问题陈述

高桥有纸牌游戏 "AtCoder Magics"中的 $N$ 张卡片。其中的第 $i$ 张卡片将被称为 卡片 $i$ 。每张卡片都有两个参数：强度和成本。卡片 $i$ 的强度为 $A_i$ ，成本为 $C_i$ 。

他不喜欢弱牌，所以他会弃掉它们。具体来说，他会重复下面的操作，直到无法再进行为止：

- 选择两张卡片 $x$ 和 $y$ ，即 $A_x > A_y$ 和 $C_x < C_y$ 。弃牌 $y$ 。

可以证明，当无法再进行这些操作时，剩余卡片的集合是唯一确定的。请找出这组卡片。
### 限制因素

- $2 \leq N \leq 2 \times 10^5$
- $1 \leq A _ i, C _ i \leq 10^9$
- $A _ 1, A _ 2, \dots ,A _ N$ 都是不同的。
- $C _ 1, C _ 2, \dots ,C _ N$ 都是不同的。
- 所有输入值均为整数。
#### 输出

剩下的卡片有 $m$ 张，按**升序**排列为 $i _ 1, i _ 2, \dots, i _ m$ 张。按以下格式打印：


$m$  
$i_1$ $i_2$ $\cdots$ $i_m$
## 解题思路
定义一个结构体，存储卡片的编号、强度、成本，并以强度大小的顺序将结构体排序。  
枚举比较成本。若 $C_i$ 小于它前面所有卡片的成本的最低值，不满足 $A_x > A_y$ 且 $C_x < C_y$，没有卡片能弃掉卡片 $i$ ，便存入答案数组。  
遍历后能得到剩余卡片的集合。升序排序后输出。
## 总结
考察对结构体排序的应用。  
[sort cmp函数与结构体排序应用 - Dark_Modest](https://www.luogu.com.cn/article/b3bjhytg)
## 示例代码
```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'

const int N = 2e5+5;
int minn = 1e9+1;
struct card{
    int id;
    int a;
    int c;
} m[N];
int n;
vector<int> ans;

bool cmp(card x, card y){
    return x.a > y.a;
}

signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

    cin >> n;
    for(int i = 1; i <= n; i++){
        cin >> m[i].a >> m[i].c;
        m[i].id = i;
    }
    sort(m + 1, m + n + 1, cmp);
    for(int i = 1; i <= n; i++){
        if(minn > m[i].c){
            minn = m[i].c;
            ans.push_back(m[i].id);
        }
    }
    sort(ans.begin(), ans.end());
    cout << ans.size() << endl;
    for(int i = 0; i < ans.size(); i++){
        cout << ans[i] << " ";
    }
    return 0;
}
```