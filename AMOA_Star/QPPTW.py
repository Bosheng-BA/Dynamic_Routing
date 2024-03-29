from heapdict import heapdict
import math
import heapq
import Cst
# fib_heap = heapdict()


def Readjustment_time_windows(graph, weights, time_windows, path):
    updated_time_windows = time_windows.copy()  # Create a copy of the original time windows

    for i, reservation in enumerate(path):
        if i == len(path)-1:
            break
        edge = (reservation[0], path[i+1][0])
        for i, time_window in enumerate(updated_time_windows[edge]):
            aj_e, bj_e = time_window
            timein_f, timeout_f = reservation[1]

            if timeout_f <= aj_e:
                # Time-window is too late, move to the next conflicting edge
                break
            elif timein_f < bj_e:
                # Time-window is too early, move to the next conflicting edge
                continue
            elif timein_f < aj_e + weights[edge]:
                if bj_e - weights[edge] < timeout_f:
                    # Remove Fj_e from F(e)
                    updated_time_windows[edge].pop(i)
                else:
                    # Shorten the start of the time-window
                    updated_time_windows[edge][i] = (timeout_f, bj_e)
            else:
                if bj_e - weights[edge] < timeout_f:
                    # Shorten the end of the time-window
                    updated_time_windows[edge][i] = (aj_e, timein_f)
                else:
                    # Split the time-window
                    updated_time_windows[edge][i] = (aj_e, timein_f)
                    updated_time_windows[edge].insert(i + 1, (timeout_f, bj_e))
        # for edge in conflicting_edges[reservation]:

    return updated_time_windows


def Readjustment_time_windows0(graph, weights, time_windows, path):
    updated_time_windows = time_windows.copy()

    for i, label in enumerate(path):
        if i == len(path) - 1:
            break
        edge = (label[0], path[i + 1][0])

        (edge_start, edge_end) = label[1]
        j = 0
        while j < len(updated_time_windows[edge]):
            (window_start, window_end) = updated_time_windows[edge][j]

            if edge_end <= window_start:
                break
            if edge_start <= window_end:
                if edge_start < window_start + weights[edge]:
                    if window_end - weights[edge] < edge_end:
                        updated_time_windows[edge].pop(j)
                        continue
                    else:
                        updated_time_windows[edge][j] = (edge_end, window_end)
                else:
                    if window_end - weights[edge] < edge_end:
                        updated_time_windows[edge].pop(j)
                        updated_time_windows[edge].insert(j, (window_start, edge_start))
                    else:
                        updated_time_windows[edge][j] = (window_start, edge_start)
                        updated_time_windows[edge].insert(j + 1, (edge_end, window_end))
                        j += 1
            j += 1
    return updated_time_windows


def QPPTW_algorithm(graph, weights, time_windows, source, target, start_time, in_angles, out_angles, Stand):
    # 初始化一个空的斐波那契堆
    # fib_heap = heapdict()
    global new_label
    heap = []

    # heap = []
    labels = {v: [] for v in graph.keys()}

    # Create initial label for the source vertex
    time_i = start_time
    initial_label = (source, (start_time, float('inf')), None)
    # heapq.heappush(heap, (start_time, initial_label))
    labels[source].append(initial_label)

    heapq.heappush(heap, (start_time, initial_label))

    # 创建一个节点并插入堆中，使用时间作为键值
    # fib_heap[time_i] = initial_label
    pathlist = []

    while heap:
        # 分解标签 L 中的元素
        # min_time, min_label_L = heap.popitem()
        min_time, min_label_L = heapq.heappop(heap)
        # time_cost = 0

        current_time = min_time
        (current_vertex, (current_start, current_end), prev_label) = min_label_L

        # If the current vertex is the target, reconstruct the path and return
        if current_vertex == target:
            time_cost = 0
            path = []
            path.append((current_vertex, (current_start, current_end), prev_label))
            endtime = current_end
            starttime = None
            while prev_label:
                path.append(prev_label)
                current_vertex, _, prev_label = prev_label
                starttime = _[0]
                # print(starttime)
            path.reverse()
            new_time_windows = Readjustment_time_windows(graph, weights, time_windows, path)
            if starttime:
                time_cost = endtime - starttime
            # print(time_cost)
            return path, path, new_time_windows, time_cost

        if current_vertex != target:
            path_for_test = []
            path_for_test.append((current_vertex, (current_start, current_end), prev_label))
            new_prev = prev_label
            while new_prev:
                path_for_test.append(new_prev)
                current_vertex_, _, new_prev = new_prev
            path_for_test.reverse()
        path = [label[0] for label in path_for_test]
        pathlist.append(path)

        # Explore outgoing edges from the current vertex
        for edge in graph[current_vertex]:
            _, next_vertex = edge  # looking for the next vertex

            # 检查next_vertex是否在Stand中，并且不是目标点
            if next_vertex in Stand and next_vertex != target:
                continue

            if len(path_for_test) > 1:
                path = [label[0] for label in path_for_test]
                # print(path, current_vertex, next_vertex)
                ang_rad = out_angles[path[-2]][current_vertex] - in_angles[current_vertex][next_vertex]
                delta = math.cos(ang_rad)  # if len(path) > 1 else 1
                if (ang_rad / 3.141592653589793) == 1.5:
                    delta = 0  # 控制有1.5pi 等于0 实际为负数
            else:
                delta = 1
            if 0 <= delta :
                # 加入角度约束
                for window_start, window_end in time_windows[edge]:
                    if current_end < window_start:
                        break
                    new_start = max(window_start, current_start)  # Use edge as key
                    new_end = new_start + weights[edge]  # Use edge as key

                    # Create a new label
                    if new_end <= window_end:
                        new_label = (
                            next_vertex, (new_end, window_end),
                            (current_vertex, (current_start, current_end), prev_label))

                    # Check dominance with existing labels
                    dominated = False
                    for existing_label in labels[next_vertex]:
                        existing_start = existing_label[1][0]
                        existing_end = existing_label[1][1]
                        # if next_vertex in Stand:
                        #     dominated = True
                        #     labels[next_vertex].remove(existing_label)
                        #     # if existing_label[1][0] in heap.keys():
                        #     if existing_label[1][0] in heap:
                        #         del heap[existing_label[1][0]]
                        #     break
                        if existing_start < new_end and window_end <= existing_end:
                            dominated = True
                            break
                        # # elif (new_start, new_end) <= existing_label[1]:
                        if new_end <= existing_start and existing_end <= window_end:
                            labels[next_vertex].remove(existing_label)
                            # if existing_label[1][0] in heap.keys():
                            if existing_label[1][0] in heap:
                                del heap[existing_label[1][0]]
                            break

                    if not dominated:
                        labels[next_vertex].append(new_label)
                        # heap[new_end] = new_label
                        heapq.heappush(heap, (new_end, new_label))
    """path_for_test"""
    return None, pathlist, time_windows, float('inf')


