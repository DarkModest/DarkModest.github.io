---
title: YZZX 集训笔记 Day3
published: 2024-11-24
tags: [OI, 扬中集训]
category: Notes
draft: false
---

# 树上问题

## 树的直径

**树上两节点之间最长的简单路径是树的直径。**

求法一：两次 DFS

从任意节点开始进行第一次 DFS，记录最远节点 $z$；再从节点 $z$ 开始进行第二次 DFS，记录最远节点 $z'$。$z$ 和 $z'$ 的最短路径即为树的直径。

如果有负权则无法使用两次 DFS 求树的直径，而需要使用树形 DP。

[Complete Code](https://www.luogu.com.cn/record/190885544)

求法二：树形 DP

对于树的直径，实际上是可以通过枚举从某个节点出发不同的两条路径相加的最大值求出。

[Complete Code](https://www.luogu.com.cn/record/190897020)

## 树的中心

## 树的重心

# 树上算法

## 最近公共祖先 LCA

### 朴素算法

每次找深度较大的那个点，使其向上跳。这样，两个点会交替上行，最终相遇，相遇位置即为 LCA。或者，先调整深度较大的那个点，将两个点深度统一之后一起向上跳，最终也会相遇。

### 倍增优化

倍增算法可以用于改进朴素 LCA。

首先我们需要一个`lowbit(n)`函数。 它是一个用于**获取一个数的二进制表示中最低位的1及其后所有0构成的数值**的函数。例如，$lowbit(20) = lowbit(10100)_2 = 100_2 = 4$。实现方法：

```cpp
int lowbit(x){
    return x & -x;
}
```

建立`fa[][]`数组。`fa[x][i]`表示点 $x$ 的第 $2^i$ 个祖先。可以通过 DFS 预处理。 

## 树上差分

[P3128 [USACO15DEC] Max Flow P](https://www.luogu.com.cn/problem/P3128)



## 树上贪心

[[ABC333D] Erase Leaves](https://www.luogu.com.cn/problem/AT_abc333_d) [Code](https://www.luogu.com.cn/record/191121844)

## 树形 DP

[P2014 [CTSC1997] 选课](https://www.luogu.com.cn/problem/P2014)

[P1122 最大子树和](https://www.luogu.com.cn/problem/P1122)

[P1352 没有上司的舞会](https://www.luogu.com.cn/problem/P1352)

模板：

```cpp
int dfs(int u){
    vis[u] = 1;
    //初始化
    for(int i = head[u]; i; i = e[i].nxt){
        int to = e[i].to;
        if(vis[to]) continue;
        dfs(to);
        //孩子->父亲，转移状态
    }
}
```

## 换根DP

又叫二次扫描。

相比于一般的树形 DP：

- 以树上不同点为根，其解不同。
- 求解答案需要求解每个节点的信息。
- 无法通过一次搜索完成答案求解。
- 难度比一般树形 DP 要高。

[P3478 [POI2008] STA-Station](https://www.luogu.com.cn/problem/P3478)

>给定一个 $n$ 个点的无根树，问以树上哪个节点为根时，其所有节点的深度之和最大？

如果以每个节点为根依次搜索一遍，时间复杂度为 $O(n^2)$。

考虑在第二次搜索时完成所有答案的统计。

- 第一次搜索，假设根节点为 $1$ 号节点，则此时只有 $1$ 号节点的答案已知。搜索过程中也需要**统计出所有子树的大小**。

- 第二次搜索，依然从 $1$ 号节点出发，如果 $1$ 号节点与 $x$ 节点相连，则考虑能否通过 $1$ 号节点的答案推出 $x$ 节点的答案。
- 假设此时根节点**换**为节点 $x$，此时子树由两部分构成，第一部分是原子树，第二部分是 $1$ 号节点的其它子树。![img](https://pic3.zhimg.com/v2-0f457add2a7272028a19d640ba073058_1440w.jpg)
- 根节点从 $1$ 号节点变为节点 $x$ 的过程中，可以发现，第一部分深度降低了 $1$，第二部分深度增大了 $1$。
- 现在，可以通过第一次搜索得到的节点数量得出递推公式：

$$ans[to] = ans[u] - siz[to] + (siz[1] - siz[to]), fa[to] = u$$

```cpp
void dfs(int u, int fa){
    dep[u] = dep[fa] + 1;
    dis[u]++;
    for(int i = head[u]; i; i = e[i].nxt){
        int to = e[i].to;
        if(to == fa) continue;
        dfs(to, u);
        dis[u] += dis[to];
    }
}
void dfs2(int u, int fa){
    for(int i = head[u]; i; i = e[i].nxt){
        int to = e[i].to;
        if(to == fa) continue;
        ans[to] = ans[u] - dis[to] + (dis[1] - dis[to]);
        dfs2(to, u);
    }
}
```



## 最长上升子序列 LIS

[P1020 [NOIP1999 提高组] 导弹拦截](https://www.luogu.com.cn/problem/P1020)



# 模拟赛 树专项

## [[ABC165F] LIS on Tree](https://www.luogu.com.cn/problem/AT_abc165_f)

树上LIS，用二分答案优化。

[Complete Code](https://www.luogu.com.cn/record/190942546)

## [[ABC348E] Minimize Sum of Distances](https://www.luogu.com.cn/problem/AT_abc348_e)

换根DP。

要求求最大直径最小，用二分答案求直径。

> 记录数组 $dp_u$ 表示在 $u$ 号点，其子树中所有点到达 $u$ 号点的最大链长。转移时，考虑其和子树之间的关系。
>
> 可以发现，$u$ 号点就类似于一个 LCA，两个最长的儿子拼起来的最长链就是这棵子树的最大直径。注意，这里的 $dp_v$ 中所存最长链均已保证子树内部合法。
>
> 接着考虑子树中直径超过二分的上限怎么办？贪心地想，我们肯定是要断掉最长的那条链，保留次长的。因为这样可以使得我们的总长度尽可能小，从而达到最优次数。 最后，如果必须断边的次数大于上限 $s$, 则不合格，应该调大区间，否则**一定合格**。想一想为什么。

```cpp
void dfs(int u, int fa, int lim){
    int maxn = 0;
    for(int i = head[u]; i; i = e[i].nxt){
        int to = e[i].to;
        if(to == fa) continue;
        dfs(to, u, lim);
        if(dp[to] + maxn > lim){
            sum ++;
            maxn = min(maxn, dp[to]);
        } else maxn = max(maxn, dp[to]);
    }
    dp[u] = maxn + 1;
}
```

[Complete Code](https://www.luogu.com.cn/record/190956093)

## [P3000 [USACO10DEC] Cow Calisthenics G](https://www.luogu.com.cn/problem/P3000)

树上二分

## [P6869 [COCI2019-2020#5] Putovanje](https://www.luogu.com.cn/problem/P6869)



# 参考

[树的直径 - OI Wiki](https://oi-wiki.org/graph/tree-diameter/)

[题解 P3000 [USACO10DEC]Cow Calisthenics G - 青鸟_Blue_Bird](https://www.luogu.com.cn/article/ny50jzze)

[【朝夕的ACM笔记】动态规划-换根DP - 知乎](https://zhuanlan.zhihu.com/p/348349531)
