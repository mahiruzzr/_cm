import numpy as np
from scipy.linalg import lu, svd, eig

# --- 修改處：安全匯入 Matplotlib ---
try:
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("注意：未檢測到 matplotlib，將跳過繪圖功能，但數值計算仍可執行。\n")
# ---------------------------------

np.set_printoptions(precision=4, suppress=True)

# 1. 遞迴計算行列式
def recursive_det(matrix):
    n = len(matrix)
    if n == 1: return matrix[0][0]
    if n == 2: return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = 0
    for c in range(n):
        sub_matrix = np.delete(np.delete(matrix, 0, axis=0), c, axis=1)
        sign = (-1) ** c
        det += sign * matrix[0][c] * recursive_det(sub_matrix)
    return det

# 2. LU 分解算行列式
def det_via_lu(matrix):
    P, L, U = lu(matrix)
    det_P = np.linalg.det(P)
    det_L = np.prod(np.diag(L))
    det_U = np.prod(np.diag(U))
    return det_P * det_L * det_U

# 4. 用特徵值分解做 SVD (A = U Σ V^T)
def manual_svd_via_eigen(A):
    ATA = A.T @ A
    evals, evecs = np.linalg.eigh(ATA)
    
    # 排序 (大到小)
    idx = np.argsort(evals)[::-1]
    evals = evals[idx]
    V = evecs[:, idx]
    
    # 算奇異值 (過濾負值誤差)
    singular_values = np.sqrt(np.maximum(evals, 0))
    
    # 算 U
    r = np.sum(singular_values > 1e-10)
    U = np.zeros((A.shape[0], r))
    for i in range(r):
        U[:, i] = (A @ V[:, i]) / singular_values[i]
        
    return U, np.diag(singular_values[:r]), V.T

# 5. PCA 主成分分析
def simple_pca(data, n_components=2):
    mean_vec = np.mean(data, axis=0)
    centered = data - mean_vec
    cov = np.cov(centered, rowvar=False)
    evals, evecs = np.linalg.eigh(cov)
    
    idx = np.argsort(evals)[::-1]
    top_vecs = evecs[:, idx][:, :n_components]
    
    return centered @ top_vecs, top_vecs

# --- 主程式 ---
if __name__ == "__main__":
    A = np.array([[4., 12., -16.], [12., 37., -43.], [-16., -43., 98.]])
    print(f"原始矩陣 A:\n{A}\n")

    # 任務 1 & 2
    print(f"1. 遞迴行列式: {recursive_det(A):.4f}")
    print(f"2. LU 行列式:  {det_via_lu(A):.4f} (驗證: {np.linalg.det(A):.4f})\n")

    # 任務 3: 驗證還原
    print("3. 驗證還原:")
    P, L, U = lu(A)
    print(f"   LU 還原:    {np.allclose(A, P @ L @ U)}")
    
    vals, vecs = np.linalg.eig(A)
    A_eig = vecs @ np.diag(vals) @ np.linalg.inv(vecs)
    print(f"   Eigen 還原: {np.allclose(A, A_eig.real)}")
    
    U_s, S_s, Vt_s = svd(A)
    S_mat = np.zeros_like(A)
    np.fill_diagonal(S_mat, S_s)
    print(f"   SVD 還原:   {np.allclose(A, U_s @ S_mat @ Vt_s)}\n")

    # 任務 4: 手算 SVD
    B = np.array([[3., 2., 2.], [2., 3., -2.]])
    my_U, my_S, my_Vt = manual_svd_via_eigen(B)
    print(f"4. 手算 SVD 還原矩陣 B: {np.allclose(B, my_U @ my_S @ my_Vt)}")
    print(f"   奇異值: {np.diag(my_S)}")

    # 任務 5: PCA
    print("\n5. PCA 測試:")
    data = np.random.rand(5, 3)
    res, comps = simple_pca(data, 2)
    print(f"   降維後形狀: {res.shape}")
    print(f"   主成分向量:\n{comps}")
