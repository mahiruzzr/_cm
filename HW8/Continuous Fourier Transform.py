import math
import cmath
import matplotlib.pyplot as plt

# 1. 定義離散傅立葉轉換 (DFT) - 正轉換
def dft(x):
    """
    輸入: x (時間域訊號，列表或陣列)
    輸出: X (頻率域訊號，複數列表)
    """
    N = len(x)
    X = []
    for k in range(N):
        sum_val = 0
        for n in range(N):
            # 套用公式: x[n] * e^(-i * 2 * pi * k * n / N)
            angle = -2 * math.pi * k * n / N
            sum_val += x[n] * cmath.exp(1j * angle)
        X.append(sum_val)
    return X

# 2. 定義離散傅立葉逆轉換 (IDFT) - 逆轉換
def idft(X):
    """
    輸入: X (頻率域訊號，複數列表)
    輸出: x (重建的時間域訊號，複數列表)
    """
    N = len(X)
    x = []
    for n in range(N):
        sum_val = 0
        for k in range(N):
            # 套用公式: X[k] * e^(i * 2 * pi * k * n / N)
            # 注意這裡是指數是正的
            angle = 2 * math.pi * k * n / N
            sum_val += X[k] * cmath.exp(1j * angle)
        # IDFT 需要除以 N
        x.append(sum_val / N)
    return x

# 3. 驗證函數
def run_verification():
    # --- 準備測試數據 ---
    # 產生一個混合波形：由兩個不同頻率的弦波組成
    # f(t) = sin(2 * pi * t) + 0.5 * sin(6 * pi * t)
    N = 50  # 取樣點數
    original_signal = []
    t_values = []
    for i in range(N):
        t = i / N
        val = math.sin(2 * math.pi * t * 1) + 0.5 * math.sin(2 * math.pi * t * 3)
        original_signal.append(val)
        t_values.append(t)

    print("1. 原始訊號生成完畢 (長度 N={})".format(N))

    # --- 執行 DFT ---
    freq_spectrum = dft(original_signal)
    print("2. DFT 正轉換完畢")

    # --- 執行 IDFT ---
    reconstructed_signal_complex = idft(freq_spectrum)
    print("3. IDFT 逆轉換完畢")

    # 由於浮點數運算誤差，逆轉換回來的數值可能是複數（虛部極小），我們取實部
    reconstructed_signal = [z.real for z in reconstructed_signal_complex]

    # --- 驗證與比對 ---
    # 計算誤差 (MSE)
    error = 0
    for i in range(N):
        error += (original_signal[i] - reconstructed_signal[i]) ** 2
    mse = error / N
    
    print("-" * 30)
    print(f"驗證結果 (均方誤差): {mse:.2e}")
    if mse < 1e-10:
        print(">> 成功！逆轉換後的訊號與原訊號幾乎完全一致。")
    else:
        print(">> 警告：誤差過大，請檢查公式。")

    # --- 繪圖顯示 ---
    plt.figure(figsize=(10, 6))
    
    # 畫出原始訊號
    plt.subplot(2, 1, 1)
    plt.plot(t_values, original_signal, 'b-', label='Original Signal', linewidth=2)
    plt.plot(t_values, reconstructed_signal, 'r--', label='Reconstructed (IDFT)', linewidth=2)
    plt.title('Verification: Original vs IDFT Reconstructed')
    plt.legend()
    plt.grid(True)

    # 畫出頻譜 (振幅)
    plt.subplot(2, 1, 2)
    # 計算振幅 |X[k]|
    magnitudes = [abs(z) for z in freq_spectrum]
    # 只需要顯示前一半的頻率 (因為是對稱的)
    plt.stem(range(len(magnitudes)), magnitudes)
    plt.title('Frequency Spectrum (Magnitude of DFT)')
    plt.xlabel('Frequency Bin (k)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_verification()
