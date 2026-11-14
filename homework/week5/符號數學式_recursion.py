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
