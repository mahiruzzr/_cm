import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

img = mpimg.imread('test_image.jpg')
gray_img = rgb2gray(img)            

plt.imshow(gray_img, cmap='gray')
plt.title("Original Grayscale Image")
plt.show()

print(f"圖片矩陣大小: {gray_img.shape}")

U, s, Vt = np.linalg.svd(gray_img, full_matrices=False)

print(f"U 的大小: {U.shape}")
print(f"s (奇異值) 的數量: {s.shape}")
print(f"Vt 的大小: {Vt.shape}")

plt.plot(s)
plt.title("Singular Values (Importance of features)")
plt.ylabel("Value")
plt.xlabel("Index")
plt.show()

def compress_image(k, U, s, Vt):
    """
    k: 要保留的前 k 個奇異值
    U, s, Vt: SVD 分解後的結果
    """
    
    Sigma_k = np.diag(s[:k])
    
    U_k = U[:, :k]
    Vt_k = Vt[:k, :]

    reconstructed_img = np.dot(U_k, np.dot(Sigma_k, Vt_k))
    
    return reconstructed_img
    
k_value = 50
img_compressed = compress_image(k_value, U, s, Vt)

plt.imshow(img_compressed, cmap='gray')
plt.title(f"Compressed with k={k_value}")
plt.show()

k_values = [5, 20, 50, 100]

plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.imshow(gray_img, cmap='gray')
plt.title("Original")
plt.axis('off')

for i, k in enumerate(k_values):
    compressed = compress_image(k, U, s, Vt)
    
    original_size = gray_img.shape[0] * gray_img.shape[1]
    compressed_size = k * (gray_img.shape[0] + k + gray_img.shape[1]) # U_k + Sigma_k + Vt_k
    compression_ratio = compressed_size / original_size * 100
    
    plt.subplot(2, 3, i+2)
    plt.imshow(compressed, cmap='gray')
    plt.title(f"k={k} (Size: {compression_ratio:.1f}%)")
    plt.axis('off')

plt.tight_layout()
plt.show()
