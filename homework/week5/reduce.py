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

# --- 應用：無迴圈泡沫排序 ---

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
