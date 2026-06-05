from functions import GetDistancesFromFile,totalDistance
from backTraking import backTrakingForTSPWithDP,backTrackingForTSP
from heldKarp import held_karp_with_path

l = GetDistancesFromFile("0.txt")
a = backTrackingForTSP(l)
print("bk : ",a ,totalDistance(a,l))
a = backTrakingForTSPWithDP(l)
print("dp: ",a,totalDistance(a,l) )
a = held_karp_with_path(l)
print("hk : ",a,totalDistance(a,l))
