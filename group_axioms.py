import random

NUM_TEST_CASES = 100

# 1. 封閉性 (Closure)
def check_closure(g):
    for _ in range(NUM_TEST_CASES):
        a = g.random_generate()
        b = g.random_generate()
        # 這裡假設 g.include 檢查的是「值」是否合法
        result = g.operation(a, b)
        assert g.include(result), f"Closure failed: {a} op {b} = {result} is not in G"

# 2. 結合性 (Associativity)
def check_associativity(g):
    for _ in range(NUM_TEST_CASES):
        a = g.random_generate()
        b = g.random_generate()
        c = g.random_generate()
        assert g.operation(g.operation(a, b), c) == g.operation(a, g.operation(b, c)), \
            f"Associativity failed: ({a} op {b}) op {c} != {a} op ({b} op {c})"

# 3. 單位元素 (Identity Element)
def check_identity_element(g):
    e = g.identity
    for _ in range(NUM_TEST_CASES):
        a = g.random_generate()
        # 左單位元素
        assert g.operation(e, a) == a, \
            f"Left identity failed: {e} op {a} != {a}"
        # 右單位元素
        assert g.operation(a, e) == a, \
            f"Right identity failed: {a} op {e} != {a}"  # 修正了這裡的變數名稱

# 4. 反元素 (Inverse Element)
def check_inverse_element(g):
    e = g.identity
    for _ in range(NUM_TEST_CASES):
        a = g.random_generate()
        
        a_inverse = g.inverse(a)

        # 檢查反元素是否也在集合 G 中
        assert g.include(a_inverse), f"Inverse {a_inverse} for {a} is not in G"

        # 檢查左反元素
        res_left = g.operation(a_inverse, a)
        assert res_left == e, \
            f"Left inverse failed: {a_inverse} op {a} = {res_left} != {e}"
            
        # 檢查右反元素
        res_right = g.operation(a, a_inverse)
        assert res_right == e, \
            f"Right inverse failed: {a} op {a_inverse} = {res_right} != {e}"

# 5. 交換性 (Commutativity)
def check_commutativity(g):
    for _ in range(NUM_TEST_CASES):
        a = g.random_generate()
        b = g.random_generate()
        assert g.operation(a, b) == g.operation(b, a), \
            f"Commutativity failed: {a} op {b} != {b} op {a}"

def check_group_axioms(g):
    """檢查一般群公理"""
    check_closure(g)
    check_associativity(g)
    check_identity_element(g)
    check_inverse_element(g)
    print(f"  {type(g).__name__}: 一般群公理通過！")

def check_commutative_group(g):
    """檢查交換群公理"""
    check_closure(g)
    check_associativity(g)
    check_identity_element(g)
    check_inverse_element(g)
    check_commutativity(g)
    print(f"  {type(g).__name__}: 交換群公理全部通過！")
