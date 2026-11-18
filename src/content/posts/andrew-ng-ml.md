---
title: "吴恩达机器学习 笔记"
published: 2026-11-14
description: "吴恩达机器学习课程笔记：监督/无监督学习、单变量线性回归与梯度下降等。"
tags: [MachineLearning]
category: Notes
draft: false
---

# 引言

## 监督学习

监督学习指的是给定一个由“正确答案”组成的数据集，运用学习算法算出更多的结果。常用**回归**和**分类**。

回归：拟合数据成一个函数，使其与真实的数据集残差平方和最小。

分类：推测离散的输出值（可以不是数字，例：0/1）。

## 无监督学习

交给算法大量没有标签的数据，学习算法自己找到数据集中的结构。

聚类算法：自动判断数据的聚集簇。

# 单变量线性回归

给出一个数据集，称为**训练集**，经过学习算法，得出解决方案，称为**假设** $h$（hypothesis）。

单变量线性回归问题可以表示为 $h_\theta \left( x \right)=\theta_{0} + \theta_{1}x$。我们需要为模型引入合适的**参数**（**parameters**）$\theta_{0}$和$\theta_{1}$。模型所预测的值与实际值的差称为**建模误差**（**modeling error**）。

残差平方和函数又称代价函数。

我们的目标是选择出可以使建模误差**残差平方和最小**的模型参数。

可以画出一个等高线图，三个坐标分别为$\theta_{0}$和$\theta_{1}$ 和$J(\theta_{0}, \theta_{1})$，可以看出三维空间中存在一个使得$J(\theta_{0}, \theta_{1})$ 最小的点。

## 梯度下降

用来求函数最小值的算法。可以求出代价函数$J(\theta_{0}, \theta_{1})$ 的最小值。

思想：随机选择一个参数组合，计算代价函数，然后寻找下一个能让代价函数值下降最多的参数组合。持续执行直到找到**局部最小值**。求导得到这个参数组合所在点的切线斜率，并逐渐移动至斜率为0。

$$
\begin{array}{l}
\textbf{Gradient descent algorithm} \\
\\
\text{repeat until convergence \{} \\
\quad \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta_0, \theta_1) \quad (\text{for } j = 0 \text{ and } j = 1) \\
\text{\}} \\
\hline
\textbf{Correct: Simultaneous update} \\
\text{temp0} := \theta_0 - \alpha \frac{\partial}{\partial \theta_0} J(\theta_0, \theta_1) \\
\text{temp1} := \theta_1 - \alpha \frac{\partial}{\partial \theta_1} J(\theta_0, \theta_1) \\
\theta_0 := \text{temp0} \\
\theta_1 := \text{temp1}
\end{array}
$$

α是**学习率**，决定我们向下降程度最大的方向迈的步子有多大。α太小会导致步数过多，α太大会导致无法收敛，甚至发散。

$\frac{\partial J}{\partial \theta_j}$：代价函数对第 $j$ 个参数的偏导数，也就是梯度分量。

> 可以理解为控制变量：当其它 $\theta$不动，变化$\theta_j$，观察其对$J$ 的影响。
>
> 如果 $\frac{\partial J}{\partial \theta_j}>0$，说明增大 $\theta_j$会让$J$增大，所以应该减小$\theta_j$；  
> 如果 $\frac{\partial J}{\partial \theta_j}<0$，说明增大 $\theta_j$会让$J$减小，所以应该增大$\theta_j$。

我们需要同时更新${\theta_{0}}$和${\theta_{1}}$。

批量梯度下降：每走一步，代价函数的求和都用到了所有的训练样本。

## 梯度下降的线性回归

将梯度下降与平方误差代价函数结合，可以求出 $J$ 的偏导数。

$j=0$ 时：$\frac{\partial}{\partial {{\theta }_{0}}}J=\frac{1}{m}\sum\limits_{i=1}^{m}{\left( {{h}_{\theta }}({{x}^{(i)}})-{{y}^{(i)}} \right)}$

$j=1$ 时：$\frac{\partial}{\partial {{\theta }_{1}}}J=\frac{1}{m}\sum\limits_{i=1}^{m}{\left( \left( {{h}_{\theta }}({{x}^{(i)}})-{{y}^{(i)}} \right)\cdot {{x}^{(i)}} \right)}$

