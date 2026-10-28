import math
import random
import time

# ==========================================
# 2. 測試資料 (Test Data)
# ==========================================
# 模擬 10 家星巴克門市的 (X, Y) 座標[cite: 4]
STARBUCKS_LOCATIONS = {
    "台北車站店": (25.0478, 121.5170),
    "中山門市": (25.0531, 121.5208),
    "西門門市": (25.0422, 121.5080),
    "東門門市": (25.0338, 121.5285),
    "信義首選店": (25.0330, 121.5654),
    "松山門市": (25.0498, 121.5780),
    "公館門市": (25.0142, 121.5347),
    "士林門市": (25.0881, 121.5260),
    "內湖門市": (25.0830, 121.5870),
    "南港門市": (25.0550, 121.6070)
}

# 計算兩點間的歐式距離
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 計算整條路徑的總距離（包含回到原點）
def total_distance(path, locations):
    dist = 0
    num_cities = len(path)
    for i in range(num_cities):
        c1 = locations[path[i]]
        c2 = locations[path[(i + 1) % num_cities]]  # 回到起點
        dist += distance(c1, c2)
    return dist

# 取得 2-opt 交換後的路徑（鄰居生成）
def get_2opt_neighbor(path, i, j):
    new_path = path[:]
    new_path[i:j+1] = reversed(path[i:j+1])
    return new_path


# ==========================================
# 4. 各演算法原理與實踐 (Algorithms Implementation)
# ==========================================

# 1. 改進法 / 局部搜尋 (Improvement Method / Local Search)[cite: 3]
def improvement_method(locations):
    path = list(locations.keys())
    random.shuffle(path)  # 隨機初始路徑
    best_dist = total_distance(path, locations)
    n = len(path)
    
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                neighbor = get_2opt_neighbor(path, i, j)
                neighbor_dist = total_distance(neighbor, locations)
                if neighbor_dist < best_dist:
                    path = neighbor
                    best_dist = neighbor_dist
                    improved = True
                    break
            if improved:
                break
    return path, best_dist

# 2. 爬山算法 (Hill Climbing)[cite: 3]
def hill_climbing(locations, max_iterations=1000):
    path = list(locations.keys())
    random.shuffle(path)
    best_dist = total_distance(path, locations)
    n = len(path)
    
    for _ in range(max_iterations):
        i, j = sorted(random.sample(range(n), 2))
        neighbor = get_2opt_neighbor(path, i, j)
        neighbor_dist = total_distance(neighbor, locations)
        
        # 僅接受嚴格更優的解
        if neighbor_dist < best_dist:
            path = neighbor
            best_dist = neighbor_dist
            
    return path, best_dist

# 3. 類比擴大機 / 模擬退火法 (Simulated Annealing)[cite: 3]
def simulated_annealing(locations, temp=1000.0, cooling_rate=0.995, min_temp=0.01):
    path = list(locations.keys())
    random.shuffle(path)
    best_path = list(path)
    best_dist = total_distance(path, locations)
    n = len(path)
    
    current_dist = best_dist
    
    while temp > min_temp:
        i, j = sorted(random.sample(range(n), 2))
        neighbor = get_2opt_neighbor(path, i, j)
        neighbor_dist = total_distance(neighbor, locations)
        
        delta = neighbor_dist - current_dist
        
        # 更優則接受；若較差，則以一定概率接受
        if delta < 0 or random.random() < math.exp(-delta / temp):
            path = neighbor
            current_dist = neighbor_dist
            if current_dist < best_dist:
                best_path = list(path)
                best_dist = current_dist
                
        temp *= cooling_rate
        
    return best_path, best_dist

# 4. 急劇下降法 (Steepest Descent)[cite: 3]
def steepest_descent(locations):
    path = list(locations.keys())
    random.shuffle(path)
    best_dist = total_distance(path, locations)
    n = len(path)
    
    while True:
        best_neighbor = None
        min_neighbor_dist = best_dist
        
        # 檢查「所有」鄰居，找出改善幅度最大者
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                neighbor = get_2opt_neighbor(path, i, j)
                neighbor_dist = total_distance(neighbor, locations)
                if neighbor_dist < min_neighbor_dist:
                    min_neighbor_dist = neighbor_dist
                    best_neighbor = neighbor
                    
        if best_neighbor is None:
            break  # 找不到更好的鄰居，停止搜尋
            
        path = best_neighbor
        best_dist = min_neighbor_dist
        
    return path, best_dist

# 5. 貪婪演算法 (Greedy Algorithm)[cite: 3]
def greedy_algorithm(locations):
    cities = list(locations.keys())
    start_city = cities[0]
    unvisited = set(cities[1:])
    path = [start_city]
    
    current_city = start_city
    while unvisited:
        # 每次選擇距離最近的未造訪門市
        next_city = min(unvisited, key=lambda city: distance(locations[current_city], locations[city]))
        path.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
        
    return path, total_distance(path, locations)


# ==========================================
# 3. 執行方式與執行結果分析 (Execution & Analysis)
# ==========================================
if __name__ == "__main__":
    algorithms = {
        "1. 改進法 (Improvement Method)": improvement_method,
        "2. 爬山算法 (Hill Climbing)": hill_climbing,
        "3. 類比擴大機 (Simulated Annealing)": simulated_annealing,
        "4. 急劇下降法 (Steepest Descent)": steepest_descent,
        "5. 貪婪演算法 (Greedy Algorithm)": greedy_algorithm
    }
    
    print("==================================================")
    print("      旅行星巴克員問題 (TSP) 5 種演算法測試結果")
    print("==================================================\n")
    
    for name, algo in algorithms.items():
        start_time = time.time()
        best_path, best_dist = algo(STARBUCKS_LOCATIONS)
        elapsed_time = (time.time() - start_time) * 1000  # 毫秒
        
        print(f"📌 {name}")
        print(f"   - 最短總距離: {best_dist:.4f}")
        print(f"   - 執行時間: {elapsed_time:.2f} ms")
        print(f"   - 最佳路徑: {' -> '.join(best_path)}")
        print("-" * 50)
