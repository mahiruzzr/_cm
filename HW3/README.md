### 1.1 基本幾何物件
在解析幾何中，我們將幾何圖形數值化：

* **點 (Point)**:
    * 定義：二維空間中的位置。
    * 表示法：向量 $\mathbf{v} = (x, y)$。
* **線 (Line)**:
    * 定義：無限延伸的直線。
    * 表示法（一般式）：$Ax + By = C$。
    * *為什麼不用斜截式 ($y=mx+b$)？* 因為一般式可以處理垂直線（斜率 $m$ 無限大）的情況，且在計算交點時更容易轉化為矩陣運算。
* **圓 (Circle)**:
    * 定義：到定點（圓心）距離為定值（半徑）的集合。
    * 表示法：$(x-h)^2 + (y-k)^2 = r^2$。

### 1.2 核心演算法原理

#### A. 兩直線交點 (Intersection of Two Lines)
計算兩直線 $L_1: A_1x + B_1y = C_1$ 與 $L_2: A_2x + B_2y = C_2$ 的交點，等同於解線性方程組。
使用 **克拉瑪公式 (Cramer's Rule)**：
$$
D = \det\begin{pmatrix} A_1 & B_1 \\ A_2 & B_2 \end{pmatrix} = A_1B_2 - A_2B_1
$$
若 $D \neq 0$，則交點 $(x, y)$ 為：
$$
x = \frac{\det\begin{pmatrix} C_1 & B_1 \\ C_2 & B_2 \end{pmatrix}}{D}, \quad y = \frac{\det\begin{pmatrix} A_1 & C_1 \\ A_2 & C_2 \end{pmatrix}}{D}
$$

#### B. 點到直線的垂足 (Projection)
給定直線 $L: Ax + By = C$ 與點 $P(x_0, y_0)$。
* 直線 $L$ 的法向量為 $\mathbf{n} = (A, B)$。
* 垂線 $L_{\perp}$ 必平行於 $\mathbf{n}$，故其方程式形式為 $-Bx + Ay = K$。
* 求出 $L$ 與 $L_{\perp}$ 的交點即為垂足。

#### C. 幾何變換 (Transformations)
所有變換均基於線性代數運算。假設點 $P$ 為行向量 $\begin{bmatrix} x \\ y \end{bmatrix}$：

1.  **平移 (Translation)**: 向量加法。
    $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} dx \\ dy \end{bmatrix}$$
2.  **縮放 (Scaling)**: 矩陣乘法（對角矩陣）。
    $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$
3.  **旋轉 (Rotation)**: 旋轉矩陣 $R(\theta)$。
    $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$
