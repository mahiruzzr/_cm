import numpy as np

def info_theory_metrics():
    print("\n--- 習題 3 & 4: 熵、交叉熵、KL散度 ---")

    # 為了避免 log(0) 錯誤，我們加上一個極小值 epsilon
    epsilon = 1e-10

    def entropy(p):
        """熵 H(P)"""
        p = np.array(p)
        return -np.sum(p * np.log2(p + epsilon))

    def cross_entropy(p, q):
        """交叉熵 H(P, Q)"""
        p = np.array(p)
        q = np.array(q)
        return -np.sum(p * np.log2(q + epsilon))

    def kl_divergence(p, q):
        """KL 散度 D_KL(P || Q)"""
        p = np.array(p)
        q = np.array(q)
        # 公式: sum(p(x) * log(p(x)/q(x)))
        return np.sum(p * np.log2((p + epsilon) / (q + epsilon)))

    # 設定兩個機率分佈
    p = np.array([0.8, 0.1, 0.1]) # 真實分佈
    q = np.array([0.2, 0.4, 0.4]) # 預測分佈 (與 p 不同)

    h_p = entropy(p)
    h_pq = cross_entropy(p, q)
    kl = kl_divergence(p, q)

    print(f"分佈 P: {p}")
    print(f"分佈 Q: {q}")
    print(f"1. 熵 (Entropy) H(P): {h_p:.4f}")
    print(f"2. 交叉熵 (Cross Entropy) H(P, Q): {h_pq:.4f}")
    print(f"3. KL 散度 (KL Divergence): {kl:.4f}")
    
    # 驗證性質: H(P,Q) = H(P) + D_KL(P||Q)
    print(f"   驗證 H(P) + KL: {h_p + kl:.4f} (應等於 H(P,Q))")

    # 習題 4 驗證
    print("\n--- 習題 4: 驗證 Cross Entropy 大小關係 ---")
    h_pp = cross_entropy(p, p) # 這其實就等於 Entropy(p)
    
    print(f"H(p, p) = {h_pp:.4f}")
    print(f"H(p, q) = {h_pq:.4f}")
    
    if h_pq > h_pp:
        print("結果: H(p, q) > H(p, p)")
        print("說明: 當 q != p 時，交叉熵通常會大於本身的熵 (Gibbs 不等式)。")
        print("注意: 題目敘述 'H(p,p) > H(p,q)' 在數學上通常是不成立的，除非題目有特殊定義。")
    else:
        print("結果符合題目敘述 (但在標準定義下極少見)。")

info_theory_metrics()
