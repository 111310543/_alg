
# 1. 動態規劃：LCS (Longest Common Subsequence)
def diff_dp(seq1: list, seq2: list):
    m, n = len(seq1), len(seq2)
    # 建立 DP 表格，dp[i][j] 代表 seq1[0..i-1] 與 seq2[0..j-1] 的 LCS 長度
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # 回溯建立 diff 結果
    i, j = m, n
    diff_result = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and seq1[i - 1] == seq2[j - 1]:
            diff_result.append(f"  {seq1[i - 1]}")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            diff_result.append(f"+ {seq2[j - 1]}")
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j - 1] < dp[i - 1][j]):
            diff_result.append(f"- {seq1[i - 1]}")
            i -= 1
            
    diff_result.reverse()
    return diff_result


# 2. 非動態規劃：Myers Diff 演算法 (貪婪 + 編輯圖尋路)
def diff_myers(seq1: list, seq2: list):
    N, M = len(seq1), len(seq2)
    MAX = N + M
    v = {1: 0}
    trace = []

    # 尋找最短編輯路徑 (Shortest Edit Script)
    for d in range(MAX + 1):
        v_copy = v.copy()
        trace.append(v_copy)
        for k in range(-d, d + 1, 2):
            # 判斷是向下走（刪除）還是向右走（插入）
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
            
            y = x - k
            
            # 對角線延伸（當元素相同時不用付代價）
            while x < N and y < M and seq1[x] == seq2[y]:
                x += 1
                y += 1
                
            v[k] = x
            
            if x >= N and y >= M:
                # 回溯還原編輯路徑
                return backtrace_myers(trace, seq1, seq2)
    return []

def backtrace_myers(trace, seq1, seq2):
    x, y = len(seq1), len(seq2)
    script = []
    
    for d in range(len(trace) - 1, -1, -1):
        v = trace[d]
        k = x - y
        
        if d == 0:
            prev_k = 0
        elif k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
            prev_k = k + 1
        else:
            prev_k = k - 1
            
        prev_x = v.get(prev_k, 0)
        prev_y = prev_x - prev_k
        
        # 對角線移動（保持不變）
        while x > prev_x and y > prev_y:
            script.append(f"  {seq1[x - 1]}")
            x -= 1
            y -= 1
            
        if d > 0:
            if x == prev_x:
                script.append(f"+ {seq2[y - 1]}")
                y -= 1
            else:
                script.append(f"- {seq1[x - 1]}")
                x -= 1
                
    script.reverse()
    return script


# 測試範例
if __name__ == "__main__":
    doc1 = ["A", "B", "C", "A", "B", "B", "A"]
    doc2 = ["C", "B", "A", "B", "A", "C"]

    print("=== 動態規劃 (LCS DP) 結果 ===")
    print("\n".join(diff_dp(doc1, doc2)))

    print("\n=== 非動態規劃 (Myers Diff) 結果 ===")
    print("\n".join(diff_myers(doc1, doc2)))

    #原理說明與複雜度分析特性 / 演算法1. 動態規劃 (LCS)   PNG2. 非動態規劃 (Myers Diff)   PNG核心原理將問題拆解為子問題，建立 $N \times M$ 矩陣，計算兩序列的最長公共子序列，再透過回溯找出相異之處。   將文本變更視為在一張網格圖（Edit Graph）上尋找最短路徑。利用貪婪策略優先嘗試「沿對角線延伸」（相同文字），按編輯距離 $D$ 逐步拓展。   時間複雜度$O(N \cdot M)$無論兩檔案差異大或小，皆需填滿整個矩陣。$O(N \cdot M)$（最壞）/ $O((N+M) \cdot D)$（平均）其中 $D$ 為兩檔案間的差異數量（Edit Distance）。差異越少（$D$ 小），執行速度越快。   空間複雜度$O(N \cdot M)$需要儲存完整的 DP 表格以進行回溯（經優化可降至 $O(\min(N,M))$，但回溯難度增加）。$O(N + M + D^2)$經空間優化（如線性空間 Myers）可進一步降低至 $O(N + M)$。實務應用適合用於小字串比對或理論教學展示。   Git (git diff)、GNU diff 等絕大多數版本控制工具的預設標準演算法。   兩者比較總結效能優勢：在真實世界的軟體開發中，檔案修改通常只佔極小部分（即差異數 $D$ 遠小於文本長度 $N$ 與 $M$）。Myers 演算法能將時間複雜度降至與 $D$ 相關，因此在處理大檔案時速度遠優於傳統 DP。   記憶體消耗：DP 需要構建巨大的二維矩陣，遭遇大型檔案時容易暴記憶體；Myers 演算法在空間利用上更具彈性且易於優化。   