>  $j=1$多出的$x^{(i)}$ 来自链式法则：$h_\theta(x)=\theta_0+\theta_1x$中$\theta_1$的“系数”是$x$，对 $\theta_0$的系数是 1。平方求导产生的 2 恰好与$\frac{1}{2m}$ 中的 2 约掉。

算法为（注意同步更新）：

$$
\begin{array}{l}
\text{repeat \{} \\
\quad \theta_0 := \theta_0 - \alpha\frac{1}{m}\sum_{i=1}^{m}\left(h_\theta(x^{(i)}) - y^{(i)}\right) \\
\quad \theta_1 := \theta_1 - \alpha\frac{1}{m}\sum_{i=1}^{m}\left(h_\theta(x^{(i)}) - y^{(i)}\right)\cdot x^{(i)} \\
\text{\}}
\end{array}
$$

$h_\theta(x^{(i)}) - y^{(i)}$ 即预测误差：预测普遍偏高（误差为正）则参数往下调，偏低则往上调。

线性回归的平方误差代价函数是**凸函数**（碗状），只有一个**全局最小值**，梯度下降必定收敛到全局最优，不必担心局部最优。

# 线性代数

## 矩阵和向量

矩阵是填满数的表格，维数 = 行数 × 列数（先说行，后说列）。

向量是只有一列的矩阵（$n \times 1$），课程中的向量默认是**列向量**。

ML 视角：训练集装成矩阵 $X$（每行一个样本，每列一个特征），标签装成向量 $y$，参数装成向量 $\theta$。

## 加法和标量乘法

矩阵加法：形状相同的矩阵对应位置相加，形状不同不能加。

标量乘法：一个数乘进每一个格子。除法即乘倒数。

## 矩阵向量乘法

$m \times n$矩阵乘$n \times 1$向量，得到$m \times 1$ 向量。矩阵**列数**必须等于向量**行数**。

结果的第 $i$个元素 = 矩阵第$i$ 行与向量**对应位置相乘再求和**（点积）：

$$
\begin{bmatrix} 1 & 3 \\ 4 & 0 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} 1 \\ 5 \end{bmatrix} = \begin{bmatrix} 1\cdot1 + 3\cdot5 \\ 4\cdot1 + 0\cdot5 \\ 2\cdot1 + 1\cdot5 \end{bmatrix} = \begin{bmatrix} 16 \\ 4 \\ 7 \end{bmatrix}
$$

与线性回归的关键连接：给每个样本补一个恒为 1 的特征 $x_0 = 1$，则 $h_\theta(x) = \theta_0 x_0 + \theta_1 x_1$ 恰为点积。把训练集摆成矩阵（第一列全为 1）：

$$
\underbrace{\begin{bmatrix} 1 & 2104 \\ 1 & 1416 \\ 1 & 1534 \\ 1 & 852 \end{bmatrix}}_{X,\;4\times2} \underbrace{\begin{bmatrix} \theta_0 \\ \theta_1 \end{bmatrix}}_{\theta,\;2\times1} = \begin{bmatrix} \theta_0 + 2104\theta_1 \\ \theta_0 + 1416\theta_1 \\ \theta_0 + 1534\theta_1 \\ \theta_0 + 852\theta_1 \end{bmatrix} = \begin{bmatrix} h_\theta(x^{(1)}) \\ h_\theta(x^{(2)}) \\ h_\theta(x^{(3)}) \\ h_\theta(x^{(4)}) \end{bmatrix}
$$

一次乘法算出全部样本的预测，for 循环消失，这就是**向量化**。

## 矩阵乘法

$m \times n$乘$n \times o$，得到 $m \times o$。中间两个 $n$ 必须相等（左列数 = 右行数），它们会“抵消”。

把右边矩阵看成一列一列的向量：$AB$的第$j$列 =$A$乘$B$的第$j$ 列。

## 矩阵乘法的性质

不满足交换律：$AB \neq BA$（**形状**常常不允许反过来乘；即使形状允许，**数值**也一般不同）。

满足结合律：$A(BC) = (AB)C$，连乘可不加括号。

**单位矩阵** $I$：主对角线全为 1、其余全为 0 的方阵。$AI = IA = A$，相当于数字中的 1。

## 逆、转置

**逆矩阵**：方阵 $A$的逆$A^{-1}$满足$AA^{-1} = A^{-1}A = I$。只有方阵才谈逆，且并非所有方阵都可逆（不可逆的称**奇异矩阵**，类比数字 0 没有倒数）。

