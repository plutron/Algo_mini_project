import itertools
from statistics import median


#اين الگوريتمه چون خيلي طولاني بود نوشتنش کد نويسيش رو با کمک هوش مصنوعي انجام دادم اما طراحي خود الگوريتم کار خودمه


'''
اين الگوريتم اينجوري کار ميکنه مياد نقاط رو به صورت جدول مختصات در ميازه ( با کمک يه تابع find_locations از functions)

بعد نقطه وسط رو با استفاده از ميانه بدست مياره يعني ميانه نقاط بر اساس محور x ها و y ها
بعد که به 4 بخش تبديل شد مياد و اونهارو به 4 بهش ( ربع هاي جدول مختصات ) تبديل ميکنه
حالا براي هر بخش يه کار انجام ميده

اول نقاط اتصال هر بخش با بخش کناري رو بدست مياره
به اين صورت که دو نقطه نزديک به هم در هر دو ربع رو به صورت پل اتصال در نظر ميگيره

اگه تعداد کمتر از 6 بود ( متناسب با دقت و سرعت الگوريتم ميشه اين مقدار رو عوض کرد) يه بار بک ترکينگ انجام ميده و با نقطه شروع و پايان که از قبل داريم که همون نقاط ارتباط با
بقيه ربع ها هستن بهترين مسير رو پيدا ميکنم

اگه بيشتر از 6 بود دوباره از اول بازگشتي انجام ميديم


پيچيدگي زماني o(nlogn) داره که به طور کلي از nn بهتره
ميشه با استفاده از اون عدد که اشاره شد دقت رو افزايش داد اما سرعت کم ميشه و بلعکس
تا حدود بازه n<100 از nn بهتر و سريع تر کار ميکنه يا اينکه خطاي خيلي کمي داره
نتايج دقيقتر توي بنچمارک ميارم
'''

