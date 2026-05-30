from statistics import median

def xBasedAlgorithm(l):
    listOfX = [_[1] for _ in l]
    my = median(listOfX)
    n = len(l)
    li = l.copy()
    li.sort()
    path = []
    for i in range(n):
        if li[i][1] < my:
            continue
        path += [findIndex(l,li[i][0],li[i][1])]
        
    for i in range(n-1,-1,-1):
        if li[i][1] >= my:
            continue
        path += [findIndex(l,li[i][0],li[i][1])]
    
    path += [path[0]]
    return path
        
def findIndex(l,x,y):
    for i in range(len(l)):
        if l[i][0] == x and l[i][1] == y:
            return i      
    return -1

#آنقدر بد شکست خورد که حتي ادامه دادن آن هم اشتباه است! پس اين فايل را همينجا به اتمام ميرسانيم ( سجاد دل شکسته از الگوريتم خويش )

    


