from collections import deque

def solve_river_crossing_bfs():
    # 狀態: (farmer, wolf, goat, cabbage)
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)
    queue = deque([(start, [])])
    visited = set([start])
    
    def is_valid(state):
        f, w, g, c = state
        # 狼吃羊 (農夫不在) 或 羊吃菜 (農夫不在)
        if (w == g and f != w) or (g == c and f != g):
            return False
        return True

    while queue:
        curr, path = queue.popleft()
        if curr == goal:
            return path + [curr]
            
        f, w, g, c = curr
        next_f = 1 - f
        # 農夫可以自己過河，或帶一件物品
        moves = [
            (next_f, w, g, c),         # 自己過
            (next_f, next_f, g, c) if f == w else None, # 帶狼
            (next_f, w, next_f, c) if f == g else None, # 帶羊
            (next_f, w, g, next_f) if f == c else None  # 帶菜
        ]
        
        for nxt in moves:
            if nxt and is_valid(nxt) and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [curr]))
    return None

print("River Crossing Steps:", solve_river_crossing_bfs())
