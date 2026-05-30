import time
import functoins  # فرض می‌کنیم توابع کمکی در این ماژول هستند
from NN import nearestNeighbor
from coordinatesAlgorithms import xBasedAlgorithm
from m import tsp_divide_and_conquer
from a import tsp_divide_conquer_dist

def benchmark():
    x = n = 0          # شمارنده بردها: n برای NN بهتر، x برای DC بهتر
    total_nn_time = 0.0
    total_dc_time = 0.0
    total_ratio = 0.0
    num_instances = 100

    print(f"{'Inst':>5} | {'Size':>5} | {'NN dist':>10} | {'DC dist':>10} | {'Ratio(NN/DC)':>13} | {'NN time(s)':>10} | {'DC time(s)':>10} | {'Winner':>6} | {'Accuracy %':>10}")
    print("-" * 110)

    for i in range(num_instances):
        # بارگذاری داده
        l = functoins.GetDistancesFromFile(str(i) + '.txt')
        size = len(l)  # تعداد شهرها

        # الگوریتم نزدیک‌ترین همسایه
        start = time.perf_counter()
        a = christofides_tsp(l)
        nn_time = time.perf_counter() - start
        nn_dist = functoins.totalDistance(a, l)

        # الگوریتم تقسیم و حل
        li = functoins.find_locations(l)  # مختصات یا مکان‌ها
        start = time.perf_counter()
        b = tsp_divide_and_conquer(li,l)
        dc_time = time.perf_counter() - start
        dc_dist = functoins.totalDistance(b, l)

        # نسبت مسافت‌ها (NN به DC)
        ratio = nn_dist / dc_dist

        # برنده
        if nn_dist < dc_dist:
            winner = "NN"
            n += 1
        elif dc_dist < nn_dist:
            winner = "DC"
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
    print(f"  بردهای NN: {n}")
    print(f"  بردهای DC: {x}")
    ties = num_instances - n - x
    print(f"  تساوی‌ها: {ties}")
    print(f"  درصد پیروزی NN: {n/num_instances*100:.2f}%")
    print(f"  درصد پیروزی DC: {x/num_instances*100:.2f}%")
    print(f"  میانگین نسبت (NN/DC): {total_ratio/num_instances:.4f}")
    print(f"  میانگین زمان NN: {total_nn_time/num_instances:.6f} ثانیه")
    print(f"  میانگین زمان DC: {total_dc_time/num_instances:.6f} ثانیه")
    print(f"  کل زمان NN: {total_nn_time:.4f} ثانیه")
    print(f"  کل زمان DC: {total_dc_time:.4f} ثانیه")

if __name__ == "__main__":
    benchmark()