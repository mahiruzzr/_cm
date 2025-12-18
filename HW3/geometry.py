import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"

    # 向量加法與減法
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    # 向量長度
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # 點的變換：平移
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    # 點的變換：縮放 (以原點為中心)
    def scale(self, sx, sy):
        self.x *= sx
        self.y *= sy

    # 點的變換：旋轉 (以原點為中心，逆時針)
    def rotate(self, angle_degrees):
        rad = math.radians(angle_degrees)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)
        new_x = self.x * cos_theta - self.y * sin_theta
        new_y = self.x * sin_theta + self.y * cos_theta
        self.x, self.y = new_x, new_y

class Line:
    # 使用一般式 Ax + By = C
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def __repr__(self):
        return f"Line({self.A}x + {self.B}y = {self.C})"

    # 給定兩點建立直線
    @classmethod
    def from_points(cls, p1, p2):
        A = p1.y - p2.y
        B = p2.x - p1.x
        C = A * p1.x + B * p1.y
        return cls(A, B, C)
    
    # 變換：線的變換通常是通過變換其構成的點來實現
    # 這裡簡化為重新定義，實際應用中會變換定義線的兩個點

class Circle:
    def __init__(self, center: Point, radius):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(Center={self.center}, r={self.radius})"

    # 圓的變換
    def translate(self, dx, dy):
        self.center.translate(dx, dy)

    def scale(self, s):
        # 圓通常只進行均勻縮放
        self.center.scale(s, s)
        self.radius *= s
        
    def rotate(self, angle):
        # 圓自轉不變，但圓心位置會繞原點旋轉
        self.center.rotate(angle)

class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = [p1, p2, p3]

    def __repr__(self):
        return f"Triangle({self.points[0]}, {self.points[1]}, {self.points[2]})"

    def translate(self, dx, dy):
        for p in self.points: p.translate(dx, dy)

    def scale(self, sx, sy):
        for p in self.points: p.scale(sx, sy)

    def rotate(self, angle):
        for p in self.points: p.rotate(angle)

# --- 計算幾何演算法 ---

def intersect_line_line(l1: Line, l2: Line):
    """ 使用克拉瑪公式 (Cramer's Rule) 計算兩直線交點 """
    det = l1.A * l2.B - l2.A * l1.B
    if abs(det) < 1e-9:
        return None # 平行或重合
    x = (l1.C * l2.B - l2.C * l1.B) / det
    y = (l1.A * l2.C - l2.A * l1.C) / det
    return Point(x, y)

def get_projection_point(line: Line, point: Point):
    """ 計算點到直線的垂足 (Projection) """
    # 幾何解法：垂足是過該點且垂直於原直線的線，與原直線的交點
    # 原直線法向量 (A, B)，垂線方向向量 (A, B)，垂線法向量 (-B, A)
    # 垂線方程式: -Bx + Ay = C_new
    perp_A = -line.B
    perp_B = line.A
    perp_C = perp_A * point.x + perp_B * point.y
    perp_line = Line(perp_A, perp_B, perp_C)
    return intersect_line_line(line, perp_line)

def intersect_line_circle(line: Line, circle: Circle):
    """ 計算直線與圓的交點 """
    # 1. 找出圓心到直線的垂足
    proj = get_projection_point(line, circle.center)
    
    # 2. 計算圓心到垂足的距離 d
    d_vec = proj - circle.center
    d = d_vec.length()

    if d > circle.radius:
        return [] # 不相交
    
    # 3. 計算垂足到交點的偏移量 t
    t = math.sqrt(circle.radius**2 - d**2)
    
    # 4. 找出直線的單位方向向量
    # 直線法向量 (A, B)，方向向量為 (B, -A) 或 (-B, A)
    len_n = math.sqrt(line.A**2 + line.B**2)
    dx = line.B / len_n
    dy = -line.A / len_n
    
    p1 = Point(proj.x + t * dx, proj.y + t * dy)
    p2 = Point(proj.x - t * dx, proj.y - t * dy)
    
    if d == circle.radius: return [p1] # 切點
    return [p1, p2]