**转置** $A^T$：沿主对角线“翻面”，第 $i$行第$j$列元素变到第$j$行第$i$ 列，$m \times n$变$n \times m$。MATLAB 中写作 `A'`。

基本性质：

$$
(A \pm B)^T = A^T \pm B^T \qquad (AB)^T = B^T A^T \qquad (A^T)^T = A \qquad (kA)^T = kA^T
$$

> 其中 $(AB)^T = B^T A^T$最反直觉，**顺序必翻转**。原因：形状上$A^T B^T$ 常常不能乘——$A$为$2\times3$、$B$为$3\times4$ 时，$A^T B^T$是$(3\times2)(4\times3)$，中间 2 对 4 配不上对；而 $B^T A^T$是$(4\times3)(3\times2)$，正好配对，且结果 $4\times2$与$(AB)^T$ 形状吻合。直觉：脱衣服顺序——先穿袜子再穿鞋，必须先脱鞋再脱袜子。求逆同理：$(AB)^{-1} = B^{-1}A^{-1}$。

# 多变量线性回归

## 多维特征

对一个单变量模型增加更多的特征，构成一个含有多变量的模型。模型中的特征为$\left( {x_{1}},{x_{2}},...,{x_{n}} \right)$ 。${x^{\left( i \right)}}$代表第 $i$ 个训练实例，是特征矩阵中的第$i$行，是一个**向量**（**vector**）。${x}_{j}^{\left( i \right)}$代表特征矩阵中第 $i$个训练实例的第$j$ 个特征。

支持多变量的假设 $h$ 表示为：$h_{\theta} \left( x \right)={\theta_{0}}{x_{0}}+{\theta_{1}}{x_{1}}+{\theta_{2}}{x_{2}}+...+{\theta_{n}}{x_{n}}$。

此时模型中的参数、任一训练实例都是一个 $n+1$维的向量。特征矩阵$X$的维度是$m \times (n+1)$，因此公式可以简化为 $h_\theta (x) = \theta^T X$。

# 多变量梯度下降

类似单变量线性回归，在多变量线性回归中，构建一个代价函数所有**建模误差**的总和：

$$
J\left( {\theta_{0}},{\theta_{1}}...{\theta_{n}} \right)=\frac{1}{2m}\sum\limits_{i=1}^{m}{{{\left( h_{\theta} \left({x}^{\left( i \right)} \right)-{y}^{\left( i \right)} \right)}^{2}}}
$$

> 多变量线性回归的代价函数中，添加一个常数$\frac 1 2$ 能使求导后的式子保持简洁，而不影响取得最小值的位置。

我们的目标：找出使得代价函数最小的一系列参数。

多变量批量梯度下降公式：

$$
\begin{aligned}
&\text{Repeat } \{ \\
&\quad \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta_0, \theta_1, ..., \theta_n) \\
&\}
\end{aligned}
$$

代入代价函数：

$$
\begin{aligned}
&\text{Repeat } \{ \\
&\quad \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2 \\
&\}
\end{aligned}
$$

求导：

$$
\begin{aligned}
&\text{Repeat } \{ \\
&\quad \theta_j := \theta_j - \alpha \frac{1}{m} \sum_{i=1}^{m} \left( (h_\theta(x^{(i)}) - y^{(i)}) \cdot x_j^{(i)} \right) \\
&\quad ( \text{ simultaneously update } \theta_j \\
&\quad \text{for } j=0, 1, ..., n ) \\
&\}
\end{aligned}
$$

随机选择一系列的参数值，计算所有的预测结果，再给所有的参数一个新的值，如此循环直到收敛。

## 梯度下降实践

### 特征缩放

对于多维特征问题，要让特征数值具有相同的尺度，帮助梯度下降算法更快的收敛。

如房价问题，当尺寸范围为0-2000英尺、房间数量为1-5时，可以对尺寸数据除以2000、房间数量除以5，使其都在$[-1, 1]$ 范围内。此时图像趋近于圆，梯度下降在最坏情况下效率高。

### 检查收敛和选择学习率

梯度下降算法收敛的迭代次数随模型变化而变化，因此我们可以先画出**迭代次数和代价的函数图像**判断模型在何处收敛。

学习率不可以过小或过大，但我们无法预知合适的学习率。因此，尝试一系列不同数量级的值（例如0.001, 0.003, 0.01, 1...）可以找到一个最大的可行学习率，或使用比这个值略小的值作为学习率。

