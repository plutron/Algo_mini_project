import time
import functions
from NN import nearestNeighbor
from tspDivideAndCounqure import tsp_divide_and_conquer
from coordinatesAlgorithms import xBasedAlgorithm

from heldKarp import held_karp_with_path

def benchmark():
    x = n = 0
    total_nn_time = 0.0
    total_dc_time = 0.0
    total_ratio = 0.0
    num_instances = 1

    print(f"{'Inst':>5} | {'Size':>5} | {'BT dist':>10} | {'DP dist':>10} | {'Ratio(BT/DP)':>13} | {'BT time(s)':>10} | {'DP time(s)':>10} | {'Winner':>6} | {'Accuracy %':>10}")
    print("-" * 110)

    for i in range(num_instances):
        # بارگذاری داده
        l = functions.GetDistancesFromFile(str(i) + '.txt')
        size = len(l)  # تعداد شهرها

        # الگوریتم نزدیک‌ترین همسایه
        start = time.perf_counter()
        a = tsp_divide_and_conquer(l)
        nn_time = time.perf_counter() - start
        nn_dist = functions.totalDistance(a, l)

        # الگوریتم تقسیم و حل
        li = functions.find_locations(l)  # مختصات یا مکان‌ها
        start = time.perf_counter()
        b = tsp_divide_and_conquer(l)
        dc_time = time.perf_counter() - start
        dc_dist = functions.totalDistance(b, l)

        # نسبت مسافت‌ها (NN به DC)
        ratio = nn_dist / dc_dist

        # برنده
        if nn_dist < dc_dist:
            winner = "BT"
            n += 1
        elif dc_dist < nn_dist:
            winner = "DP"
            x += 1
        else:
            winner = "Tie"

        # درصد دقت نسبی: (مسافت بهتر / مسافت بدتر) * 100
        better = min(nn_dist, dc_dist)
        worse = max(nn_dist, dc_dist)
        accuracy_pct = (better / worse) * 100 if worse != 0 else 100.0

        # ذخیره مجموع‌ها برای میانگین‌های نهایی
        total_nn_time += nn_time
        total_dc_time += dc_time
        total_ratio += ratio

        # چاپ ردیف
        print(f"{i:5d} | {size:5d} | {nn_dist:10.2f} | {dc_dist:10.2f} | {ratio:13.4f} | {nn_time:10.6f} | {dc_time:10.6f} | {winner:>6} | {accuracy_pct:9.2f}%")

    # خلاصه نهایی
    print("\n" + "=" * 110)
    print("خلاصه بنچمارک:")
    print(f"  تعداد نمونه‌ها: {num_instances}")
    print(f"  بردهای BT: {n}")
    print(f"  بردهای DP: {x}")
    ties = num_instances - n - x
    print(f"  تساوی‌ها: {ties}")
    print(f"  درصد پیروزی BT: {n/num_instances*100:.2f}%")
    print(f"  درصد پیروزی DP: {x/num_instances*100:.2f}%")
    print(f"  میانگین نسبت (BT/DP): {total_ratio/num_instances:.4f}")
    print(f"  میانگین زمان BT: {total_nn_time/num_instances:.6f} ثانیه")
    print(f"  میانگین زمان DP: {total_dc_time/num_instances:.6f} ثانیه")
    print(f"  کل زمان BT: {total_nn_time:.4f} ثانیه")
    print(f"  کل زمان DP: {total_dc_time:.4f} ثانیه")

if __name__ == "__main__":
    benchmark()