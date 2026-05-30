def held_karp_with_path(dists):
    n = len(dists)
    memo = {}
    parent = {}

    def visit(visited_mask, last_city):
        if visited_mask == (1 << n) - 1:
            return dists[last_city][0]
        if (visited_mask, last_city) in memo:
            return memo[(visited_mask, last_city)]

        min_cost = float('inf')
        best_next_city = -1
        for next_city in range(n):
            if (visited_mask & (1 << next_city)) == 0:
                cost = dists[last_city][next_city] + visit(visited_mask | (1 << next_city), next_city)
                if cost < min_cost:
                    min_cost = cost
                    best_next_city = next_city
        memo[(visited_mask, last_city)] = min_cost
        parent[(visited_mask, last_city)] = best_next_city
        return min_cost
    min_tour_cost = visit(1, 0)
    path = [0]
    visited_mask = 1
    current_city = 0

    for _ in range(n - 1):
        next_city = parent[(visited_mask, current_city)]
        path.append(next_city)


        visited_mask |= (1 << next_city)
        current_city = next_city

    path.append(0)

    return path
