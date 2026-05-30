def nearestNeighbor(l):
    n = len(l)
    path = [0]
    point = 0
    for i in range(n-1):
        m = float('inf')
        nextPoint = -1
        for j in range(n):
            x = l[point][j]
            if x and (j not in path):
                if m>x:
                    m = x
                    nextPoint = j
                
                    
        path.append(nextPoint)
        point = nextPoint
    path.append(0)
    return path