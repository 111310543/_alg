def solve_n_queens(n=8):
    res = []
    board = [-1] * n # board[i] 表示第 i 列的皇后所在的行數

    def is_safe(row, col):
        for r in range(row):
            c = board[r]
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def dfs(row):
        if row == n:
            res.append(board[:])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                dfs(row + 1)
                board[row] = -1

    dfs(0)
    return res

solutions = solve_n_queens(8)
print(f"8-Queens Total Solutions: {len(solutions)}")
