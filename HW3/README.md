## 1. 直線的代數表示 (Line Representation)

### 為什麼不使用 $y = mx + b$？
在程式碼中，`Line` 類別使用**一般式 (General Form)**：
$$Ax + By = C$$

**邏輯原因：**
1.  **完備性**：斜截式 ($y=mx+b$) 無法表示垂直線（斜率 $m$ 為無窮大），會導致程式出現 `ZeroDivisionError`。一般式可以表示平面上任何直線。
2.  **向量意義**：係數 $(A, B)$ 剛好組成了直線的**法向量 (Normal Vector)** $\vec{n} = (A, B)$，這對於計算垂直線非常方便。

---

## 2. 兩直線交點：克拉瑪公式 (Cramer's Rule)

程式中的 `intersect_line_line` 函式並非使用代換法求解，而是使用**線性代數**的方法。

### 數學推導
尋找兩直線 $L_1, L_2$ 的交點，等同於解二元一次聯立方程式：
$$
\begin{cases}
A_1x + B_1y = C_1 \\
A_2x + B_2y = C_2
\end{cases}
$$

將其寫成矩陣形式 $M\mathbf{x} = \mathbf{b}$：
$$
\begin{bmatrix} A_1 & B_1 \\ A_2 & B_2 \end{bmatrix} 
\begin{bmatrix} x \\ y \end{bmatrix} = 
\begin{bmatrix} C_1 \\ C_2 \end{bmatrix}
$$

根據**克拉瑪公式**，解 $(x, y)$ 為：
$$
x = \frac{\Delta_x}{\Delta}, \quad y = \frac{\Delta_y}{\Delta}
$$

其中行列式 (Determinant) 為：
* $\Delta = A_1B_2 - A_2B_1$ (程式碼中的 `det`)
* $\Delta_x = C_1B_2 - C_2B_1$
* $\Delta_y = A_1C_2 - A_2C_1$

**程式邏輯：**
若 $\Delta = 0$，表示矩陣不可逆，幾何意義為**兩直線平行**（無交點）。

---

## 3. 點到直線的垂足 (Projection & Perpendicularity)

在 `get_projection_point` 中，我們需要找到從點 $P$ 到直線 $L$ 的垂直線。

### 數學推導
若原直線 $L$ 為 $Ax + By = C$，其法向量為 $\vec{n} = (A, B)$。
垂直線 $L_{\perp}$ 必須與 $L$ 垂直，這意味著 $L_{\perp}$ 的法向量 $\vec{n}_{\perp}$ 必須與 $\vec{n}$ 垂直。

根據向量內積性質 $\vec{u} \cdot \vec{v} = 0$，若 $\vec{n} = (A, B)$，則 $\vec{n}_{\perp} = (-B, A)$ 是一個垂直向量。

因此，垂線方程式形式必為：
$$-Bx + Ay = K$$
常數 $K$ 可由帶入點 $P$ 的座標求得。

---

## 4. 幾何變換 (Geometric Transformations)

物件的移動、旋轉與縮放，本質上是**函數映射**。

### A. 平移 (Translation)
平移是非線性變換（在二維向量空間中），簡單定義為向量加法：
$$(x', y') = (x + dx, y + dy)$$

### B. 縮放 (Scaling)
以原點為中心的縮放是線性變換：
$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = 
\begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix} 
\begin{bmatrix} x \\ y \end{bmatrix}
$$

### C. 旋轉 (Rotation)
這是線性代數中最核心的應用之一。程式中的 `rotate` 方法實作了**旋轉矩陣**。
將點 $(x, y)$ 逆時針旋轉 $\theta$ 角度：

$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = 
\underbrace{\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}}_{\text{Rotation Matrix } R}
\begin{bmatrix} x \\ y \end{bmatrix}
$$

**程式實作細節：**
```python
new_x = self.x * cos_theta - self.y * sin_theta
new_y = self.x * sin_theta + self.y * cos_theta
