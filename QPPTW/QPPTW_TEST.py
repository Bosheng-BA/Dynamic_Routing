import heapq


class Label:
    def __init__(self, vertex, interval, predecessor):
        self.vertex = vertex
        self.interval = interval
        self.predecessor = predecessor

    def __lt__(self, other):
        return self.interval[0] < other.interval[0]


def quickest_path_with_time_windows(graph, weights, time_windows, source, target, start_time):
    heap = []
    labels = {v: [] for v in graph}

    label = Label(source, [start_time, float('inf')], None)
    heapq.heappush(heap, (start_time, label))
    labels[source].append(label)

    while heap:
        _, curr_label = heapq.heappop(heap)
        curr_vertex = curr_label.vertex

        if curr_vertex == target:
            return reconstruct_path(curr_label)

        for edge in graph[curr_vertex]:
            for time_window in sorted(time_windows[edge], key=lambda x: x[0]):
                a_window, b_window = time_window

                if a_window > curr_label.interval[1]:
                    break

                if b_window < curr_label.interval[0]:
                    continue

                time_in = max(curr_label.interval[0], a_window)
                time_out = time_in + weights[edge]

                if time_out <= b_window:
                    next_vertex = edge[1]
                    new_label = Label(next_vertex, [time_out, b_window], curr_label)

                    if dominates_any(labels[next_vertex], new_label):
                        continue

                    labels[next_vertex] = remove_dominated(labels[next_vertex], new_label)
                    heapq.heappush(heap, (new_label.interval[0], new_label))
                    labels[next_vertex].append(new_label)

    return "No route exists"


def reconstruct_path(label):
    path = []

    while label:
        path.append(label.vertex)
        label = label.predecessor

    return list(reversed(path))


def dominates_any(labels, new_label):
    for label in labels:
        if dominates(label, new_label):
            return True
    return False


def dominates(label1, label2):
    return label1.interval[0] <= label2.interval[0] and label1.interval[1] >= label2.interval[1]


def remove_dominated(labels, new_label):
    return [label for label in labels if not dominates(new_label, label)]


# Example usage
graph = {
    'A': [('A', 'B'), ('A', 'C')],
    'B': [('B', 'D'), ('B', 'E')],
    'C': [('C', 'E')],
    'D': [('D', 'F')],
    'E': [('E', 'F')],
    'F': [('F', 'G')],
    'G': []
}

weights = {
    ('A', 'B'): 4,
    ('A', 'C'): 3,
    ('B', 'D'): 2,
    ('B', 'E'): 3,
    ('C', 'E'): 1,
    ('D', 'F'): 2,
    ('E', 'F'): 2,
    ('F', 'G'): 3
}

time_windows = {
    ('A', 'B'): [(0, 5)],
    ('A', 'C'): [(0, 4)],
    ('B', 'D'): [(2, 6)],
    ('B', 'E'): [(3, 7)],
    ('C', 'E'): [(1, 5)],
    ('D', 'F'): [(4, 8)],
    ('E', 'F'): [(3, 6)],
    ('F', 'G'): [(7, 9)]
}

source = 'A'
target = 'G'
start_time = 0

route = quickest_path_with_time_windows(graph, weights, time_windows, source, target, start_time)
print("Route:", route)
