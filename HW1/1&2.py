import math

def probability_demo():
    print("--- 習題 1 & 2: 機率與對數機率 ---")
    p = 0.5
    n = 10000
    
    # 習題 1: 直接計算 p^n
    # 在標準浮點數中，0.5 的 10000 次方會因為數值過小而產生 Underflow (下溢)，直接變成 0.0
    direct_prob = p ** n
    print(f"1. 直接計算 0.5^{n}: {direct_prob}")
    print("   (注意：結果為 0.0 是因為數值太小，超出了電腦浮點數的精度範圍)\n")

    # 習題 2: 使用 Log 計算 log(p^n) = n * log(p)
    # 這能將極小的機率轉換為可處理的負數數值
    # 資訊理論通常使用以 2 為底 (bits)
    log_prob_base2 = n * math.log2(p)
    
    # 如果要使用以 10 為底
    log_prob_base10 = n * math.log10(p)

    print(f"2. 使用 Log 計算 log(0.5^{n}):")
    print(f"   以 2 為底 (bits): {log_prob_base2}")
    print(f"   以 10 為底: {log_prob_base10}")
    print(f"   (這代表機率約為 10 的 {log_prob_base10:.2f} 次方)")

probability_demo()
