from itertools import permutations
from functions import totalDistance

def bruteForceForTSP(distances):
    n = len(distances)
    bestpath = ()
    m = float('inf')
    for path in permutations(range(n)):
        p = list(path)+[path[0]]
        total_path_distance = totalDistance(p, distances)
        if total_path_distance < m:
            m = total_path_distance
            bestpath = path
    a = list(bestpath)
    a.append(a[0])
    return a

def bruteForceForTSPWithDP(l):
    n = len(l)
    li = [[i] for i in range(n)]
    cost = [0 for i in range(n)]
    dp = {}

    for i in range(n):
        dp[(tuple([i]), i)] = 0
    for z in range(n - 1):
        new_li = []
        new_cost = []
        i = 0
        for j in li:
            for k in range(n):
                if k not in j:
                    newPath = j + [k]
                    newCost = cost[i] + l[j[-1]][k]
                    key = (tuple(sorted(newPath)), k)

                    if key not in dp or newCost < dp[key]:
                        dp[key] = newCost
                        new_li.append(newPath)
                        new_cost.append(newCost)
            i += 1
        li = new_li
        cost = new_cost
    final_costs = []
    for i in range(len(li)):
        path = li[i]
        start_node = path[0]
        last_node = path[-1]

        cycle_cost = cost[i] + l[last_node][start_node]
        final_costs.append(cycle_cost)
    min_cost = min(final_costs)
    min_index = final_costs.index(min_cost)

    best_path = li[min_index] + [li[min_index][0]]
    return best_path