def intersect_circle_circle(c1: Circle, c2: Circle):
    """ 計算兩圓交點 """
    d_vec = c2.center - c1.center
    d = d_vec.length()
    
    # 檢查是否分離、內含或重合
    if d > c1.radius + c2.radius or d < abs(c1.radius - c2.radius) or d == 0:
        return []

    # 兩圓相交的弦所在的直線（根軸 Radical Axis）
    # 推導過程：(x-x1)^2 + ... = r1^2 減去 (x-x2)^2 + ... = r2^2
    # 這會消去 x^2, y^2 得到一條直線方程式
    # 這裡我們用幾何法：
    a = (c1.radius**2 - c2.radius**2 + d**2) / (2 * d)
    h = math.sqrt(max(0, c1.radius**2 - a**2))
    
    # P2 = P1 + a * (P2 - P1) / d
    x2 = c1.center.x + a * (c2.center.x - c1.center.x) / d
    y2 = c1.center.y + a * (c2.center.y - c1.center.y) / d
    
    # 偏移量
    x3_1 = x2 + h * (c2.center.y - c1.center.y) / d
    y3_1 = y2 - h * (c2.center.x - c1.center.x) / d
    x3_2 = x2 - h * (c2.center.y - c1.center.y) / d
    y3_2 = y2 + h * (c2.center.x - c1.center.x) / d
    
    return [Point(x3_1, y3_1), Point(x3_2, y3_2)]

def distance(p1, p2):
    return (p1 - p2).length()

# --- 主程式驗證區 ---

print("=== 1. 兩直線交點 ===")
L1 = Line(1, -1, 0) # y = x
L2 = Line(1, 1, 10) # y = -x + 10
p_cross = intersect_line_line(L1, L2)
print(f"L1 與 L2 交點: {p_cross}") # 應為 (5, 5)

print("\n=== 2. 直線與圓交點 ===")
C1 = Circle(Point(0, 0), 5)
L3 = Line(0, 1, 3) # y = 3
p_lc = intersect_line_circle(L3, C1)
print(f"L3 與 C1 交點: {p_lc}") # 應為 (-4, 3) 和 (4, 3)

print("\n=== 3. 兩圓交點 ===")
C2 = Circle(Point(3, 0), 4) # 中心(3,0) 半徑4
p_cc = intersect_circle_circle(C1, C2)
print(f"C1 與 C2 交點: {p_cc}") 

print("\n=== 4. 畢氏定理驗證 ===")
# 給定直線 L: 3x + 4y = 0 和線外一點 P(5, 5)
L_test = Line(3, 4, 0)
P_out = Point(5, 5)
# 找出垂足 P_foot
P_foot = get_projection_point(L_test, P_out)
print(f"線外一點: {P_out}")
print(f"垂足: {P_foot}")

# 在直線上隨便找另一點 P_on_line (讓 x=4, 則 12+4y=0 => y=-3)
P_on_line = Point(4, -3) 
print(f"線上任一點: {P_on_line}")

# 計算三角形三邊長
a = distance(P_out, P_foot)       # 股1 (垂線長)
b = distance(P_foot, P_on_line)   # 股2 (線上點到垂足)
c = distance(P_out, P_on_line)    # 斜邊 (線外點到線上任一點)

print(f"a (垂距) = {a:.4f}")
print(f"b (底邊) = {b:.4f}")
print(f"c (斜邊) = {c:.4f}")
print(f"驗證: a^2 + b^2 = {a**2 + b**2:.4f}")
print(f"驗證: c^2       = {c**2:.4f}")
if abs((a**2 + b**2) - c**2) < 1e-9:
    print(">> 畢氏定理成立！")

print("\n=== 5. 幾何變換 (平移/旋轉/縮放) ===")
tri = Triangle(Point(0, 0), Point(1, 0), Point(0, 1))
print(f"原三角形: {tri}")
tri.translate(2, 2)
print(f"平移後(2,2): {tri}")
tri.scale(2, 2)
print(f"縮放後(2x): {tri}")
tri.rotate(90)
print(f"旋轉後(90度): {tri}")
