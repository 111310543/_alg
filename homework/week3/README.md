# 布林可滿足性問題 (SAT) 真值表列舉程式

## 什麼是 SAT 問題？
布林可滿足性問題（Boolean Satisfiability Problem，簡稱 SAT）的核心在於找出一組布林變數的賦值（`True` 或 `False`），使得整個布林表達式的結果為真（`True`）。

使用「列舉真值表（Truth Table）」是最基礎也最直觀的解法，也就是所謂的**暴力破解法（Brute-force）**。對於 $n$ 個變數，我們系統性地產生 $2^n$ 種所有可能的真假值組合，並一一帶入表達式中檢驗。

---

## Python 程式碼實作

以下是使用 Python 撰寫的 SAT 真值表列舉程式。程式利用了 `itertools.product` 來系統性生成所有的變數組合，並透過 `eval` 來計算布林表達式的結果。

```python
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
```

---

## 程式運作原理

1. **定義變數與表達式**：我們將邏輯式寫成 Python 支援的語法（如 `and`, `or`, `not`），並將變數的名稱用列表傳入。
2. **生成所有組合**：呼叫 `itertools.product([False, True], repeat=n)`。這是一個笛卡爾積函數，完美對應了二進制中從 `000...0` 到 `111...1` 的所有枚舉過程。
3. **動態評估**：`eval()` 函數將字串形式的表達式轉為程式碼執行，同時將生成的 True/False 組合（`env` 字典）作為變數值傳入。
4. **驗證與記錄**：只要在遍歷過程中，出現至少一個讓結果為 `True` 的組合，就判定這個 SAT 問題是「可滿足的」，並將這組賦值記錄下來。

## 效能與限制

這種真值表窮舉法的時間複雜度為 **$O(2^n)$**：
* 對於 3 到 10 個變數的簡單邏輯式，這支程式能瞬間給出答案並印出精美的真值表。
* 但由於指數增長的特性，如果變數數量達到 50 或 100 個以上，真值表列舉法將會耗費極長的時間（甚至超出宇宙壽命）。

在實務的 SAT Solver（例如 MiniSat、Z3）中，通常不會使用完全的真值表窮舉，而是會採用更高效的演算法（如 **DPLL** 或 **CDCL (Conflict-Driven Clause Learning)**），藉由邏輯推導大幅跳過不需要檢查的真值分支。