def tsp_divide_and_conquer(L, D):
    n = len(L)
    if n == 0:
        return []
    if n == 1:
        return [0]


    def exact_path(points, start, end):
        if len(points) == 1:
            return [start]  
        if start != end:
            middle = [p for p in points if p != start and p != end]
            best_dist = float('inf')
            best_perm = None
            
            for perm in itertools.permutations(middle):
                dist = D[start][perm[0]] if middle else D[start][end]
                for i in range(len(perm)-1):
                    dist += D[perm[i]][perm[i+1]]
                if middle:
                    dist += D[perm[-1]][end]
                if dist < best_dist:
                    best_dist = dist
                    best_perm = perm
            if middle:
                return [start] + list(best_perm) + [end]
            else:
                return [start, end]
        else:
            middle = [p for p in points if p != start]
            best_dist = float('inf')
            best_perm = None
            for perm in itertools.permutations(middle):
                dist = D[start][perm[0]] if middle else 0
                for i in range(len(perm)-1):
                    dist += D[perm[i]][perm[i+1]]
                if middle:
                    dist += D[perm[-1]][start]
                if dist < best_dist:
                    best_dist = dist
                    best_perm = perm
            if middle:
                return [start] + list(best_perm) + [start]
            else:
                return [start, start]

    def recursive_solve(indices, start_idx, end_idx):
        if len(indices) <= 6:
            return exact_path(indices, start_idx, end_idx)

        xs = [L[i][0] for i in indices]
        ys = [L[i][1] for i in indices]
        med_x = median(xs)
        med_y = median(ys)


        q1, q2, q3, q4 = [], [], [], []
        for i in indices:
            x, y = L[i]
            if x > med_x and y > med_y:
                q1.append(i)
            elif x <= med_x and y > med_y:
                q2.append(i)
            elif x <= med_x and y <= med_y:
                q3.append(i)
            else:  
                q4.append(i)


        quadrants = {}
        if q1: quadrants['Q1'] = q1
        if q2: quadrants['Q2'] = q2
        if q3: quadrants['Q3'] = q3
        if q4: quadrants['Q4'] = q4


        start_quad = None
        end_quad = None
        for name, qlist in quadrants.items():
            if start_idx in qlist:
                start_quad = name
            if end_idx in qlist:
                end_quad = name

        if start_quad == end_quad or len(quadrants) <= 1 or not start_quad or not end_quad:

            group_A = []
            group_B = []
            for i in indices:
                if D[i][start_idx] < D[i][end_idx]:
                    group_A.append(i)
                else:
                    group_B.append(i)
            

            if not group_A or not group_B:
                mid = len(indices) // 2
                group_A = indices[:mid]
                group_B = indices[mid:]
                if start_idx not in group_A:
                    group_A.append(start_idx)
                if end_idx not in group_B:
                    group_B.append(end_idx)


            min_d_ab = float('inf')
            u_best, v_best = start_idx, end_idx

            candidates_A = [x for x in group_A if x != start_idx] if len(group_A) >= 2 else group_A
            candidates_B = [x for x in group_B if x != end_idx] if len(group_B) >= 2 else group_B

            for u in candidates_A:
                for v in candidates_B:
                    if D[u][v] < min_d_ab:
                        min_d_ab = D[u][v]
                        u_best, v_best = u, v

            path_A = recursive_solve(group_A, start_idx, u_best)
            path_B = recursive_solve(group_B, v_best, end_idx)
            
            return path_A + path_B

        closest = {} 
        quad_names = list(quadrants.keys())
        for i in range(len(quad_names)):
            for j in range(i+1, len(quad_names)):
                A = quad_names[i]
                B = quad_names[j]
                min_d = float('inf')
                best_pair = (None, None)
                for u in quadrants[A]:
                    for v in quadrants[B]:
                        if D[u][v] < min_d:
                            min_d = D[u][v]
                            best_pair = (u, v)
                closest[(A, B)] = (best_pair[0], best_pair[1], min_d)
                closest[(B, A)] = (best_pair[1], best_pair[0], min_d)

        best_order = None
        best_order_cost = float('inf')
        other_quads = [q for q in quad_names if q not in (start_quad, end_quad)]
        
        for perm in itertools.permutations(other_quads):
            candidate = [start_quad] + list(perm) + [end_quad]
            cost = 0
            valid = True
            for k in range(len(candidate)-1):
                edge_key = (candidate[k], candidate[k+1])
                if edge_key not in closest:
                    valid = False
                    break
                cost += closest[edge_key][2]
            if valid and cost < best_order_cost:
                best_order_cost = cost
                best_order = candidate

        if not best_order:
            best_order = quad_names

        child_start_end = {}
        for idx, qname in enumerate(best_order):
            if idx == 0:
                s = start_idx
            else:
                prev = best_order[idx-1]
                s = closest[(prev, qname)][1] 
            if idx == len(best_order)-1:
                e = end_idx
            else:
                nxt = best_order[idx+1]
                e = closest[(qname, nxt)][0]

            if s == e and len(quadrants[qname]) >= 2:
                if idx < len(best_order) - 1:
                    nxt = best_order[idx+1]
                    min_d = float('inf')
                    best_e = -1
                    for u in quadrants[qname]:
                        if u == s:
                            continue
                        for v in quadrants[nxt]:
                            if D[u][v] < min_d:
                                min_d = D[u][v]
                                best_e = u
                    if best_e != -1:
                        e = best_e
                else:
                    prev = best_order[idx-1]
                    min_d = float('inf')
                    best_s = -1
                    for u in quadrants[qname]:
                        if u == e:
                            continue
                        for v in quadrants[prev]:
                            if D[v][u] < min_d:
                                min_d = D[v][u]
                                best_s = u
                    if best_s != -1:
                        s = best_s

            child_start_end[qname] = (s, e)

        path_parts = []
        for qname in best_order:
            s, e = child_start_end[qname]
            sub_path = recursive_solve(quadrants[qname], s, e)
            path_parts.append(sub_path)

        full_path = []
        for part in path_parts:
            full_path.extend(part)
        return full_path

    med_x_all = median([p[0] for p in L])
    med_y_all = median([p[1] for p in L])

    q1_all, q4_all = [], []
    for i, (x, y) in enumerate(L):
        if x > med_x_all and y > med_y_all:
            q1_all.append(i)
        elif x > med_x_all and y <= med_y_all:
            q4_all.append(i)

    if q1_all and q4_all:
        min_d = float('inf')
        best_q4 = best_q1 = None
        for u in q4_all:
            for v in q1_all:
                if D[u][v] < min_d:
                    min_d = D[u][v]
                    best_q4, best_q1 = u, v
        global_start = best_q1
        global_end = best_q4
    else:
        min_d = float('inf')
        global_start, global_end = 0, 1 if n > 1 else 0
        for u in range(n):
            for v in range(u+1, n):
                if D[u][v] < min_d:
                    min_d = D[u][v]
                    global_start = u
                    global_end = v

    all_indices = list(range(n))
    tour_path = recursive_solve(all_indices, global_start, global_end)


    unique_tour = []
    seen = set()
    for u in tour_path:
        if u not in seen:
            unique_tour.append(u)
            seen.add(u)

    for i in range(n):
        if i not in seen:
            unique_tour.append(i)
            seen.add(i)

    if unique_tour:
        unique_tour.append(unique_tour[0])

    return unique_tour
