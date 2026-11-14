def hanoi_iterative(n, source, auxiliary, target):
    # stack 儲存：(盤子數量, 來源, 輔助, 目標, 是否已完成子任務)
    stack = [(n, source, auxiliary, target, False)]
    
    while stack:
        disk, src, aux, tgt, is_done = stack.pop()
        
        if is_done or disk == 1:
            print(f"移動盤子 {disk} 從 {src} 到 {tgt}")
        else:
            # 依照遞迴反向順序推入 stack (LIFO)
            stack.append((disk - 1, aux, src, tgt, False))  # 步驟3
            stack.append((disk, src, aux, tgt, True))       # 步驟2
            stack.append((disk - 1, src, tgt, aux, False))  # 步驟1

# 測試呼叫： hanoi_iterative(3, 'A', 'B', 'C')
