def solve_maze_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    path = []
    visited = set()

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or maze[r][c] == 1 or (r, c) in visited:
            return False
        
        path.append((r, c))
        visited.add((r, c))
        
        if (r, c) == end:
            return True
            
        # 探索方向：下、右、上、左
        if dfs(r+1, c) or dfs(r, c+1) or dfs(r-1, c) or dfs(r, c-1):
            return True
            
        path.pop() # 回溯
        return False

    if dfs(start[0], start[1]):
        return path
    return None

# 測試 (0為可走，1為牆壁)
maze = [[0, 1, 0, 0], [0, 0, 0, 1], [1, 1, 0, 0]]
print("Maze Path:", solve_maze_dfs(maze, (0,0), (2,3)))
