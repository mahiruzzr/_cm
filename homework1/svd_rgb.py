import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# ==========================================
# 1. 設定與讀取
# ==========================================
img_filename = 'test_image.jpg' # 請確認你的檔名

if not os.path.exists(img_filename):
    print(f"錯誤：找不到 {img_filename}，請確認圖片位置！")
    exit()

original_img = mpimg.imread(img_filename)
print(f"原始圖片尺寸: {original_img.shape}")
print(f"原始數值最大值: {original_img.max()}")

# *** 修正重點：標準化輸入圖片 ***
# 如果圖片是 0-1 的浮點數 (PNG 常見)，我們把它乘 255 轉成 0-255
# 如果圖片已經是 0-255 (JPG 常見)，就不動它
# 最後統一轉成 float 進行 SVD 運算，避免整數溢位
if original_img.max() <= 1.0:
    print("檢測到圖片數值為 0-1 (Float)，自動轉換為 0-255...")
    process_img = original_img * 255.0
else:
    print("檢測到圖片數值為 0-255 (Integer)，保持不變...")
    process_img = original_img.astype(float)

# ==========================================
# 2. 定義核心函式
# ==========================================

def compress_single_channel(channel_matrix, k):
    U, s, Vt = np.linalg.svd(channel_matrix, full_matrices=False)
    
    Sigma_k = np.diag(s[:k])
    U_k = U[:, :k]
    Vt_k = Vt[:k, :]
    
    return np.dot(U_k, np.dot(Sigma_k, Vt_k))

def compress_rgb_image(img, k):
    # 分離 R, G, B 通道 (img 是已經轉成 0-255 的 float)
    r_compressed = compress_single_channel(img[:, :, 0], k)
    g_compressed = compress_single_channel(img[:, :, 1], k)
    b_compressed = compress_single_channel(img[:, :, 2], k)
    
    # 合併
    compressed_img = np.stack((r_compressed, g_compressed, b_compressed), axis=2)
    
    # 限制數值在 0-255 之間，並轉回整數 uint8 供顯示使用
    compressed_img = np.clip(compressed_img, 0, 255).astype(np.uint8)
    
    return compressed_img

# ==========================================
# 3. 執行壓縮與產圖
# ==========================================
k_values = [5, 20, 50, 100]

plt.figure(figsize=(12, 8))

# 顯示原始圖片 (注意：如果是 float 0-255，顯示時要轉回 int 或是除回 255)
# 最簡單的方法是用我們剛剛轉好的 process_img 轉成 uint8 來顯示
plt.subplot(2, 3, 1)
plt.imshow(process_img.astype(np.uint8)) 
plt.title("Original (RGB)")
plt.axis('off')

print("開始處理 RGB 壓縮...")

for i, k in enumerate(k_values):
    print(f"正在處理 k={k}...")
    compressed = compress_rgb_image(process_img, k)
    
    # 計算壓縮率
    h, w, _ = original_img.shape
    original_size = h * w * 3
    compressed_data_size = 3 * (k * (h + k + w))
    ratio = compressed_data_size / original_size * 100
    
    plt.subplot(2, 3, i+2)
    plt.imshow(compressed)
    plt.title(f"k={k}\n(Size: ~{ratio:.1f}%)")
    plt.axis('off')

plt.tight_layout()
plt.savefig('rgb_compression_result.png')
print("完成！結果已儲存為 rgb_compression_result.png")
plt.show()
