class FiniteFieldElement:
    """
    表示有限體 GF(p) 中的一個元素。
    重載了運算子，讓運算會自動呼叫所屬 Field 的邏輯。
    """
    def __init__(self, field, value):
        self.field = field
        if not isinstance(value, int):
            raise TypeError("有限體元素的初始值必須是整數")
        # 確保數值在 [0, p-1]
        self.value = value % field.p

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, FiniteFieldElement):
            return self.field.p == other.field.p and self.value == other.value
        if isinstance(other, int):
            return self.value == (other % self.field.p)
        return False

    def _check_same_field(self, other):
        if self.field.p != other.field.p:
            raise ValueError("無法對不同模數的有限體元素進行運算")

    # --- 加法 ---
    def __add__(self, other):
        if isinstance(other, FiniteFieldElement):
            self._check_same_field(other)
            return self.field.add(self, other)
        elif isinstance(other, int):
            return self.field.add(self, self.field.element(other))
        return NotImplemented

    def __radd__(self, other):
        return self + other

    # --- 減法 ---
    def __sub__(self, other):
        if isinstance(other, FiniteFieldElement):
            self._check_same_field(other)
            return self.field.subtract(self, other)
        elif isinstance(other, int):
            return self.field.subtract(self, self.field.element(other))
        return NotImplemented

    def __rsub__(self, other):
        return self.field.subtract(self.field.element(other), self)

    # --- 乘法 ---
    def __mul__(self, other):
        if isinstance(other, FiniteFieldElement):
            self._check_same_field(other)
            return self.field.multiply(self, other)
        elif isinstance(other, int):
            return self.field.multiply(self, self.field.element(other))
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    # --- 除法 ---
    def __truediv__(self, other):
        if isinstance(other, FiniteFieldElement):
            self._check_same_field(other)
            return self.field.divide(self, other)
        elif isinstance(other, int):
            return self.field.divide(self, self.field.element(other))
        return NotImplemented

    def __rtruediv__(self, other):
        return self.field.divide(self.field.element(other), self)
