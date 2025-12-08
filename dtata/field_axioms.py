from group_axioms import check_commutative_group, NUM_TEST_CASES
from field_finite import FiniteField

def check_distributivity(f):
    """檢驗乘法對加法的分配律"""
    print(f"--- 檢驗分配律 ({NUM_TEST_CASES} 次) ---")
    for _ in range(NUM_TEST_CASES):
        # 從加法群取值 (包含 0)
        a_val = f.add_group.random_generate()
        b_val = f.add_group.random_generate()
        c_val = f.add_group.random_generate()
        
        # 轉換為 Element 物件以便使用重載運算子 (或者手動呼叫 operation)
        # 這裡我們使用底層 operation 來驗證數學公理
        
        # 左分配律: a * (b + c)
        b_plus_c = f.add_group.operation(b_val, c_val)
        lhs = f.multiply(f.element(a_val), f.element(b_plus_c)).value
        
        # (a * b) + (a * c)
        ab = f.multiply(f.element(a_val), f.element(b_val)).value
        ac = f.multiply(f.element(a_val), f.element(c_val)).value
        rhs = f.add_group.operation(ab, ac)
        
        assert lhs == rhs, f"Left distributivity failed"

        # 右分配律: (a + b) * c
        a_plus_b = f.add_group.operation(a_val, b_val)
        lhs = f.multiply(f.element(a_plus_b), f.element(c_val)).value
        
        # (a * c) + (b * c)
        ac = f.multiply(f.element(a_val), f.element(c_val)).value
        bc = f.multiply(f.element(b_val), f.element(c_val)).value
        rhs = f.add_group.operation(ac, bc)
        
        assert lhs == rhs, f"Right distributivity failed"
        
    print("  分配律驗證通過！")

def check_field_axioms(f):
    print(f"=== 開始檢驗有限體 GF({f.p}) ===")
    
    print("\n[1. 加法群檢驗]")
    check_commutative_group(f.add_group)
    
    print("\n[2. 乘法群檢驗 (排除0)]")
    check_commutative_group(f.mul_group)
    
    print("\n[3. 分配律檢驗]")
    check_distributivity(f)
    
    print("\n=== 所有公理檢驗成功！ ===")

if __name__ == "__main__":
    # 建立一個質數 p=31 的體
    p = 31
    F = FiniteField(p)
    
    # 1. 執行公理檢查
    check_field_axioms(F)
    
    # 2. 額外展示：使用物件導向寫法 (類似 rational_number.py 的用法)
    print("\n--- 程式物件使用範例 ---")
    a = F.element(10)
    b = F.element(25)
    print(f"a = {a}, b = {b}")
    print(f"a + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"驗證除法: (a/b)*b = {(a/b)*b}")
