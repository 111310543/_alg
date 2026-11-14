# 演算法與函數式編程實作範例

本文件收錄了三個經典問題的實作方法，包含河內塔問題的雙重解法、符號數學式的遞迴微分，以及完全不使用迴圈的函數式泡沫排序。

---

## 1. 河內塔問題：遞迴與非遞迴解法

### 遞迴解法
利用分治法的思想，將 N 個盤子分為「上方的 N-1 個」與「最底層的 1 個」進行搬移。

```python
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
```

### 非遞迴解法 (使用堆疊模擬)
利用 Stack 手動模擬遞迴的過程，將每次的狀態（包含參數與執行階段）推進堆疊中，以避免使用系統內建的遞迴。

```python
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
```

---

## 2. 符號數學式微分：遞迴解法

使用 Tuple 樹狀結構來表示抽象語法樹 (AST)。例如 $x^2 + 3x$ 可表示為 `('+', ('^', 'x', 2), ('*', 3, 'x'))`，並透過遞迴法則進行偏導數計算。

```python
def sym_diff(expr, var='x'):
    # 常數的微分為 0
    if isinstance(expr, (int, float)):
        return 0
    # 變數的微分：若為目標變數則為 1，其餘變數當作常數為 0
    if isinstance(expr, str):
        return 1 if expr == var else 0
        
    op, *args = expr
    
    # 遞迴應用微分基本法則
    if op == '+':
        return ('+', sym_diff(args[0], var), sym_diff(args[1], var))
    elif op == '-':
        return ('-', sym_diff(args[0], var), sym_diff(args[1], var))
    elif op == '*':
        u, v = args[0], args[1]
        # (uv)' = u'v + uv'
        return ('+', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var)))
    elif op == '^':
        base, exp = args[0], args[1]
        # 簡單 Chain rule: (u^n)' = n * u^(n-1) * u'
        return ('*', ('*', exp, ('^', base, exp - 1)), sym_diff(base, var))
    else:
        raise ValueError(f"未支援的運算子: {op}")

# 測試呼叫：對 x^2 + 5x 微分
# expr = ('+', ('^', 'x', 2), ('*', 5, 'x'))
# print(sym_diff(expr, 'x')) 
# 輸出：('+', ('*', ('*', 2, ('^', 'x', 1)), 1), ('+', ('*', 0, 'x'), ('*', 5, 1)))
```

---

## 3. 自製 map / filter / reduce 與無迴圈泡沫排序

在完全禁止使用 `for` 或 `while` 迴圈的前提下，所有迭代皆利用遞迴完成。透過自製的 `my_reduce` 實現單次「相鄰元素交換 (Bubble Pass)」，再透過外部遞迴完成所有排序步驟。

### 自製高階函數
```python
# 1. 自製 map 函數 (遞迴)
def my_map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

# 2. 自製 filter 函數 (遞迴)
def my_filter(func, lst):
    if not lst:
        return []
    return ([lst[0]] if func(lst[0]) else []) + my_filter(func, lst[1:])

# 3. 自製 reduce 函數 (遞迴)
def my_reduce(func, lst, initial=None):
    if not lst:
        return initial
    if initial is None:
        return my_reduce(func, lst[1:], lst[0])
    return my_reduce(func, lst[1:], func(initial, lst[0]))
```

### 無迴圈泡沫排序實作
```python
def bubble_pass(acc, x):
    """
    reduce 的回呼函數：
    將新元素 x 與目前累積陣列 (acc) 的最後一個元素比較。
    若發現前面的元素較大，則交換（將大的元素保留在尾端，繼續往右浮動）。
    """
    if not acc:
        return [x]
    prev = acc[-1]
    if prev > x:
        return acc[:-1] + [x, prev]
    return acc + [x]

def bubble_sort(lst):
    """主函數：利用遞迴反覆執行 reduce 進行排序"""
    if len(lst) <= 1:
        return lst
        
    # 單次 pass 會將當前最大的元素推至列表最尾端
    bubbled = my_reduce(bubble_pass, lst, [])
    
    # 將已排好序的最大值切出，剩下的子陣列繼續遞迴排序
    return bubble_sort(bubbled[:-1]) + [bubbled[-1]]

# 測試呼叫：
# unsorted_list = [64, 34, 25, 12, 22, 11, 90]
# print(bubble_sort(unsorted_list)) 
# 輸出：[11, 12, 22, 25, 34, 64, 90]
```
