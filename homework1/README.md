# 基於奇異值分解 (SVD) 的影像壓縮演算法
# Image Compression via Singular Value Decomposition

**課程名稱：** [程式與數學]
**作者：** [張政榮/111310546]
**日期：** 2026/01/03

---

## 1. 專案動機 (Motivation)

在數位影像處理領域中，隨著解析度的提升，數據儲存與傳輸的成本也隨之增加。如何有效地減少影像數據量，同時保留肉眼可見的主要特徵，是數據科學中的核心課題。

本專案旨在探討 **線性代數 (Linear Algebra)** 中的 **奇異值分解 (Singular Value Decomposition, SVD)** 技術。雖然 JPEG 等成熟的壓縮標準已廣泛使用，但 SVD 提供了一個優雅的數學觀點，證明了我們可以透過矩陣分解與降維技術，從數學根本上提取影像特徵並實現數據壓縮。

## 2. 數學原理 (Mathematical Background)

數位影像在計算機科學中本質上是一個矩陣。對於一張解析度為 $m \times n$ 的灰階圖片，我們將其定義為矩陣 $A \in \mathbb{R}^{m \times n}$。

### 2.1 SVD 分解定理
根據線性代數理論，任意實數矩陣 $A$ 皆可分解為三個矩陣的乘積：

$$A = U \Sigma V^T$$

其中：
* **$U$ (Left Singular Vectors)**：$m \times m$ 的正交矩陣，其行向量稱為左奇異向量，代表影像在垂直方向的特徵基底。
* **$\Sigma$ (Singular Values)**：$m \times n$ 的對角矩陣，對角線元素 $\sigma_1, \sigma_2, \dots, \sigma_r$ 即為**奇異值**。
    * **特性**：$\sigma_1 \ge \sigma_2 \ge \dots \ge 0$ (遞減排列)。
    * **物理意義**：奇異值的大小對應於該特徵分量在影像中的「能量」或「資訊權重」。
* **$V^T$ (Right Singular Vectors)**：$n \times n$ 的正交矩陣，其列向量稱為右奇異向量，代表影像在水平方向的特徵基底。

### 2.2 低秩近似 (Low-Rank Approximation)
SVD 壓縮的核心原理在於**截斷 (Truncation)**。若我們僅保留前 $k$ 個最大的奇異值，則矩陣 $A$ 可被近似為秩為 $k$ 的矩陣 $A_k$：

$$A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$

**Eckart–Young–Mirsky 定理** 為此提供了理論保證：在 Frobenius 範數 (Frobenius Norm) 下，$A_k$ 是所有秩為 $k$ 的矩陣中，與原矩陣 $A$ 誤差最小的最佳近似：

$$\min_{\text{rank}(B)=k} \|A - B\|_F = \|A - A_k\|_F = \sqrt{\sum_{i=k+1}^{r} \sigma_i^2}$$

這意味著捨棄尾端的奇異值（通常對應影像的高頻雜訊或微小細節）所造成的失真是數學上最小的。

### 2.3 壓縮率估算 (Compression Ratio)
原始矩陣需儲存 $m \times n$ 個像素值。壓縮後只需儲存 $k$ 個奇異值、前 $k$ 個左奇異向量與前 $k$ 個右奇異向量。

$$\text{Compression Ratio} = \frac{\text{Compressed Size}}{\text{Original Size}} = \frac{k(m + n + 1)}{m \times n}$$

當 $k \ll \min(m, n)$ 時，可達到顯著的壓縮效果。

## 3. 實作流程 (Implementation)

本專案使用 Python 語言，結合 `NumPy` 進行高效矩陣運算，並使用 `Matplotlib` 進行結果視覺化。

### 核心演算法步驟
1.  **影像前處理**：讀取圖片並轉換為灰階矩陣 $A$。
2.  **矩陣分解**：
    * 呼叫 `numpy.linalg.svd(A, full_matrices=False)` 進行經濟型 SVD 分解。
    * *注意：NumPy 回傳的 `S` 為一維陣列，重建時需使用 `np.diag(S)` 轉換為對角矩陣。*
3.  **特徵截斷與重建**：
    * 設定保留特徵數 $k$。
    * 取出 $U$ 的前 $k$ 行、$S$ 的前 $k$ 項、$V^T$ 的前 $k$ 列。
    * 計算 $A_k = U_k \Sigma_k V_k^T$ 還原影像矩陣。

## 4. 實驗結果與分析 (Results)

### 4.1 奇異值能量分佈
![奇異值分佈圖](singular_values.png)
*(圖示說明：奇異值大小隨索引增加而急劇下降，顯示影像的主要資訊集中在前少數幾個特徵值上。)*

### 4.2 不同 k 值的重建效果
![壓縮結果對比圖](compression_result.png)

### 4.3 數據分析表
以 $512 \times 512$ 的測試圖片為例：

| 保留特徵數 (k) | 視覺品質描述 | 壓縮率 (估算) | 分析 |
| :--- | :--- | :--- | :--- |
| **5** | 極度模糊 | ~2.0% | 僅保留了影像的基礎光影結構，細節完全丟失。 |
| **20** | 可辨識但粗糙 | ~7.8% | 輪廓已清晰可見，但在邊緣處有明顯的吉布斯現象 (Gibbs Phenomenon) 或塊狀雜訊。 |
| **50** | 清晰且細緻 | ~19.6% | 肉眼難以分辨與原圖差異，且去除了部分高頻雜訊。 |
| **Original** | 原始畫質 | 100% | 基準對照組。 |

## 5. 結論與展望 (Conclusion)

1.  **理論驗證**：實驗結果證實了 SVD 的低秩近似性質，僅需保留前 10%-20% 的奇異值即可重建高品質影像。
2.  **去噪潛力**：由於影像雜訊通常表現為數值較小的奇異值，SVD 壓縮過程在本質上具有**影像去噪 (Denoising)** 的副作用。
3.  **未來工作**：
    * **彩色影像支援**：目前的實作僅針對單通道灰階圖。未來可將演算法擴展至 RGB 三通道，對每個顏色通道獨立進行 SVD 壓縮後再合併。
    * **區塊壓縮**：針對超高解析度影像，可先將影像切割為小區塊 (如 $8 \times 8$) 再分別進行 SVD，這類似於 JPEG 的運作邏輯，能進一步提升計算效率。

---

### 程式執行說明
請確保環境已安裝 `numpy`, `matplotlib`, `pillow` 套件，並在終端機執行：
```bash
python svd_compression.py
