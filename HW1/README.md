# 有限體 (Finite Field) 數學原理與 Python 實作

本專案實作了代數學中的 **有限體 (Finite Field)**，具體來說是質數體 $GF(p)$。我們利用 Python 的物件導向特性，將抽象代數結構實體化，並驗證程式實作是否符合數學公理。

## 📂 檔案結構與功能

本專案由四個主要檔案組成，層次分明地對應不同的數學結構：

1.  **`group_axioms.py`**：定義並檢驗 **群 (Group)** 的數學公理。
2.  **`field_finite.py`**：實作有限體 $GF(p)$ 的核心邏輯（加法群 + 乘法群）。
3.  **`finite_field_element.py`**：實作 **元素 (Element)** 物件，透過運算子重載提供直觀的數學操作介面。
4.  **`field_axioms.py`**：整合測試，驗證上述實作是否符合 **體 (Field)** 的完整定義（特別是分配律）。

---

## 🧮 數學原理深度解析

### 1. 什麼是有限體 $GF(p)$？
有限體（亦稱 Galois Field）是一個包含有限個元素的集合，在此集合上定義了 **加法** 與 **乘法** 兩種運算。
本實作的數學基礎在於：**$GF(p)$ 與模 $p$ 的整數環 $\mathbb{Z}/p\mathbb{Z}$ 是同構的 (Isomorphic)**。

* **集合範圍**：$S = \{0, 1, 2, ..., p-1\}$
* **運算規則**：所有運算結果均取模 $p$ ($a \pmod p$)。
* **封閉性**：由於模運算的特性，運算結果保證永遠落在集合 $S$ 內，這在數學上是 **自動成立** 的，程式中的檢查僅是為了確保實作無誤。

### 2. 群論基礎 (`group_axioms.py`)
一個集合要成為「群」，必須符合特定公理。值得注意的是，對於模 $p$ 的運算，**結合律** 與 **封閉性** 源自整數性質，理論上必然成立；我們的隨機測試主要用於 **驗證程式邏輯的正確性**。

* **封閉性 (Closure)**：$\forall a, b \in G \Rightarrow a \cdot b \in G$。
* **結合律 (Associativity)**：$(a \cdot b) \cdot c = a \cdot (b \cdot c)$。
* **單位元素 (Identity Element)**：
    * 加法單位元為 $0$。
    * 乘法單位元為 $1$。
* **反元素 (Inverse Element)**：
    * 加法反元素：$-a \equiv p - a \pmod p$。
    * 乘法反元素：$a^{-1}$ 滿足 $a \cdot a^{-1} \equiv 1 \pmod p$。
* **交換律 (Commutativity)**：$a \cdot b = b \cdot a$。

### 3. 體的構成 (`field_finite.py`)
數學上，一個體 (Field) 是由兩個 **阿貝爾群 (Abelian Group)** 透過分配律交織而成的結構：

#### A. 加法群 $(GF(p), +)$
* 對應於整數模 $p$ 的加法群。
* 包含所有元素 $\{0, ..., p-1\}$。

#### B. 乘法群 $(GF(p)^\times, \times)$
* 嚴格來說是對應於 $(\mathbb{Z}/p\mathbb{Z})^\times$。
* 包含所有 **非零** 元素 $\{1, ..., p-1\}$。
* **乘法逆元實作**：
    程式中使用 Python 內建的 `pow(val, -1, p)`。其底層主要基於 **擴展歐幾里得演算法 (Extended Euclidean Algorithm)** 來高效求解 $ax + py = 1$ 中的 $x$，這保證了在 $p$ 為質數時必能找到逆元（這也符合費馬小定理的結論）。

### 4. 分配律：連接兩群的橋樑 (`field_axioms.py`)
體結構最關鍵的特徵在於乘法對加法具有 **分配律 (Distributivity)**：
$$a \times (b + c) = (a \times b) + (a \times c)$$

這是驗證程式架構正確性的最終關卡。若加法與乘法各自運作正常，但無法通過分配律測試，則表示這兩個運算並沒有正確地結合成一個「體」。


```bash
python field_axioms.py
