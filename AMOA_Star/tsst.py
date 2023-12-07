import heapq


def QPPTW_algorithm0(graph, weights, time_windows, source, target, start_time):
    heap = []
    labels = {v: [] for v in graph.keys()}

    # Create initial label for the source vertex
    initial_label = (source, (start_time, float('inf')), None)
    heapq.heappush(heap, (start_time, initial_label))
    labels[source].append(initial_label)

    while heap:
        current_time, (current_vertex, (current_start, current_end), prev_label) = heapq.heappop(heap)

        # If the current vertex is the target, reconstruct the path and return
        if current_vertex == target:
            path = []
            while prev_label:
                path.append(prev_label)
                current_vertex, _, prev_label = prev_label
            path.reverse()
            return path

        # Explore outgoing edges from the current vertex
        for next_vertex in graph[current_vertex]:
            edge = (current_vertex, next_vertex)
            for window_start, window_end in time_windows[edge]:
                if current_end <= window_start:
                    continue
                new_start = max(window_start, current_start) + weights[edge]
                new_end = new_start + weights[edge]

                # Create a new label
                new_label = (
                next_vertex, (new_start, new_end), (current_vertex, (current_start, current_end), prev_label))

                # Check dominance with existing labels
                dominated = False
                for existing_label in labels[next_vertex]:
                    if existing_label[1] <= (new_start, new_end):
                        dominated = True
                        break
                    if (new_start, new_end) <= existing_label[1]:
                        labels[next_vertex].remove(existing_label)
                        heapq.heappop(heap)  # Remove from heap
                        break

                if not dominated:
                    labels[next_vertex].append(new_label)
                    heapq.heappush(heap, (new_start, new_label))

    return None  # No path found


def QPPTW_algorithm(graph, weights, time_windows, source, target, start_time):
    heap = []
    labels = {v: [] for v in graph.keys()}
    # print(weights)
    # print(time_windows)

    # Create initial label for the source vertex
    initial_label = (source, (start_time, float('inf')), None)
    heapq.heappush(heap, (start_time, initial_label))
    labels[source].append(initial_label)

    while heap:
        current_time, (current_vertex, (current_start, current_end), prev_label) = heapq.heappop(heap)
        # print('current_end:  ' + str(current_end))

        # If the current vertex is the target, reconstruct the path and return
        if current_vertex == target:
            path = []
            while prev_label:
                path.append(prev_label)
                current_vertex, _, prev_label = prev_label
            path.reverse()
            return path

        # Explore outgoing edges from the current vertex
        for edge in graph[current_vertex]:
            _, next_vertex = edge  # looking for the next vertex
            # print('edge:'+str(edge), 'next_vertex:'+str(next_vertex))
            for window_start, window_end in time_windows[edge]:
                # print('windoe_start'+str(window_start), 'window_end'+str(window_end))
                if current_end <= window_start:
                    continue
                new_start = max(window_start, current_start) + weights[edge]  # Use edge as key
                new_end = new_start + weights[edge]  # Use edge as key

                # Create a new label
                new_label = (
                next_vertex, (new_start, new_end), (current_vertex, (current_start, current_end), prev_label))

                # Check dominance with existing labels
                dominated = False
                for existing_label in labels[next_vertex]:
                    if existing_label[1] <= (new_start, new_end):
                        dominated = True
                        break
                    if (new_start, new_end) <= existing_label[1]:
                        labels[next_vertex].remove(existing_label)
                        heapq.heappop(heap)  # Remove from heap
                        break

                if not dominated:
                    labels[next_vertex].append(new_label)
                    heapq.heappush(heap, (new_start, new_label))

    return None  # No path found


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
