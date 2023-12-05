from heapdict import heapdict
import math

def contains_key(fib_heap, key_to_check):
    for node in fib_heap:
        if node.key == key_to_check:
            return True
    return False
fib_heap = heapdict()
def QPPTW_algorithm(graph, weights, time_windows, source, target, start_time, in_angles, out_angles):
    """此版本存在的问题是当 Key值为 26566 与 26574 的时候，在堆的最小值的索引会出现索引到26574为最小"""
    # 初始化一个空的斐波那契堆
    # fib_heap = heapdict()

    # heap = []
    labels = {v: [] for v in graph.keys()}
    # if ((21566,7465), (21606, 7324)) in graph[(21566, 7465)]:
    #     graph[(21566, 7465)].remove(((21566,7465), (21606, 7324)))

    # Create initial label for the source vertex
    time_i = start_time
    initial_label = (source, (start_time, float('inf')), None)
    # print("start_time:", start_time)
    # heapq.heappush(heap, (start_time, initial_label))
    labels[source].append(initial_label)

    # 创建一个节点并插入堆中，使用时间作为键值
    fib_heap[time_i] = initial_label
    pathlist = []

    while fib_heap:
        # 分解标签 L 中的元素
        # print(len(fib_heap), "111")
        min_time, min_label_L = fib_heap.popitem()
        # num_elements = len(fib_heap)
        # print('num', num_elements)
        # min_time = next(iter(fib_heap))  # 获取堆中的第一个键
        # min_label_L = fib_heap[min_time]
        # fib_heap[min_time] = min_label_L
        # print(len(fib_heap),"222")
        # if contains_key(fib_heap, 26566):
        #     label_0 = fib_heap
        #     print("Fibonacci Heap 包含键值为 26566 的元素")
        # else:
        #     print("Fibonacci Heap 不包含键值为 26566 的元素")

        current_time = min_time
        (current_vertex, (current_start, current_end), prev_label) = min_label_L

        # If the current vertex is the target, reconstruct the path and return
        if current_vertex == target:
            path = []
            path.append((current_vertex, (current_start, current_end), prev_label))
            while prev_label:
                path.append(prev_label)
                current_vertex, _, prev_label = prev_label
            path.reverse()
            return path, path

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

        if current_vertex == (22622, 8509):
            current_vertex0 = current_vertex

        # Explore outgoing edges from the current vertex
        for edge in graph[current_vertex]:
            _, next_vertex = edge  # looking for the next vertex
            if current_vertex == (22622, 8509):
                num_elements = len(fib_heap)
                print('num', num_elements)
                ########需要判断26566是不是在这个堆里
            check = False
            if 26566.37133895767 in fib_heap:
                check = True
            if len(path_for_test) > 1:
                path = [label[0] for label in path_for_test]
                # print(path, current_vertex, next_vertex)
                ang_rad = out_angles[path[-2]][current_vertex] - in_angles[current_vertex][next_vertex]
                delta = math.cos(ang_rad)  # if len(path) > 1 else 1
                if (ang_rad / 3.141592653589793) == 1.5:
                    delta = 0  # 控制有1.5pi 等于0 实际为负数
            else:
                delta = 1
            if 0 <= delta:
                # print('edge:'+str(edge), 'next_vertex:'+str(next_vertex))
                # 加入角度约束
                for window_start, window_end in time_windows[edge]:
                    # print('windoe_start'+str(window_start), 'window_end'+str(window_end))
                    # if current_start > window_end:
                    #     continue
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
                        # print("existing_label:", existing_label[1], "new_label:", new_label[1], new_label[0])
                        existing_start = existing_label[1][0]
                        existing_end = existing_label[1][1]
                        if existing_start < new_end and window_end <= existing_end:
                            dominated = True
                            break
                        # # elif (new_start, new_end) <= existing_label[1]:
                        if new_end <= existing_start and existing_end <= window_end:
                            labels[next_vertex].remove(existing_label)
                            # keys = list(fib_heap.keys())
                            # print(keys)
                            if existing_label[1][0] in fib_heap.keys():
                                # print("444444")
                                del fib_heap[existing_label[1][0]]
                            break

                    if not dominated:
                        labels[next_vertex].append(new_label)
                        fib_heap[new_end] = new_label
                        # heapq.heappush(heap, (new_start, new_label))
    # print(len(fib_heap))
    """path_for_test"""
    return None, pathlist
    # return None  # No path found

    # def QPPTW_algorithm(graph, weights, time_windows, source, target, start_time, in_angles, out_angles):
    # # 初始化一个空的斐波那契堆
    # fib_heap = Fib(0, 0)
    #
    # # heap = []
    # labels = {v: [] for v in graph.keys()}
    #
    # # Create initial label for the source vertex
    # time_i = start_time
    # initial_label = (source, (start_time, float('inf')), None)
    # # heapq.heappush(heap, (start_time, initial_label))
    # labels[source].append(initial_label)
    #
    # # 创建一个节点并插入堆中，使用时间作为键值
    # node = FibNode(initial_label)
    # fib_heap.insert(node)
    #
    # # 插入 L 到斐波那契堆 H
    # # fib_heap.insert(initial_label)
    # # path_for_test = []
    #
    # while fib_heap.n > 0:
    #     # 分解标签 L 中的元素
    #     min_node = fib_heap.extract_min()
    #
    #     # 分解标签 L 中的元素
    #     vL, IL, predL = min_node.key
    #     aL, bL = IL
    #
    #     # 现在您可以在这里对 L 做任何操作
    #     # ...
    #
    #     # 示例：输出最小标签的元素
    #     print("vL:", vL)
    #     print("IL:", IL)
    #     print("predL:", predL)
    #
    #     current_time, (current_vertex, (current_start, current_end), prev_label) = heapq.heappop(heap)
    #     # print('current_end:  ' + str(current_end))
    #
    #     # If the current vertex is the target, reconstruct the path and return
    #     if current_vertex == target:
    #         path = []
    #         path.append((current_vertex, (current_start, current_end), prev_label))
    #         while prev_label:
    #             path.append(prev_label)
    #             current_vertex, _, prev_label = prev_label
    #         path.reverse()
    #         return path, path
    #
    #     if current_vertex != target:
    #         path_for_test = []
    #         path_for_test.append((current_vertex, (current_start, current_end), prev_label))
    #         new_prev = prev_label
    #         while new_prev:
    #             path_for_test.append(new_prev)
    #             current_vertex_, _, new_prev = new_prev
    #         path_for_test.reverse()
    #
    #     # Explore outgoing edges from the current vertex
    #     for edge in graph[current_vertex]:
    #         _, next_vertex = edge  # looking for the next vertex
    #         if len(path_for_test) > 1:
    #             path = [label[0] for label in path_for_test]
    #             # print(path, current_vertex, next_vertex)
    #             ang_rad = out_angles[path[-2]][current_vertex] - in_angles[current_vertex][next_vertex]
    #             delta = math.cos(ang_rad)  # if len(path) > 1 else 1
    #             if (ang_rad / 3.141592653589793) == 1.5:
    #                 delta = 0  # 控制有1.5pi 等于0 实际为负数
    #         else:
    #             delta = 1
    #         if 0 <= delta:
    #             # print('edge:'+str(edge), 'next_vertex:'+str(next_vertex))
    #             # 加入角度约束
    #             for window_start, window_end in time_windows[edge]:
    #                 # print('windoe_start'+str(window_start), 'window_end'+str(window_end))
    #                 if current_start > window_end:
    #                     continue
    #                 if current_end < window_start:
    #                     break
    #                 new_start = max(window_start, current_start)  # Use edge as key
    #                 new_end = new_start + weights[edge]  # Use edge as key
    #
    #                 # Create a new label
    #                 if new_end <= window_end:
    #                     new_label = (
    #                         next_vertex, (new_end, window_end),
    #                         (current_vertex, (current_start, current_end), prev_label))
    #
    #                 # Check dominance with existing labels
    #                 dominated = False
    #                 for existing_label in labels[next_vertex]:
    #                     print(existing_label[1], new_label[1])
    #                     existing_start = existing_label[1][0]
    #                     existing_end = existing_label[1][1]
    #                     if existing_start <= new_end and existing_end >= new_start:
    #                         dominated = True
    #                         break
    #                     # # elif (new_start, new_end) <= existing_label[1]:
    #                     if existing_start > new_end and existing_end < new_start:
    #                         labels[next_vertex].remove(existing_label)
    #                         heapq.heappop(heap)  # Remove from heap
    #                         break
    #                     # elif existing_label[1] <= (new_start, new_end):
    #                     #     dominated = True
    #                     #     break
    #
    #                     # if existing_label[1] <= (new_end, window_end):
    #                     #     dominated = True
    #                     #     break
    #                     # if (new_end, window_end) <= existing_label[1]:
    #                     #     labels[next_vertex].remove(existing_label)
    #                     #     heapq.heappop(heap)  # Remove from heap
    #                     #     break
    #
    #                 if not dominated:
    #                     labels[next_vertex].append(new_label)
    #                     heapq.heappush(heap, (new_start, new_label))
    #
    # return None, path_for_test
    # # return None  # No path found


