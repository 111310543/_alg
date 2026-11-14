import heapq

def heuristic(a, b):
    # 曼哈頓距離
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, curr = heapq.heappop(open_set)
        
        if curr == goal:
            path = []
            while curr in came_from:
                path.append(curr)
                curr = came_from[curr]
            return path[::-1]
            
        r, c = curr
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g_score[curr] + 1
                if tentative_g < g_score.get((nr, nc), float('inf')):
                    came_from[(nr, nc)] = curr
                    g_score[(nr, nc)] = tentative_g
                    f_score = tentative_g + heuristic((nr, nc), goal)
                    heapq.heappush(open_set, (f_score, (nr, nc)))
    return None

grid = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
print("NPC A* Path:", a_star_search(grid, (0,0), (2,2)))
