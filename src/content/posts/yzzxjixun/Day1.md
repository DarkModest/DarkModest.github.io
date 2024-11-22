---
title: YZZX 集训笔记 Day1
published: 2024-11-22
tags: [OI, 扬中集训]
category: Notes
draft: false
---

# 模拟赛 - 图论专项（一）

$$ 10 / 400 $$

## T1 机器人擂台赛 (ranking, [CF645D](https://www.luogu.com.cn/problem/CF645D))

拓扑序唯一性。即，在拓扑排序过程中，不能出现多个入度为 $0$ 的节点，否则无法判断机器人级别。

二分答案，当`q.size() > 1`时，拓扑序不唯一，缩小范围，直到找到唯一拓扑序为止，否则输出 `-1`。

待补。

## T2 最近奇偶数对 (parity, [CF1272E](https://www.luogu.com.cn/problem/CF1272E))

BFS，反向建图。

待补。


## T3 逃离螺旋迷宫 (maze, COCI2008, [P6399](https://www.luogu.com.cn/problem/P6399))

建图，
 $a$，跑 Dijkstra。
待补。


## T4 最优星际贸易 (COCI2012/2013 Final, HIPERPROSTOR)
关于 SPFA，它死了。因此不补。

# 算法

## 广度优先搜索 BFS

> 因为种种原因之前没有学习BFS，今天被模拟题重创才开始恶补。

**例题 [P5318  查找文献](https://www.luogu.com.cn/problem/P5318)**

核心思想：

1. 将起点先入队。此时`q.front()`为起点。

2. 重复以下操作：\
   取出队列最前端的点，遍历所有与它相邻的点。如果没有访问过，打标记并入队。遍历结束后弹出最前端的点。

```cpp
//链式前向星存图
void bfs(int u){
	queue<int> q;
	q.push(u);
	v[u] = 1;
	ans2.push_back(u); //存储路径
	while(!q.empty()){
		int fro = q.front();
		for(int i = head[fro]; i; i = e[i].nxt){
			int to = e[i].to;
			if(!v[to]){
				q.push(to);
				v[to] = 1;
				ans2.push_back(to);
			}
		}
		q.pop();
	}
}
```

[Complete Code](https://www.luogu.com.cn/record/190382151)

## 拓扑排序 (Topological Sort, Kahn)

**例题 [P4017  最大食物链计数](https://www.luogu.com.cn/problem/P4017)**

BFS的变种。仅适用于 DAG (有向无环图)，否则会在环中打转，陷入死循环。

“事实上，拓扑排序就是将一个图变化为一个线性序列的过程。故，我愿称之为降维打击。” ——[Aw顿顿](https://www.luogu.com.cn/user/212283)

核心思想：

1. 在建边的时候维护每个点的入度。
```cpp
for(int i = 1; i <= m; i++){
    int u, v;
    cin >> u >> v;
    add(u, v);
    ind[v]++;
    }
```
2. 扫一遍点，找到入度为 $0$ 的点。入队。
3. 重复操作：
   
   取出此点并出队，将其放入拓扑序数组，遍历此点的相邻点并将它们的入度 $-1$。
   (直观地说，就是删除此点)
4. 当队列为空时，说明所有节点都已进入拓扑序数组。

```cpp
bool topsort() {
    queue<int> q;
    int cnt = 0;  //输出顶点的个数
    for (int i = 1; i <= n; i++)
        if (ind[i] == 0) q.push(i);
    while (!q.empty()) {
        int x = q.front();
        q.pop();
        A[++cnt] = x;
        for (int i = 0; i < G[x].size(); i++) {
            int y = G[x][i];
            ind[y]--;
            if (ind[y] == 0) q.push(y);
        }
    }
    return cnt == n; //true:无环  false:有环
}
```
时间复杂度 $O(E + V)$。

[Complete Code](https://www.luogu.com.cn/record/190436728)

## Dijkstra 单源最短路

**例题 [P4779 【模板】单源最短路径（标准版）](https://www.luogu.com.cn/problem/P4779)**

一种贪心算法，求带**正**权图中单源点到其他所有节点的最短路。

核心思想：

1. 初始化 `dis[s] = 0`，其余顶点的 `dis`均为`inf`。
2. 在所有未标记顶点中找出 `dis` 值最小的顶点 `x` ，并标记。
3. 对 `x` 的所有未标记邻接点 `y` 进行松弛操作。
4. 重复 2、3 操作 $n$ 次 ，直至所有顶点都被标记。

```cpp
void Dijkstra(){
    for(int i = 1; i <= n; i++)
        dis[i] = inf;
    dis[s] = 0;
    d.v = s, d.w = 0; q.push(d);
    while(!q.empty()){
        int u = q.top().v;
        q.pop();
        if(vis[u]) continue;
        vis[u] = 1;
        for(int i = head[u]; i; i = e[i].next){
            if(dis[e[i].to] > (long long)dis[u] + e[i].val){
                dis[e[i].to] = dis[u] + e[i].val;
                d.v = e[i].to, d.w = dis[e[i].to]; q.push(d);
            }
        }
    }
}
```

[Complete Code](https://www.luogu.com.cn/record/184872324)

# Atcoder Beginner Contest 381

很特殊的一场比赛，A B C D E F全是和`1122`有关的。

很不幸，我 C 又爆了，赛时 WA 两个点，赛后看题解觉得自己是个SB。

# 总结

图论，得学。

# 参考
- [【图论】拓扑排序专题训练 - Aw顿顿](https://www.luogu.com.cn/training/42933)

- [拓扑排序 - OI Wiki](https://oi-wiki.org/graph/topo/)
- 超超的课件