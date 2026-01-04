# 🖼️ 基於奇異值分解 (SVD) 的影像壓縮實作
### Image Compression via Singular Value Decomposition

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/Library-NumPy-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Library-Matplotlib-orange?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **課程名稱：** [程式與數學]  
> **作者：** [張政榮/111310546]  
> **日期：** 2026/01/03

---

## 📖 目錄 (Table of Contents)
1. [動機 (Motivation)](#1-動機-motivation)
2. [數學原理 (Mathematical Background)](#2-數學原理-mathematical-background)
3. [專案結構與實作 (Implementation)](#3-專案結構與實作-implementation)
4. [實作結果 (Results)](#4-實作結果-results)
5. [結論 (Conclusion)](#5-結論-conclusion)
6. [執行說明](#-執行程式)

---

## 1. 🎯 動機 (Motivation)

在數位時代，高解析度的影像佔據了大量的儲存空間與傳輸頻寬。如何有效地減少影像數據量，同時保留肉眼可見的主要特徵，是資訊工程與數據科學的重要課題。

雖然現代有許多成熟的壓縮格式（如 JPEG, PNG），但其背後的數學原理往往被忽視。本專案旨在探討 **線性代數 (Linear Algebra)** 中的 **奇異值分解 (Singular Value Decomposition, SVD)** 技術，證明數學理論並非紙上談兵，而是能實際應用於「降維」與「特徵提取」。

> 💡 **核心概念**：透過 SVD，我們可以將一張複雜的圖片矩陣拆解，並透過捨棄次要的奇異值來達到壓縮效果。

---

## 2. 📐 數學原理 (Mathematical Background)

數位影像在電腦中本質上是一個矩陣（Matrix）。對於一張 $m \times n$ 的灰階圖片，我們可以將其視為矩陣 $A$。

### 2.1 SVD 定義
根據線性代數理論，任意實數矩陣 $A$ 皆可分解為三個矩陣的乘積：

$$A = U \Sigma V^T$$

| 符號 | 名稱 | 維度 | 物理意義 |
| :---: | :--- | :--- | :--- |
| **$U$** | Left Singular Vectors | $m \times m$ | 圖片在**垂直方向**的特徵基底 (正交矩陣) |
| **$\Sigma$** | Singular Values | $m \times n$ | 對角線元素 $\sigma_i$ 代表特徵的**能量**或**重要程度** ($\sigma_1 \ge \sigma_2 \ge \dots \ge 0$) |
| **$V^T$** | Right Singular Vectors | $n \times n$ | 圖片在**水平方向**的特徵基底 (正交矩陣) |

### 2.2 低秩近似 (Low-Rank Approximation)
SVD 的強大之處在於我們可以利用**截斷 (Truncation)** 來逼近原始矩陣。若我們只保留前 $k$ 個最大的奇異值，則矩陣 $A$ 可以被近似為 $A_k$：

$$A_k = \sum_{i=1}^{k} \sigma_i u_i v_i^T$$

由於 $\sigma$ 的數值下降得非常快，後面的項（細節與雜訊）對影像的貢獻極小。因此，我們可以使用遠小於原始像素數量的數據來重建影像，這就是 SVD 壓縮的核心原理。

---

## 3. 💻 專案結構與實作 (Implementation)

本專案使用 Python 語言，結合 `NumPy` 進行矩陣運算與 `Matplotlib` 進行視覺化。

### 📂 檔案說明

```text
Project/
├── svd_compression.py    # 主要程式碼：SVD 分解與圖片重建邏輯
├── README.md             # 專案報告與說明文件
└── test_image.jpg        # 測試用的原始圖片
