def lee_algorithm_routing(grid, start, end):
    # 與 BFS 類似，但會擴展並標記擴展波(Wave propagation)
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    distances = {start: 0}
    
    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            break
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                if (nr, nc) not in distances:
                    distances[(nr, nc)] = distances[(r, c)] + 1
                    queue.append((nr, nc))
    
    # Backtrace (回溯路徑)
    if end not in distances: return None
    path = [end]
    curr = end
    while curr != start:
        r, c = curr
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in distances and distances[(nr, nc)] == distances[curr] - 1:
                curr = (nr, nc)
                path.append(curr)
                break
    return path[::-1]
