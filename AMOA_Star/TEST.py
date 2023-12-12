import math


def read_cost_vector(n, m, costs):
    # This should read the cost vector from the database or data structure
    C_n_m = costs[n, m]
    return C_n_m


def check_time_windows(segment, time_windows, c_n_m_l, G_op, G_cl, start_time):
    # This should check time windows for all edges within the segment
    check = False
    holding_enabled = False
    holding_cost = 0
    for window_start, window_end in time_windows[segment]:
        n = segment[0]

        if n in G_op and G_op[n]:
            # print("n in G_op ")
            current_time = start_time + int(next(iter(G_op[n]))[0])
        elif n in G_cl and G_cl[n]:
            # print('n in G_cl')
            current_time = start_time + int(next(iter(G_cl[n]))[0])

        if c_n_m_l[0] + current_time > window_end:
            check = False
            break
        elif c_n_m_l[0] <= window_start and window_end - window_start >= c_n_m_l[0]:
            check = False
            holding_enabled = True
            holding_cost = window_start - current_time
        elif c_n_m_l[0] >= window_start and c_n_m_l[0] + current_time <= window_end:
            check = True
            holding_enabled = True
            holding_cost = 0
    return check, holding_enabled, holding_cost


def add_holding_cost(c_n_m_l, holding_cost):
    # This should add the cost of holding to the cost vector
    c_n_m_l = tuple(sum(x) for x in zip(c_n_m_l, holding_cost))
    return c_n_m_l


def select_from_open(OPEN):
    """
    Select the alternative from OPEN with the smallest sum of the first elements of gn and fn.

    :param OPEN: A list of tuples, where each tuple is of the form (n, gn, fn).
    :return: The tuple from OPEN with the smallest sum of the first elements of gn and fn.
    """
    # Find the alternative with the smallest sum of the first elements of gn and fn
    return min(OPEN, key=lambda x: x[1][0] + x[2][0])


def is_dominated(c, c_prime):
    """
    Determine if cost vector c is dominating cost vector c_prime.

    :param c: A cost vector (tuple of integers).
    :param c_prime: Another cost vector (tuple of integers).
    :return: True if c is dominating c_prime, False otherwise.
    """
    # Check if all elements in c are less than or equal to corresponding elements in c_prime
    # and c is not equal to c_prime
    dominated = False
    if isinstance(c, set):
        # 将集合中的所有非 None 子集合扁平化为一个列表
        # print('ccccc')
        c = [item for sublist in c if sublist is not None for item in sublist]

    if c and c_prime:
        # print("c", c, "C_prime", c_prime)
        if all(c_j <= c_prime_j for c_j, c_prime_j in zip(c, c_prime)) and c != c_prime:
            dominated = True
    # else:
    #     dominated = False
    return dominated


def reconstruct_paths(SG, end, start):
    # Placeholder for the path reconstruction process from the search graph SG
    path = []
    current_node = end
    i = 0
    # print(SG)

    while current_node is not start:
        # print("i:", i)
        i += 1
        path.append(current_node)
        current_node = SG.get(current_node)  # 获取父节点
    path.append(start)

    return path[::-1]  # 反转路径


def eliminate_dominated(g_m, G_op_m, G_cl_m, OPEN):
    """
    Eliminate dominated vectors from G_op_m and G_cl_m.
    Also, remove corresponding entries from OPEN.

    :param g_m: The new cost vector.
    :param G_op_m: The set of cost vectors in G_op for node m.
    :param G_cl_m: The set of cost vectors in G_cl for node m.
    :param OPEN: The set of open alternatives.
    :return: Updated G_op_m, G_cl_m, and OPEN.
    """
    # Remove dominated vectors from G_op_m and G_cl_m
    new_G_op_m = {}  # 创建一个新的空字典
    new_G_cl_m = {}  # 创建一个新的空字典
    for key, value in G_op_m.items():  # 遍历 G_op_m 中的每个键值对
        # print('Value:', value)
        # print(g_m)
        V_list = list(value)
        if V_list and not is_dominated(g_m, V_list[0]):  # 检查值是否没有被 g_m 支配
            new_G_op_m[key] = value  # 如果没有被支配，添加到新字典中

    for key, value in G_cl_m.items():  # 遍历 G_cl_m 中的每个键值对
        V_list = list(value)
        if V_list and not is_dominated(g_m, V_list[0]):  # 检查值是否没有被 g_m 支配
            new_G_cl_m[key] = value  # 如果没有被支配，添加到新字典中

    G_cl_m = new_G_cl_m  # 更新 G_cl_m 为新的字典
    G_op_m = new_G_op_m  # 更新 G_op_m 为新的字典

    # G_op_m = {g for g in G_op_m if not is_dominated(G_op_m[g], g_m)}
    # G_cl_m = {g for g in G_cl_m if not is_dominated(G_cl_m[g], g_m)}

    # Remove corresponding entries from OPEN
    OPEN = [alt for alt in OPEN if not is_dominated(g_m, alt[1])]

    return G_op_m, G_cl_m, OPEN


def heuristic_function(current_position, target_position):
    """
    Calculate a heuristic estimate from the current position to the target position.

    :param current_position: Tuple (x, y) representing the current position.
    :param target_position: Tuple (x, y) representing the target position.
    :param max_speed: Maximum speed in the network.
    :param min_fuel_rate: Minimum fuel consumption rate.
    :return: Tuple of heuristic time and fuel cost estimates.
    """
    max_speed = 10
    min_fuel_rate = 0.5
    # Calculate straight line distance
    distance = (target_position[0] - current_position[0]) + (target_position[1] - current_position[1])

    # Time estimate based on maximum speed
    time_estimate = distance / max_speed

    # Fuel estimate based on minimum fuel rate and time estimate
    fuel_estimate = time_estimate * min_fuel_rate

    return time_estimate, fuel_estimate

