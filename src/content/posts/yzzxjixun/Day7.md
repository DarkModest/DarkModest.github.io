---
title: YZZX 集训笔记 Day4
published: 2024-11-25
tags: [OI]
category: Notes
draft: false
---
## [P10277 [USACO24OPEN] Bessie's Interview S](https://www.luogu.com.cn/problem/P10277)

因为每头牛所面试的农夫可能不同，但是开始时间和结束时间必定相同，所以我们先记录 Bessie 前每头奶牛的结束时间。结束时间的最大值即为第一问答案。 使用优先队列 。

第二问，需要我们在用优先队列的过程中记录每头奶牛的开始和结束时间。然后用 Bessie 的开始时间找前一头奶牛的结束时间，再向前寻找，最终找到 编号 $1$ 到 $k$ 的奶牛，确定农夫。

可以 `set`维护。遍历到一个奶牛时，如果这个奶牛的结束时间正好是我们要找的，就把它的开始时间放入`set`。如果 $i <= k$ 即可记录答案。

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'
const int N = 3e5+5;
#define pii pair<int,int>
int n, k, a[N], vis[N], ans;
int st[N], e[N];
priority_queue<int,vector<int>,greater<int> > q;
set<int> s;
signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
	// freopen("interview.in", "r", stdin);
    // freopen("interview.out", "w", stdout);
    cin >> n >> k;
    for(int i = 1; i <= n; i++) cin >> a[i];
	for(int i = 1; i <= k; i++) {
        e[i] = a[i];
        q.push(e[i]);
    }
	for(int i = k + 1; i <= n; i++){
		int fro = q.top();
        q.pop();
        st[i] = fro, fro += a[i], e[i] = fro;
        q.push(fro);
	}
    cout << q.top() << endl;
    s.insert(q.top());
    for(int i = n; i >= 1; i--){
        if(s.find(e[i]) != s.end()){
            s.insert(st[i]);
            if(i <= k) vis[i] = 1;
        }
    }
	for(int i = 1; i <= k; i++) cout << vis[i];
    return 0;
}
```



## [P10192 [USACO24FEB] Moorbles S](https://www.luogu.com.cn/problem/P10192)

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define endl '\n'
const int N = 3e5+5;
int t, n, m, k;
int a[5];
int e[N], o[N], w[N];
signed main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> t;
    while(t--){
        cin >> n >> m >> k;
        memset(o, 0x3f, sizeof(o)), memset(e, 0x3f, sizeof(e));
        for(int i = 1; i <= m; i++){
            for(int j = 1; j <= k; j++){
                cin >> a[j];
                if(a[j] & 1)
                    o[i] = min(o[i], a[j]), e[i] = min(e[i], -a[j]);
                else
                    o[i] = min(o[i], -a[j]), e[i] = min(e[i], a[j]);
            }
            w[i] = max(e[i], o[i]);
        }
        w[m + 1] = 0;
        for(int i = m; i >= 1; i--)
            w[i] = min(w[i] + w[i + 1], 0ll);
        if(n + w[1] <= 0){
            cout << -1 << endl;
            continue;
        }
        for(int i = 1; i <= m; i++){
            n += max(e[i], o[i]);
            if(e[i] >= o[i]) cout << "Even "; // L34: n += e[i]
            else if(n - o[i] + e[i] + w[i + 1] > 0) //L34: n += o[i] 先亏后赚
                cout << "Even ", n = n - o[i] + e[i];
            else cout << "Odd ";
            assert(n > 0);
        }
        cout << endl;
    }
    return 0;
}
```