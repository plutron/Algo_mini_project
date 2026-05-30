#------------------<FindLocatoins>------------------

import math

def find_locations(dist_matrix):
    n = len(dist_matrix)
    if n < 3:
        raise ValueError("At least 3 points required for 2D localization.")

    locations = [None] * n
    locations[0] = (0.0, 0.0)

    d01 = dist_matrix[0][1]
    if d01 <= 0:
        raise ValueError("Distance between point 0 and 1 must be > 0.")
    locations[1] = (d01, 0.0)

    x2, y2 = find_xy(d01, dist_matrix[2][0], dist_matrix[2][1])
    locations[2] = (x2, y2)

    for i in range(3, n):
        x, y = find_xy(d01, dist_matrix[i][0], dist_matrix[i][1])
        y = resolve_side(x, y, locations[2], dist_matrix[i][2])
        locations[i] = (x, y)

    return locations


def find_xy(d01, d0, d1):
    x = (d0**2 - d1**2 + d01**2) / (2 * d01)
    radicand = max(0.0, d0**2 - x**2)
    y = math.sqrt(radicand)
    return (x, y)


def resolve_side(x, y, ref_point, d_to_ref):
    xr, yr = ref_point
    d2 = d_to_ref ** 2
    dp = abs((x - xr)**2 + (y - yr)**2 - d2)
    dn = abs((x - xr)**2 + (y + yr)**2 - d2)   
    return -y if dn < dp else y  

#------------------<GetDistancesFromFile>------------------


def GetDistancesFromFile(address):
    file = open("./matrix/"+address,"r")
    l = []
    for line in file:
        li = list(map(int,line.split()))
        l.append(li)
    file.close()
    return l


#------------------<totalDistance>------------------

def totalDistance(l0,l1):
    n = len(l0)
    distance = 0
    for i in range(n-1):
        distance += l1[l0[i]][l0[i+1]]
    return distance
    

