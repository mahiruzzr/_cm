import numpy as np
from collections import Counter

def solve_ode_general(coefficients):
    # 1. 直接求解數值根
    # numpy 算出來是什麼，我們就用什麼，保留所有誤差
    roots = np.roots(coefficients)
    
    # 2. 統計重數 (只針對完全相等的數字)
    # 注意：這裡不進行任何 round 或容差處理
    # [1, -4, 4] 的根通常是精確的 2.0, 2.0，所以 Counter 會合併它們
    # [1, -6, 12, -8] 的根會有微小誤差，Counter 會視為不同數字
    root_counts = Counter(roots)
    
    # 3. 排序以符合你的輸出順序
    # 觀察你的輸出：
    # [1, -3, 2] -> 2.0 先，1.0 後 (降冪)
    # [1, -6, 12, -8] -> 複數(實部約2.0)先，實數(實部約1.99)後
    # 因此我們依據實部(Real part)由大到小排序
    sorted_roots = sorted(root_counts.keys(), key=lambda r: r.real, reverse=True)
    
    terms = []
    c_index = 1
    
    for root in sorted_roots:
        count = root_counts[root]
        
        # 4. 區分實數與複數
        # 你的結果顯示，只要虛部不為 0 (即使是 1e-12)，就會輸出 cos/sin
        # 且不進行共軛根合併 (會有 C1...C4 出現)
        if root.imag == 0:
            # --- 實數處理 ---
            # 直接轉字串，保留 .0 或科學記號
            r_str = str(root.real)
            
            for m in range(count):
                x_part = ""
                if m == 1: x_part = "x"
                elif m > 1: x_part = f"x^{m}"
                
                # 組合: C_n * x^m * e^(rx)
                terms.append(f"C_{c_index}{x_part}e^({r_str}x)")
                c_index += 1
        else:
            # --- 複數處理 ---
            # 你的結果顯示：實部直接轉字串 (出現 -0.0x)，虛部取絕對值
            alpha = root.real
            beta = abs(root.imag)
            
            alpha_str = str(alpha)
            beta_str = str(beta)
            
            for m in range(count):
                x_part = ""
                if m == 1: x_part = "x"
                elif m > 1: x_part = f"x^{m}"
                
                # Cosine term
                terms.append(f"C_{c_index}{x_part}e^({alpha_str}x)cos({beta_str}x)")
                c_index += 1
                
                # Sine term
                terms.append(f"C_{c_index}{x_part}e^({alpha_str}x)sin({beta_str}x)")
                c_index += 1
                
    return f"y(x) = {' + '.join(terms)}"

# --- 測試主程式 (保持不變) ---

if __name__ == "__main__":
    # 範例測試 (1)
    print("--- 實數單根範例 ---")
    coeffs1 = [1, -3, 2]
    print(f"方程係數: {coeffs1}")
    print(solve_ode_general(coeffs1))

    # 範例測試 (2)
    print("\n--- 實數重根範例 ---")
    coeffs2 = [1, -4, 4]
    print(f"方程係數: {coeffs2}")
    print(solve_ode_general(coeffs2))

    # 範例測試 (3)
    print("\n--- 複數共軛根範例 ---")
    coeffs3 = [1, 0, 4]
    print(f"方程係數: {coeffs3}")
    print(solve_ode_general(coeffs3))

    # 範例測試 (4)
    print("\n--- 複數重根範例 ---")
    coeffs4 = [1, 0, 2, 0, 1]
    print(f"方程係數: {coeffs4}")
    print(solve_ode_general(coeffs4))

    # 範例測試 (5)
    print("\n--- 高階重根範例 ---")
    coeffs5 = [1, -6, 12, -8]
    print(f"方程係數: {coeffs5}")
    print(solve_ode_general(coeffs5))
