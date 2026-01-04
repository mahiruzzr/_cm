# 常係數齊次線性微分方程求解器 (ODE Solver)

本專案實作了一個 Python 程式，用於求解 **常係數齊次線性普通微分方程 (Linear Homogeneous ODEs with Constant Coefficients)** 的通解。程式結合了符號邏輯與數值演算法，能自動處理實數根、複數根及高階重根的情況。

## 📐 數學原理

### 1. 問題定義
本程式旨在解決如下形式的 $n$ 階微分方程：

$$a_n y^{(n)} + a_{n-1} y^{(n-1)} + \dots + a_1 y' + a_0 y = 0$$

其中 $a_i$ 為實數常數，且 $a_n \neq 0$。

### 2. 特徵方程式 (Characteristic Equation)
基於線性算子的特性，我們尋找形如 $y = e^{rx}$ 的指數解。代入原方程後可得一元 $n$ 次多項式：

$$a_n r^n + a_{n-1} r^{n-1} + \dots + a_1 r + a_0 = 0$$

根據代數基本定理，此 $n$ 次多項式在複數域中恰有 **$n$ 個根（計入重數）**。這些根 $r_1, r_2, \dots, r_n$ 決定了微分方程解的基底函數。

### 3. 通解的構成 (General Solution)
微分方程的通解是其解空間基底的 **線性組合 (Linear Combination)**。這意味著我們找到的 $n$ 個線性獨立解 $y_1, y_2, \dots, y_n$，可以組合成：

$$y(x) = C_1 y_1(x) + C_2 y_2(x) + \dots + C_n y_n(x)$$

其中 $C_i$ 為待定常數，由初始條件 (Initial Conditions) 決定。

---

## ⚙️ 基底建構規則

程式碼依據特徵根 $r$ 的性質，自動選擇對應的基底函數：

### Case 1: 實數相異根 (Real Distinct Roots)
若 $r$ 為實數且不重複，對應的基底為：
$$e^{rx}$$

### Case 2: 實數重根 (Real Repeated Roots)
若實數根 $r$ 重複出現 $m$ 次（重數為 $m$），為了保證解的 **線性獨立性**，需依序乘上 $x$ 的冪次。對應的 $m$ 個基底為：
$$e^{rx}, \quad x e^{rx}, \quad x^2 e^{rx}, \quad \dots, \quad x^{m-1} e^{rx}$$

### Case 3: 複數共軛根 (Complex Conjugate Roots)
若出現複數根 $r = \alpha \pm i\beta$（係數為實數時必成對出現）。利用 **歐拉公式 (Euler's Formula)** 將複數指數形式轉換為實數三角函數形式：
$$e^{\alpha x} \cos(\beta x) \quad \text{與} \quad e^{\alpha x} \sin(\beta x)$$

#### 複數重根的情況
若一對共軛複數 $r = \alpha \pm i\beta$ 的重數為 $m$，則需結合乘冪規則。對應的 $2m$ 個基底項為 ($k = 0, \dots, m-1$)：
$$x^k e^{\alpha x} \cos(\beta x) \quad \text{與} \quad x^k e^{\alpha x} \sin(\beta x)$$

---

## 💻 演算法實作細節：數值穩定性

由於電腦使用浮點數運算，本程式包含特殊的數值處理邏輯以確保結果正確：

### 1. 數值求根與誤差
使用 `numpy.roots` 計算多項式的根。由於這是數值逼近算法，會產生微小的浮點數誤差（例如理論值 `2.0` 可能算出 `1.99999999`）。

### 2. 容差分組 (Tolerance Grouping)
為了解決誤差導致「重根被誤判為相異根」的問題，引入容差 ($\epsilon \approx 10^{-7}$) 機制：
* **重根判定**：若 $|r_i - r_j| < \epsilon$，則視為同一個根，並累加重數。
* **虛部濾波**：若複數根的虛部 $|\text{Imag}(r)| < \epsilon$，強制視為實數根，避免輸出如 $\cos(10^{-15}x)$ 的數值雜訊。

### 3. 共軛去重
程式會自動偵測共軛對 $(\alpha \pm i\beta)$，並只處理其中一個（通常取 $\beta > 0$），一次生成 $\cos$ 與 $\sin$ 兩項，避免基底重複。

---

## 🚀 範例輸出

針對方程 $y''' - 6y'' + 12y' - 8y = 0$，特徵方程為 $(r-2)^3 = 0$。

程式輸出：
```text
y(x) = C_1e^(2x) + C_2xe^(2x) + C_3x^2e^(2x)
