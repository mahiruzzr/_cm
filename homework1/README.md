# 基於奇異值分解 (SVD) 的影像壓縮
# Image Compression via Singular Value Decomposition

**課程名稱：** [程式與數學]
**作者：** [張政榮/111310546]
**日期：** 2026/01/03

---

## 1. 動機 (Motivation)

在數位時代，高解析度的影像佔據了大量的儲存空間與傳輸頻寬。如何有效地減少影像數據量，同時保留肉眼可見的主要特徵，是資訊工程與數據科學的重要課題。

雖然現代有許多成熟的壓縮格式（如 JPEG, PNG），但本專案旨在探討 **線性代數 (Linear Algebra)** 中的 **奇異值分解 (Singular Value Decomposition, SVD)** 技術，證明數學理論能實際應用於「降維」與「特徵提取」。透過 SVD，我們可以將一張複雜的圖片矩陣拆解，透過捨棄次要的奇異值來達到壓縮效果，這也是許多機器學習降維演算法（如 PCA）的基礎。

## 2. 數學原理 (Mathematical Background)

數位影像在電腦中本質上是一個矩陣。對於一張 $m \times n$ 的灰階圖片，我們視其為矩陣 $A$。

### 2.1 SVD 定義
根據線性代數理論，任意實數矩陣 $A$ 皆可分解為三個矩陣的乘積：

$$A = U \Sigma V^T$$

其中：
* **$U$ (Left Singular Vectors)**：$m \times m$ 正交矩陣，代表垂直方向的特徵基底。
* **$\Sigma$ (Singular Values)**：$m \times n$ 對角矩陣，對角線元素 $\sigma_1, \sigma_2, \dots, \sigma_r$ 為**奇異值**。
    * 特性：$\sigma_1 \ge \sigma_2 \ge \dots \ge 0$ (遞減排列)。
    * 物理意義：奇異值越大，代表該特徵對圖片的「能量」或「資訊量」貢獻越大。
* **$V^T$ (Right Singular Vectors)**：$n \times n$ 正交矩陣，代表水平方向的特徵基底。

### 2.2 低秩近似與 Eckart–Young 定理
SVD 的核心應用在於**低秩近似 (Low-Rank Approximation)**。若我們只保留前 $k$ 個最大的奇異值，將其餘視為 0，則可得到近似矩陣 $A_k$：

$$A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$

**理論保證：**
根據 **Eckart–Young–Mirsky 定理**，在 Frobenius 範數 (Frobenius Norm) 下，$A_k$ 是所有秩為 $k$ 的矩陣中，與原矩陣 $A$ 誤差最小的最佳近似：
$$\min_{\text{rank}(B)=k} \|A - B\|_F = \|A - A_k\|_F = \sqrt{\sum_{i=k+1}^{r} \sigma_i^2}$$
這保證了我們截斷尾端的奇異值後，所保留的是圖片中最重要的資訊。

### 2.3 壓縮率估算
原始矩陣需要儲存 $m \times n$ 個像素。SVD 壓縮後（保留 $k$ 個特徵），我們只需儲存 $U$ 的前 $k$ 行、$V^T$ 的前 $k$ 列以及 $k$ 個奇異值。壓縮率公式如下：

$$\text{Compression Ratio} = \frac{\text{Compressed Size}}{\text{Original Size}} = \frac{k(m + n + 1)}{m \times n}$$

當 $k \ll \min(m, n)$ 時，可以達到顯著的壓縮效果。

## 3. 專案結構與實作 (Implementation)

本專案使用 Python (`NumPy`, `Matplotlib`) 實作。

### 核心演算法流程
1.  **讀取圖片**：將圖片轉換為灰階矩陣 $A$。
2.  **SVD 分解**：
    * 使用 `numpy.linalg.svd(A, full_matrices=False)` 進行經濟型分解。
    * *注意：NumPy 回傳的 `S` 為一維向量，運算時需使用 `np.diag(S)` 轉為對角矩陣。*
3.  **奇異值截斷**：選定 $k$ 值，僅保留前 $k$ 個 $u_i, \sigma_i, v_i^T$。
4.  **矩陣重建**：計算 $A_k = U_k \Sigma_k V_k^T$ 還原影像。

## 4. 實作結果 (Results)

### 4.1 奇異值分佈分析
![奇異值分佈圖](singular_values.png)
上圖 (Log Scale) 顯示奇異值數值下降極快，大部分能量集中在前幾項，後段數值極小（通常對應影像雜訊），這證實了 SVD 壓縮的可行性。

### 4.2 壓縮效果視覺化
我們測試了不同 $k$ 值的重建效果：

![壓縮結果對比圖](compression_result.png)

### 4.3 數據分析
以 $512 \times 512$ 的測試圖片為例：

| 保留特徵數 (k) | 視覺品質 | 壓縮率 (公式估算) | 說明 |
| :--- | :--- | :--- | :--- |
| **5** | 模糊/僅輪廓 | ~2.0% | 資訊量不足，僅剩光影結構。 |
| **20** | 可辨識/有雜訊 | ~7.8% | 輪廓成形，但有明顯塊狀感。 |
| **50** | 清晰/細節完整 | ~19.6% | 肉眼難以分辨差異，移除高頻雜訊。 |
| **Original** | 原始畫質 | 100% | 基準對照。 |

## 5. 結論與展望 (Conclusion)

1.  **理論驗證**：實作結果吻合 Eckart–Young 定理，只需保留前 10%-20% 的奇異值 ($k=50$) 即可還原高品質影像。
2.  **去噪應用**：由於影像雜訊通常對應於數值極小的奇異值，SVD 壓縮過程（捨棄尾端奇異值）自然具備**去噪 (Denoising)** 的效果。
3.  **彩色影像擴展**：目前的實作針對灰階圖片。對於 RGB 彩色圖片，可將 R、G、B 三個通道視為獨立矩陣，分別執行 SVD 壓縮後再合併，即可達到全彩壓縮效果。

---

### 如何執行程式
請確保環境安裝 `numpy`, `matplotlib`, `pillow`，並執行：
```bash
python svd_compression.py
