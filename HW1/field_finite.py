import random
from finite_field_element import FiniteFieldElement

# 若您有定義 Group base class 可以在此繼承，若無則依 Duck Typing 實作即可
class FiniteFieldAddGroup:
    """有限體加法群 (GF(p), +)"""
    def __init__(self, p):
        self.p = p
        self._identity = 0
    
    @property
    def identity(self):
        return self._identity

    def operation(self, a, b):
        return (a + b) % self.p

    def inverse(self, val):
        return (-val) % self.p

    def include(self, element):
        return isinstance(element, int) and 0 <= element < self.p

    def random_generate(self):
        return random.randint(0, self.p - 1)

class FiniteFieldMulGroup:
    """有限體乘法群 (GF(p)*, x)"""
    def __init__(self, p):
        self.p = p
        self._identity = 1

    @property
    def identity(self):
        return self._identity

    def operation(self, a, b):
        return (a * b) % self.p

    def inverse(self, val):
        # 使用 pow(val, -1, p) 計算模逆元
        if val % self.p == 0:
            raise ValueError("0 沒有乘法逆元")
        return pow(val, -1, self.p)

    def include(self, element):
        # 乘法群不包含 0
        return isinstance(element, int) and 1 <= element < self.p
        
    def random_generate(self):
        return random.randint(1, self.p - 1)

class FiniteField:
    """有限體主類別"""
    def __init__(self, p=11):
        self.p = p
        self.add_group = FiniteFieldAddGroup(p)
        self.mul_group = FiniteFieldMulGroup(p)

    def element(self, value):
        """工廠方法：產生一個有限體元素物件"""
        return FiniteFieldElement(self, value)

    def add(self, a, b):
        val = self.add_group.operation(a.value, b.value)
        return self.element(val)

    def subtract(self, a, b):
        val = self.add_group.operation(a.value, self.add_group.inverse(b.value))
        return self.element(val)
        
    def multiply(self, a, b):
        # 注意：multiply 處理的是 Element 物件
        if a.value == 0 or b.value == 0:
            return self.element(0)
        val = self.mul_group.operation(a.value, b.value)
        return self.element(val)
    
    def divide(self, a, b):
        if b.value == 0:
            raise ZeroDivisionError("Cannot divide by zero in Finite Field")
        if a.value == 0:
            return self.element(0)
        val = self.mul_group.operation(a.value, self.mul_group.inverse(b.value))
        return self.element(val)
