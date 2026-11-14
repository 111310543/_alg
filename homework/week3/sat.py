import itertools

def solve_sat_by_truth_table(formula_str, variables):
    """
    透過系統性列舉真值表來解決 SAT 問題
    
    :param formula_str: Python 語法的布林表達式字串，例如 "(P or Q) and (not R)"
    :param variables: 變數名稱的列表，例如 ['P', 'Q', 'R']
    """
    print(f"🔍 正在解析布林表達式: {formula_str}")
    print("-" * 50)
    
    # 建立真值表標題列
    header = "\t".join(variables) + "\t| Result"
    print(header)
    print("-" * 50)
    
    satisfiable = False
    solutions = []
    
    # itertools.product([False, True], repeat=n) 會產生 2^n 種所有的 True/False 組合
    for values in itertools.product([False, True], repeat=len(variables)):
        # 將變數名稱與當前的 True/False 值綁定成字典 { 'P': False, 'Q': True, ... }
        env = dict(zip(variables, values))
        
        try:
            # 評估布林表達式的結果 (限制全域與區域變數環境以提升安全性與準確性)
            result = eval(formula_str, {}, env)
        except Exception as e:
            print(f"表達式評估錯誤: {e}")
            return
        
        # 格式化輸出：為了閱讀方便，將 True/False 轉換為 T/F
        row_str = "\t".join(['T' if v else 'F' for v in values]) + f"\t| {'T' if result else 'F'}"
        print(row_str)
        
        # 若結果為 True，代表找到一組滿足解 (Satisfying Assignment)
        if result:
            satisfiable = True
            solutions.append(env)
            
    print("-" * 50)
    
    # 輸出最終 SAT 結論
    if satisfiable:
        print("💡 結論：此表達式是【可滿足的 (Satisfiable)】。")
        print(f"總共找到 {len(solutions)} 組解。滿足條件的變數組合為：")
        for i, sol in enumerate(solutions, 1):
            # 格式化輸出解
            sol_str = ", ".join([f"{k} = {v}" for k, v in sol.items()])
            print(f"  解 {i}: {sol_str}")
    else:
        print("🚫 結論：此表達式是【不可滿足的 (Unsatisfiable)】(即矛盾式，結果永遠為 False)。")


# ==========================================
# 測試範例
# ==========================================
if __name__ == "__main__":
    # 範例 1：可滿足的表達式 (Satisfiable)
    # 邏輯式：(A ∨ B) ∧ (¬C)
    formula1 = "(A or B) and (not C)"
    vars1 = ['A', 'B', 'C']
    solve_sat_by_truth_table(formula1, vars1)

    print("\n" + "="*50 + "\n")

    # 範例 2：不可滿足的表達式 (Unsatisfiable)
    # 邏輯式：P ∧ (¬P ∨ Q) ∧ ¬Q
    # 根據邏輯推演，這是一個矛盾式，不可能為 True
    formula2 = "P and (not P or Q) and (not Q)"
    vars2 = ['P', 'Q']
    solve_sat_by_truth_table(formula2, vars2)
