import sys

def christofides_tsp(dist):
    """
    الگوریتم کریستوفیدس برای TSP متریک.
    ورودی: ماتریس فاصله متقارن و صدق‌کننده در نامساوی مثلث
    خروجی: لیست ترتیب شهرها (اندیس‌ها) در یک تور بسته (بازگشت به شهر اول حذف شده)
    """
    n = len(dist)

    # ۱. ساخت درخت پوشای کمینه با الگوریتم پریم
    mst_edges = prim_mst(dist, n)

    # ۲. یافتن رأس‌های با درجه فرد در MST
    degree = [0] * n
    for u, v in mst_edges:
        degree[u] += 1
        degree[v] += 1
    odd_nodes = [i for i in range(n) if degree[i] % 2 == 1]

    # ۳. تطابق کامل کمینه‌وزن روی رأس‌های فرد (روش حریصانه)
    matching_edges = greedy_min_weight_perfect_matching(odd_nodes, dist)

    # ۴. ساخت چندگراف از اجتماع یال‌های MST و تطابق
    # (برای سادگی، گراف را با لیست مجاورت می‌سازیم)
    graph = [[] for _ in range(n)]
    for u, v in mst_edges + matching_edges:
        graph[u].append(v)
        graph[v].append(u)

    # ۵. یافتن مدار اویلری (با الگوریتم Hierholzer)
    eulerian_circuit = hierholzer(graph, start=0)

    # ۶. میان‌بر زدن برای ساخت تور همیلتونی
    visited = [False] * n
    tour = []
    for node in eulerian_circuit:
        if not visited[node]:
            tour.append(node)
            visited[node] = True
    # (اختیاری) بازگشت به نقطه اول به صورت ضمنی وجود دارد

    return tour


# --- توابع کمکی ---

def prim_mst(dist, n):
    """درخت پوشای کمینه با الگوریتم پریم (برای گراف کامل)"""
    visited = [False] * n
    visited[0] = True
    edges = []
    # در هر مرحله نزدیک‌ترین رأس به درخت اضافه می‌شود
    for _ in range(n - 1):
        min_edge = (None, None, float('inf'))
        for u in range(n):
            if visited[u]:
                for v in range(n):
                    if not visited[v] and dist[u][v] < min_edge[2]:
                        min_edge = (u, v, dist[u][v])
        u, v, _ = min_edge
        visited[v] = True
        edges.append((u, v))
    return edges


def greedy_min_weight_perfect_matching(odd_nodes, dist):
    """
    تطابق کامل کمینه‌وزن حریصانه.
    در هر مرحله نزدیک‌ترین زوج از رأس‌های همتا نشده را انتخاب می‌کند.
    (برای تضمین نسبت تقریب ۱.۵ باید تطابق دقیق به‌کار رود)
    """
    unmatched = set(odd_nodes)
    matching = []
    while unmatched:
        u = unmatched.pop()
        # نزدیک‌ترین v در unmatched
        best_v = None
        best_d = float('inf')
        for v in unmatched:
            d = dist[u][v]
            if d < best_d:
                best_d = d
                best_v = v
        if best_v is not None:
            unmatched.remove(best_v)
            matching.append((u, best_v))
    return matching


def hierholzer(graph, start=0):
    """
    الگوریتم Hierholzer برای یافتن مدار اویلری در گرافی که همه رأس‌ها درجه زوج دارند.
    گراف به‌صورت لیست مجاورت (با یال‌های چندگانه مجاز) است.
    """
    # کپی لیست مجاورت (دستکاری‌شدنی)
    adj = [list(neighbors) for neighbors in graph]
    stack = [start]
    circuit = []

    while stack:
        u = stack[-1]
        if adj[u]:  # هنوز یال خروجی دارد
            v = adj[u].pop()
            # حذف یال معکوس از adj[v] (برای گراف بدون جهت)
            adj[v].remove(u)
            stack.append(v)
        else:
            circuit.append(stack.pop())
    # مدار اویلری برعکس است؛ برمی‌گردانیم
    return circuit[::-1]


# --- مثال اجرا ---
if __name__ == "__main__":
    # یک ماتریس فاصله متریک (مثلاً فواصل شهرها)
    dist_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tour = christofides_tsp(dist_matrix)
    print("ترتیب بازدید شهرها:", tour)
    print("طول تور:", sum(dist_matrix[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour))))