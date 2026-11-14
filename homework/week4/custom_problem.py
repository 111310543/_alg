# 定義三個不同的迭代函數
g1 = lambda x: x**3 - 1
g2 = lambda x: (x + 1)**(1/3)
g3 = lambda x: x - (x**3 - x - 1) / (3*x**2 - 1)

# 設定初始猜測值
x1 = x2 = x3 = 1.0

print(f"{'次數':<4} | {'g1(x) (直接移項)':<18} | {'g2(x) (開三次方)':<18} | {'g3(x) (牛頓法)':<18}")
print("-" * 70)

for i in range(1, 11):
    # g1(x) 增長極快，為了避免數字大到無法顯示，做個簡單的溢位保護
    try:
        if abs(x1) < 1e5:
            x1 = g1(x1)
        else:
            x1 = float('inf')
    except OverflowError:
        x1 = float('inf')
        
    x2 = g2(x2)
    x3 = g3(x3)
    
    print(f"{i:<6} | {x1:<22.5f} | {x2:<22.5f} | {x3:<22.5f}")