将 $\alpha$ 设为一个足够小的数可以对模型进行调试，此时如果代价变大，说明代码中有 bug。

## 多项式回归

线性回归不适用于所有的数据。有时我们需要使用曲线适应数据，比如二次方模型$h_{\theta}\left( x \right)={\theta_{0}}+{\theta_{1}}{x_{1}}+{\theta_{2}}{x_{2}^2}$或三次方模型 $h_{\theta}\left( x \right)={\theta_{0}}+{\theta_{1}}{x_{1}}+{\theta_{2}}{x_{2}^2}+{\theta_{3}}{x_{3}^3}$。先观察、再使用合适的函数。

采用多项式回归的时候，特征**缩放**非常必要。

# 正规方程

正规方程：通过求解$\frac{\partial}{\partial{\theta_{j}}}J\left( {\theta_{j}} \right)=0$ 来使得代价函数最小的参数。正规方程对于某些线性回归问题是**更好的解决方案**。

**结论**：假设我们的训练集特征矩阵为 $X$（包含了 ${{x}_{0}}=1$）并且我们的训练集结果为向量 $y$，则利用正规方程解出向量 $\theta ={{\left( {X^T}X \right)}^{-1}}{X^{T}}y$ 。

# 逻辑回归

## 分类问题

分类问题：预测变量$y$是离散的值（如0/1）。

二元分类：将**因变量**可能属于的两个类分为**正向类**和**负向类**，即：$y\in \{0,1\}$ ，其中 0 表示负向类，1 表示正向类。

线性回归算法不适合解决分类问题的原因：预测值可能远大于1或远小于0。因此使用逻辑回归算法处理分类问题。

我们引入一个新的模型，逻辑回归，该模型的输出变量范围始终在0和1之间。

### 假设表示

逻辑回归模型的假设是： $h_\theta \left( x \right)=g\left(\theta^{T}X \right)$
其中：
$X$ 代表特征向量
$g$代表逻辑函数，一个常用的逻辑函数为**Sigmoid**函数，公式为：$g\left( z \right)=\frac{1}{1+{{e}^{-z}}}$。

### 判定边界

逻辑函数可以利用参数 $\theta$在特征空间中划出一条线（或曲线），将不同的类别区分开。如在$g(z)$ 中，当${h_\theta}\left( x \right)\ge 0.5$时，预测 $y=1$。反之预测 $y=0$ 。

### 代价函数

对于逻辑回归模型，如果沿用线性回归的代价函数，我们将会得到一个**非凸函数**，有许多局部最小值，影响梯度下降算法。

逻辑回归的代价函数：

我们重新定义逻辑回归的代价函数为：

$$
J(\theta) = \frac{1}{m} \sum_{i=1}^{m} Cost \left( h_\theta \left( x^{(i)} \right), y^{(i)} \right)
$$

其中：

$$
Cost(h_\theta(x), y) =
\begin{cases}
-\log(h_\theta(x)) & \text{if } y = 1 \\
-\log(1 - h_\theta(x)) & \text{if } y = 0
\end{cases}
$$

可以化简为：

$$
J\left( \theta  \right)=-\frac{1}{m}\sum\limits_{i=1}^{m}{[{{y}^{(i)}}\log \left( {h_\theta}\left( {{x}^{(i)}} \right) \right)+\left( 1-{{y}^{(i)}} \right)\log \left( 1-{h_\theta}\left( {{x}^{(i)}} \right) \right)]}
$$

就可以使用梯度下降算法了。

$$
\begin{aligned}
& \textbf{Repeat} \{ \\
& \quad \theta_j := \theta_j - \alpha \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} \\
& \quad \text{(simultaneously update all } \theta_j \text{)} \\
& \}
\end{aligned}
$$

除梯度下降算法外，我们还可以使用共轭梯度、局部优化法、有限内存局部优化法。

### 公式简化

$$
J(\theta) = -\frac{1}{m} \sum_{i=1}^{m} \left[ y^{(i)} \log\left(h_\theta(x^{(i)})\right) + (1 - y^{(i)}) \log\left(1 - h_\theta(x^{(i)})\right) \right]
$$

$$
\begin{aligned}
& \textbf{Repeat} \{ \\
& \quad \theta_j := \theta_j - \alpha \frac{1}{m} \sum_{i=1}^{m} \left( h_\theta(x^{(i)}) - y^{(i)} \right) x_j^{(i)} \\
& \quad \text{(simultaneously update all } \theta_j \text{)} \\
& \}
\end{aligned}
$$