# # Example usage
# # Replace 'point_a' and 'point_b' with actual points from your network
# point_a = airport_cepo.points[0].xy  # Current position
# point_b = airport_cepo.points[-1].xy  # Target position
# max_speed = max([line.speed for line in airport_cepo.lines if line.speed > 0])  # Maximum speed in the network
# min_fuel_rate = X  # Minimum fuel consumption rate (replace X with actual value)


def AMOA_star(start, end, costs, graph, time_windows, start_time, out_angles, in_angles, Stand):
    SG = {}  # Acyclic search graph
    G_op = {start: {(0, 0)}}
    G_cl = {start: set()}
    OPEN = [(start, (0, 0), (0, 0))]
    COSTS = set()
    i = 0

    while OPEN:
        # print(i)
        i += 1
        n, g_n, f_n = select_from_open(OPEN)
        OPEN.remove((n, g_n, f_n))
        # print(n, g_n, f_n)
        # print(G_op)
        # print(G_cl)
        exists_in_G_op = any(g_n in value_set for value_set in G_op.values())
        if exists_in_G_op:
            key_to_remove = [k for k, v in G_op.items() if g_n in v][0]  # 假设 g_n 只在一个键的值集合中
            # print("key_to:", key_to_remove)
            G_op.pop(key_to_remove)

        if n in G_cl:
            # print("22222")
            G_cl[n].add(g_n)
        else:
            # print("33333")
            G_cl[n] = {g_n}

        if n == end:
            print("n == end")
            COSTS.add(g_n)
            OPEN = [alt for alt in OPEN if not is_dominated(g_n, alt[2])]
            if not OPEN:
                path = reconstruct_paths(SG, end, start)
                return path, COSTS
        else:
            for segment in graph[n]:
                # print(segment)
                m = segment[1]  # Assuming segment identifies the end node

                # 检查next_vertex是否在Stand中，并且不是目标点
                if m in Stand and m != end:
                    continue

                if len(SG) > 1:
                    s = SG[n]
                    ang_rad = out_angles[s][n] - in_angles[n][m]
                    delta = math.cos(ang_rad)  # if len(path) > 1 else 1
                    if (ang_rad / 3.141592653589793) == 1.5:
                        delta = 0  # 控制有1.5pi 等于0 实际为负数
                else:
                    delta = 1
                if 0 <= delta:
                    # C_n_m = read_cost_vector(n, m, costs)
                    if (n, m) in costs:
                        C_n_m = costs[(n, m)]
                        # print(C_n_m)

                    if len(C_n_m) > 2:  # Normal segment
                        for c_n_m_l in C_n_m:
                            n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time, C_n_m, c_n_m_l, segment = \
                                expand(n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows,
                                       start_time, C_n_m, c_n_m_l, segment)
                    else:  # Turn segment
                        c_n_m_l = C_n_m
                        n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time, C_n_m, c_n_m_l, segment = \
                            expand(n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows,
                                   start_time, C_n_m, c_n_m_l, segment)

    path = reconstruct_paths(SG, n, start)
    # path = None
    COSTS = None
    return path, COSTS


def expand(n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time, C_n_m, c_n_m_l, segment):
    # for segment in graph[n]:
    #     # print(segment)
    #     m = segment[1]  # Assuming segment identifies the end node
    #     # C_n_m = read_cost_vector(n, m, costs)
    #     C_n_m = costs[(n, m)]
    #
    #     if len(C_n_m) > 2:
    # for c_n_m_l in C_n_m:
    #     # print(C_n_m)
    #     # print("hhhhh", c_n_m_l)
    #     加入角度（），单行道（），Pushback（）
    check, holding_enabled, holding_cost = check_time_windows(segment, time_windows, c_n_m_l, G_op, G_cl,
                                                              start_time)
    # check = True
    if not check:
        #  holding_enabled is Boolean type
        if holding_enabled:
            # print("Holding_enable")
            c_n_m_l = add_holding_cost(c_n_m_l, holding_cost)
        else:
            # print("No_Holding_enable")
            return n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows,start_time, C_n_m, c_n_m_l, segment

    g_m = tuple(sum(x) for x in zip(g_n, c_n_m_l))
    if m not in SG:
        f_m = tuple(sum(x) for x in zip(g_m, heuristic_function(m, end)))
        # print("f_m:", f_m)
        # print("m not in SG")
        # if not is_dominated(f_m, COSTS):
        # print("COSTS:", COSTS, f_m)
        if not is_dominated(COSTS, f_m):
            # print('f_m is not dominated by COSTS')
            OPEN.append((m, g_m, f_m))
            G_op[m] = {g_m}
            SG[m] = n
    else:
        # print('22222')
        if g_m in G_op.get(m, set()).union(G_cl.get(m, set())):
            # print('g_m in G_op.get(m, set()) or g_m in G_cl.get(m, set())')
            SG[m] = n
        elif not any(is_dominated(other, g_m) for other in G_op.get(m, set()).union(G_cl.get(m, set()))):
            # print('not any(is_dominated(g_m, other) for other in G_op.get(m, set()).union(G_cl.get(m, set())))')
            # eliminate_dominated(g_m, G_op.get(m, set()).union(G_cl.get(m, set())))
            G_op, G_cl, OPEN = eliminate_dominated(g_m, G_op, G_cl, OPEN)
            f_m = tuple(sum(x) for x in zip(g_m, heuristic_function(m, end)))
            if not is_dominated(COSTS, f_m):
                # print('f_m is not dominated by COSTS')
                OPEN.append((m, g_m, f_m))
                G_op[m] = {g_m}
                SG[m] = n
        # print(SG)
    return n, m, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time, C_n_m, c_n_m_l, segment