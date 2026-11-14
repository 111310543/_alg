def hanoi_recursive(n, source, auxiliary, target):
    if n == 1:
        print(f"移動盤子 1 從 {source} 到 {target}")
        return
    # 將 N-1 個盤子從 source 移到 auxiliary
    hanoi_recursive(n - 1, source, target, auxiliary)
    # 將最底下的第 N 個盤子從 source 移到 target
    print(f"移動盤子 {n} 從 {source} 到 {target}")
    # 將 N-1 個盤子從 auxiliary 移到 target
    hanoi_recursive(n - 1, auxiliary, source, target)

# 測試呼叫： hanoi_recursive(3, 'A', 'B', 'C')
