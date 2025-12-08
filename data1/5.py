import numpy as np

def hamming_74_demo():
    print("\n--- 習題 5: 7-4 漢明碼編碼與解碼 ---")

    # 定義生成矩陣 G (4x7)
    # 結構為 [I_4 | P]，其中 I_4 是單位矩陣，P 是奇偶校驗部分
    G = np.array([
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ])

    # 定義校驗矩陣 H (3x7)
    # 結構為 [P^T | I_3]
    H = np.array([
        [1, 1, 0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 0, 1]
    ])

    # 1. 輸入資料 (4 bits)
    data = np.array([1, 0, 1, 1]) 
    print(f"原始資料: {data}")

    # 2. 編碼: c = d * G (模 2 運算)
    codeword = np.dot(data, G) % 2
    print(f"編碼後 (Codeword): {codeword}")

    # 3. 模擬雜訊: 隨機翻轉一個 bit (例如第 2 個 bit，索引 1)
    received = codeword.copy()
    error_pos = 1 
    received[error_pos] = (received[error_pos] + 1) % 2
    print(f"接收到的訊號 (第 {error_pos+1} 位出錯): {received}")

    # 4. 解碼與除錯: 計算校驗子 (Syndrome) s = r * H^T
    syndrome = np.dot(received, H.T) % 2
    print(f"校驗子 (Syndrome): {syndrome}")
    
    # 將二進位 [s0, s1, s2] 轉為十進位整數以找出錯誤位置
    # 注意: 這裡的 syndrome 排列順序對應 H 的行向量
    # 對於這個特定的 H 矩陣，Syndrome (轉十進位) 直接對應錯誤的位置 (由大到小排列位元)
    # s 向量通常讀作 [z1, z2, z3] 或類似順序，需根據 H 矩陣構造解析
    
    error_index = -1
    # 比對 Syndrome 與 H 的每一個行向量(Column)
    for i in range(7):
        if np.array_equal(syndrome, H[:, i]):
            error_index = i
            break
            
    if error_index != -1:
        print(f"偵測到錯誤在索引: {error_index} (第 {error_index+1} 位)")
        # 更正錯誤
        received[error_index] = (received[error_index] + 1) % 2
        print(f"更正後的訊號: {received}")
        
        # 提取前 4 位作為原始資料
        decoded_data = received[:4] # 因為 G 矩陣前 4 列是單位矩陣
        print(f"解碼資料: {decoded_data}")
        print(f"是否與原始資料相符: {np.array_equal(data, decoded_data)}")
    else:
        print("未偵測到錯誤。")

hamming_74_demo()
