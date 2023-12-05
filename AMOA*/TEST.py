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
        # if in G_cl
        if n in G_op and G_op[n] != set():
            # print(G_op[n])
            current_time = start_time + int(next(iter(G_op[n]))[0])
        elif n in G_cl and G_cl[n] != set():
            # print(next(iter(G_cl[n]))[0])
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
    Select the alternative from OPEN with the smallest fn value.

    :param OPEN: A list of tuples, where each tuple is of the form (n, gn, fn).
    :return: The tuple from OPEN with the smallest fn value.
    """
    # Find the alternative with the smallest fn value
    return min(OPEN, key=lambda x: x[2][1])


def is_dominated(c, c_prime):
    """
    Determine if cost vector c is dominated by cost vector c_prime.

    :param c: A cost vector (tuple of integers).
    :param c_prime: Another cost vector (tuple of integers).
    :return: True if c is dominated by c_prime, False otherwise.
    """
    # Check if all elements in c are less than or equal to corresponding elements in c_prime
    # and c is not equal to c_prime
    dominated = False
    if all(c_j <= c_prime_j for c_j, c_prime_j in zip(c, c_prime)) and c != c_prime:
        dominated = True
    return dominated


def reconstruct_paths(SG, end):
    # Placeholder for the path reconstruction process from the search graph SG
    path = []
    current_node = end

    while current_node is not None:
        path.append(current_node)
        current_node = SG.get(current_node)  # 获取父节点

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
    G_op_m = {g for g in G_op_m if not is_dominated(g, g_m)}
    G_cl_m = {g for g in G_cl_m if not is_dominated(g, g_m)}

    # Remove corresponding entries from OPEN
    OPEN = [alt for alt in OPEN if not is_dominated(alt[1], g_m)]

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
    max_speed = 20
    min_fuel_rate = 0.5
    # Calculate straight line distance
    distance = math.sqrt((target_position[0] - current_position[0]) ** 2 +
                         (target_position[1] - current_position[1]) ** 2)

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


def AMOA_star(start, end, costs, graph, time_windows, start_time):
    SG = {}  # Acyclic search graph
    G_op = {start: {(0, 0)}}
    G_cl = {start: set()}
    OPEN = [(start, (0, 0), (0, 0))]
    COSTS = set()
    i = 0

    while OPEN:
        print(i)
        i += 1
        n, g_n, f_n = select_from_open(OPEN)
        OPEN.remove((n, g_n, f_n))
        G_op[n].remove(g_n)
        G_cl[n].add(g_n)

        if n == end:
            COSTS.add(g_n)
            OPEN = [alt for alt in OPEN if not is_dominated(g_n, alt[2])]
        else:
            n, g_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows =\
                expand(n, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time)

    path = reconstruct_paths(SG, end)
    return path, COSTS


def expand(n, g_n, f_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows, start_time):
    for segment in graph[n]:
        # print(segment)
        m = segment[1]  # Assuming segment identifies the end node
        # C_n_m = read_cost_vector(n, m, costs)
        C_n_m = costs[(n, m)]

        for c_n_m_l in C_n_m:
            print(C_n_m)
            print("hhhhh", c_n_m_l)
            check, holding_enabled, holding_cost = check_time_windows(segment, time_windows, c_n_m_l, G_op, G_cl, start_time)
            if not check:
                #  holding_enabled is Boolean type
                if holding_enabled:
                    c_n_m_l = add_holding_cost(c_n_m_l, holding_cost)
                else:
                    continue

            g_m = tuple(sum(x) for x in zip(g_n, c_n_m_l))
            if m not in SG:
                f_m = tuple(sum(x) for x in zip(g_m, heuristic_function(m, end)))
                if not is_dominated(f_m, COSTS):
                    OPEN.append((m, g_m, f_m))
                    G_op[m] = {g_m}
                    SG[m] = n
            else:
                if g_m in G_op.get(m, set()) or g_m in G_cl.get(m, set()):
                    SG[m] = n
                elif not any(is_dominated(g_m, other) for other in G_op.get(m, set()).union(G_cl.get(m, set()))):
                    # eliminate_dominated(g_m, G_op.get(m, set()).union(G_cl.get(m, set())))
                    G_op, G_cl, OPEN = eliminate_dominated(g_m, G_op, G_cl, OPEN)
                    f_m = tuple(sum(x) for x in zip(g_m, heuristic_function(m, end)))
                    if not is_dominated(f_m, COSTS):
                        OPEN.append((m, g_m, f_m))
                        G_op[m] = {g_m}
                        SG[m] = n
    return n, g_n, SG, G_op, G_cl, OPEN, COSTS, end, costs, graph, time_windows