### 多类别分类

对于将一类数据分成多类的问题（邮件分组、药物诊断等），可以使用**一对余**的方法，即选择一类作为正向类、将其它类作为反向类，进行二元分类，以此类推。

即：

1. 将数据分为两类，类别$i$和其余；

2. 训练模型$h_\theta^i$ 用来判断“是不是类别$i$”；

3. 对于未知样本，输入进所有的训练模型，采用最大置信度进行分类。

## 正则化

### 过拟合

对于一个数据集，当假设中$x$的次数过低（线性模型），会导致欠拟合；当$x$的次数过高，预测新数据的能力会变差，导致过拟合。中间的模型往往最合适。

当我们发现了过拟合问题，应该：

1. 丢弃不能帮助我们正确预测的特征；

2. 正则化：保留特征，减少参数的大小。

由于高次项导致了过拟合，所以通过正则化降低高次项的系数就可以很好的拟合。我们要做的就是修改代价函数，在高次项系数上设置惩罚。

例：

$$
\underset{\theta }{\mathop{\min }}\,\frac{1}{2m}[\sum\limits_{i=1}^{m}{{{\left( {{h}_{\theta }}\left( {{x}^{(i)}} \right)-{{y}^{(i)}} \right)}^{2}}+1000\theta _{3}^{2}+10000\theta _{4}^{2}]}
$$

这样 $\theta_3$和$\theta_4$ 对预测结果的影响变小。

如果特征很多，不知道要惩罚其中哪些特征，可以对所有特征进行惩罚，让代价函数最优化的软件来选择惩罚程度。

$$
J\left( \theta  \right)=\frac{1}{2m}[\sum\limits_{i=1}^{m}{{{({h_\theta}({{x}^{(i)}})-{{y}^{(i)}})}^{2}}+\lambda \sum\limits_{j=1}^{n}{\theta_{j}^{2}}]}
$$

其中 $\lambda$ 称为正则化参数。一般不对 $\theta_0$ 惩罚。如果 $\lambda$ 过大，会导致所有的 $\theta$ 过小，以至于趋近于零，导致欠拟合。

## 正则化线性回归

# 神经网络

## 非线性假设

对于普通的逻辑回归，想要拟合**弯曲、复杂**的判定边界，模型假设必须对原始输入$x$是**非线性的**。使用非线性的**多项式项**能够帮助我们建立更好的分类模型，但我们会得到**数量惊人**的特征组合。普通的逻辑回归模型不能有效地处理这么多的特征，这时候我们需要**神经网络**。

## 模型表示

每个**神经元**都是一个学习模型。神经网络由神经元组成。

分为三层：

1. 输入层：由输入单元组成，负责输入原始数据

2. 隐藏层（Hidden Layers）：负责处理数据并传递到下一层

3. 输出层：计算 $h_\theta(x)$。

为每一层添加一个偏差单位（类似$\theta_0$）。

标记方法：

- $a_i^{(j)}$表示第$j$层的第$i$个激活单元。
- $\theta^{(j)}$表示从第$j$层映射到第$j+1$层的权重的矩阵。
- 尺寸为：以第$j+1$层的激活单元数量为**行数**，以第$j$层的激活单元数$+1$为**列数**的矩阵。

## 特征与直观理解

1. 隐藏层在学习“新特征”

   - 在普通逻辑回归中，我们通常使用原始特征$x_i$，或手动构造多项式特征。但在神经网络中，输出层用隐藏层的中间变量$a_i$做逻辑回归。

   - 因此，神经网络先用隐藏层把原始特征$x$转化为更高级的特征$a$，再用这些新特征做分类。

2. 单层神经元可以做逻辑运算

   - 一个没有中间层（隐藏层）的神经元，可以通过**增大权重**的方式实现 AND/OR/NOT 逻辑运算。

   - 把多个神经元组合可以表示更复杂的逻辑函数，比如 XNOR。

   - 层数越多，组合越多，就能表达越来越复杂的非线性函数。

## 多类分类

定义：把输出层从1个神经元扩展到k个神经元，每个神经元负责判断一个类别。

训练时，标签应为one-hot向量，对应类别的值为1，其它值为0。预测时，看哪个值最大就判为哪个类。
