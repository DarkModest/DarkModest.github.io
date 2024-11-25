# 模拟赛

## 植物收集

[单调栈 - 洛谷专栏](https://oi-wiki.org/ds/monotonous-stack/#应用)

[RMQ - OI Wiki](https://oi-wiki.org/topic/rmq/)

## 最美子序列

[容斥原理 - OI Wiki](https://oi-wiki.org/math/combinatorics/inclusion-exclusion-principle/)

子序列问题 怎么样不记重复？

[对求本质不同子序列个数的一点理解 - hzy1 - 博客园](https://www.cnblogs.com/hzy1/p/16878663.html)

[辰星凌的博客QAQ](https://www.cnblogs.com/Xing-Ling/p/11594147.html)

## 字符序列



## 网络攻防



# 杂题选讲

[P5664 [CSP-S2019] Emiya 家今天的饭](https://www.luogu.com.cn/problem/P5664)

[P1578 奶牛浴场 - 洛谷 | 计算机科学教育新生态](https://www.luogu.com.cn/problem/P1578)

极大子矩形问题。

[P3275 [SCOI2011] 糖果](https://www.luogu.com.cn/problem/P3275)

[P3628 [APIO2010] 特别行动队](https://www.luogu.com.cn/problem/P3628)

# 算法 & 数据结构

[单调队列 - OI Wiki ](https://oi-wiki.org/ds/monotonous-queue/) |  [P1886 滑动窗口 /【模板】单调队列](https://www.luogu.com.cn/problem/P1886)

```cpp
const int N = 1e6+5;
int n, k;
int a[N];
deque<int> q;
signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> n >> k;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
    }
    for(int i = 1; i <= n; i++){
        while(!q.empty() && a[q.back()] >= a[i]) q.pop_back();
        q.push_back(i);
        if(i >= k){
            while(q.front() <= i - k) q.pop_front();
            cout << a[q.front()] << " ";
        }
    }
    cout << endl;
    while(!q.empty()) q.pop_front();
    for(int i = 1; i <= n; i++){
        while(!q.empty() && a[q.back()] <= a[i]) q.pop_back();
        q.push_back(i);
        if(i >= k){
            while(q.front() <= i - k) q.pop_front();
            cout << a[q.front()] << " ";
        }
    }
    return 0;
}
```