def Readjustment_time_windows(graph, weights, time_windows, path):
    for label in range(len(path)):
        (edge_start, edge_end) = label[1]
        for edge in graph[label[0]]:
            for (window_start, window_end) in time_windows(edge):
                if edge_end <= window_start:
                    break
                if edge_start <= window_end:
                    if edge_start < window_start + weights(edge):
                        if window_end - weights(edge) < edge_end:
                            time_windows(edge).pop((window_start, window_end))
                        else:
                            time_windows(edge).pop((window_start, window_end))
                            time_windows(edge).apprend((edge_end, window_end))
                    else:
                        if window_end - weights(edge) < edge_end:
                            time_windows(edge).pop((window_start, window_end))
                            time_windows(edge).apprend((window_start, edge_start))
                        else:
                            time_windows(edge).apprend((window_start, edge_start))
    new_time_windows = time_windows
    return new_time_windows

# # Example usage
# graph = {
#     'A': [('A', 'B'), ('A', 'C')],
#     'B': [('B', 'D'), ('B', 'E')],
#     'C': [('C', 'E')],
#     'D': [('D', 'F')],
#     'E': [('E', 'F')],
#     'F': [('F', 'G')],
#     'G': []
# }
#
# weights = {
#     ('A', 'B'): 4,
#     ('A', 'C'): 3,
#     ('B', 'D'): 2,
#     ('B', 'E'): 3,
#     ('C', 'E'): 1,
#     ('D', 'F'): 2,
#     ('E', 'F'): 2,
#     ('F', 'G'): 3
# }
#
# time_windows = {
#     ('A', 'B'): [(0, 5)],
#     ('A', 'C'): [(0, 4)],
#     ('B', 'D'): [(2, 6)],
#     ('B', 'E'): [(3, 7)],
#     ('C', 'E'): [(1, 5)],
#     ('D', 'F'): [(4, 8)],
#     ('E', 'F'): [(3, 6)],
#     ('F', 'G'): [(7, 9)]
# }
#
# source = 'A'
# target = 'G'
# start_time = 0
#
# result = QPPTW_algorithm(graph, weights, time_windows, source, target, start_time)
# if result:
#     print("Quickest Path:", [label[0] for label in result])
# else:
#     print("No path found.")
