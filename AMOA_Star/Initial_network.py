
import airport
import os.path
import geo
import Cst
import random
import helpfunction

APT_FILE = Cst.APT_FILE
airport_cepo = airport.load2(APT_FILE)
airport_init = airport.load(APT_FILE)


def calculate_cost(length, speed, fuel_rate):
    """
    Calculate the time and fuel cost for a segment at a given speed.

    :param length: Length of the segment in meters.
    :param speed: Speed in m/s.
    :param fuel_rate: Fuel consumption rate in liters per second.
    :return: Tuple of time cost (in seconds) and fuel cost (in liters).
    """
    time_cost = abs(length / speed)  # Time to travel the segment
    fuel_cost = time_cost * fuel_rate  # Total fuel consumed
    return time_cost, fuel_cost


def initial_network(airport_cepo):
    graph = {}
    weights = {}
    network = {}
    in_angles = {}
    out_angles = {}
    time_windows = {}
    # print("the number of points", len(airport_cepo.points))
    # points, lines, runways = [], [], []
    points = airport_cepo.points
    runways = airport_cepo.runways
    lines = airport_cepo.lines
    init_lines = airport_init.lines
    points0 = airport_init.points
    pushback_edges = []

    for (i, point) in enumerate(points):
        network[point.xy] = {}
        in_angles[point.xy] = {}
        out_angles[point.xy] = {}
        graph[point.xy] = []
    for (i, line) in enumerate(lines):
        line_init = init_lines[i]
        length = geo.length(line_init.xys)
        length_cepo = abs(length / line.speed)
        # print(length)
        # p1 = (float(line_init.xys[0][0]), float(line_init.xys[0][1]))
        p11 = line_init.xys[0]
        p22 = line_init.xys[1]
        p33 = line_init.xys[-2]
        p44 = line_init.xys[-1]
        p1 = line.xys[0]
        # p2 = line.xys[1]
        # p3 = line.xys[-2]
        p4 = line.xys[-1]
        # print((p1, p4))
        # print('length', len(points), len())

        if length == 0.0:
            print('Line = 0', line.oneway, line.taxiway)

        while length != 0.0:  # ignore the line with length '0'
            # network[p1][p4] = length_cepo
            # network[p4][p1] = length_cepo
            if (p1, p4) not in graph[p1]:
                graph[p1].append((p1, p4))
            if (p4, p1) not in graph[p4]:
                graph[p4].append((p4, p1))

            weights[(p1, p4)] = length_cepo
            weights[(p4, p1)] = length_cepo
            time_windows[(p1, p4)] = [(0, 24 * 60 * 60)]
            time_windows[(p4, p1)] = [(0, 24 * 60 * 60)]
            if line.speed < 0:  # Give the angle of every arc and reverse the pushback's outangle
                in_angles[p1][p4] = geo.angle_2p(p11, p22)
                out_angles[p1][p4] = geo.angle_2p(p44, p33)
                in_angles[p4][p1] = geo.angle_2p(p44, p33)
                out_angles[p4][p1] = geo.angle_2p(p22, p11)
                pushback_edges.append((p1, p4))
            else:
                in_angles[p1][p4] = geo.angle_2p(p11, p22)
                out_angles[p1][p4] = geo.angle_2p(p33, p44)
                in_angles[p4][p1] = geo.angle_2p(p44, p33)
                out_angles[p4][p1] = geo.angle_2p(p22, p11)
            length = 0.0  # 注意浮点型
            if line.oneway:  # 处理路网单向路
                # print(line.oneway)
                # time_windows[(p4, p1)] = [(0, 0)]
                graph[p4].remove((p4, p1))

    for (i, runway) in enumerate(runways):
        p1 = runway.xys[0]
        p2 = runway.xys[1]
        if (p1, p2) not in graph[p1]:
            graph[p1].append((p1, p2))
        if (p2, p1) not in graph[p2]:
            graph[p2].append((p2, p1))
        length = geo.length(runway.xys)
        weights[(p1, p2)] = length
        weights[(p2, p1)] = length
        time_windows[(p1, p2)] = [(0, 24 * 60 * 60)]
        time_windows[(p2, p1)] = [(0, 24 * 60 * 60)]
        # network[p1][p2] = length
        # network[p2][p1] = length
        in_angles[p1][p2] = geo.angle_2p(p1, p2)
        out_angles[p1][p2] = geo.angle_2p(p1, p2)
        in_angles[p2][p1] = geo.angle_2p(p2, p1)
        out_angles[p2][p1] = geo.angle_2p(p2, p1)

    # Initialize the cost matrix for each segment
    costs = {}

    # Assuming speeds and fuel_consumption_rate are defined
    V1 = 5
    V2 = 10
    V3 = 15
    X = 0.5
    speeds = [V1, V2, V3]  # Replace with actual values
    speeds2 = [2.5, 5, 7.5]
    fuel_consumption_rate = X  # Replace with actual value

    for (i, line) in enumerate(lines):

        p1 = line.xys[0]
        p4 = line.xys[-1]
        length = geo.length(line_init.xys)  # Assuming this is the length of the segment

        if line.speed < 0:
            speed = line.speed
            costs[(p4, p1)] = costs[(p1, p4)] = calculate_cost(length, speed, fuel_consumption_rate)
            # costs[(p4, p1)] = costs[(p1, p4)] = [calculate_cost(length, speed, fuel_consumption_rate) for speed in speeds2]
            # calculate_cost(length, speed, fuel_consumption_rate)
        else:
            # Calculate cost for each speed
            speed = 10
            costs[(p4, p1)] = costs[(p1, p4)] = calculate_cost(length, speed, fuel_consumption_rate)
            # costs[(p4, p1)] = costs[(p1, p4)] = [calculate_cost(length, speed, fuel_consumption_rate) for speed in speeds]
            # costs[(p4, p1)] = [calculate_cost(length, speed, fuel_consumption_rate) for speed in speeds]

    # Now, `costs` dictionary contains the time and fuel costs for each segment at different speeds

    # for i in range(len(pointcoordlist)):  # 形成以节点序号为名称的路网
    #     network_cepo[i] = {}
    #     in_angles_cepo[i] = {}
    #     out_angles_cepo[i] = {}
    #     listkey = list(network[pointcoordlist[i]].keys())
    #     for (j, keys) in enumerate(listkey):
    #         key = pointcoordlist.index(keys)
    #         # print(key)
    #         network_cepo[i][key] = network[pointcoordlist[i]][keys]
    #         in_angles_cepo[i][key] = in_angles[pointcoordlist[i]][keys]
    #         out_angles_cepo[i][key] = out_angles[pointcoordlist[i]][keys]


    # print(network_cepo)

    # print_network_info(network, points)
    """********* print network **********"""
    # neighbor_info = helpfunction.turn_network(network)
    # helpfunction.print_neighbor_info(neighbor_info, points)
    return graph, weights, time_windows, in_angles, out_angles, costs, pushback_edges

# network, pointcoordlist, network_cepo, in_angles, out_angles, in_angles_cepo, out_angles_cepo = initial_network(airport_cepo);

# def findsource(points):
#     source_points = [p for p in points if p.ptype == 'Stand']
#     point = random.choice(source_points)
#     # point = points[-10]
#     print("Source:", point.ptype, point.name, point.xy)
#     source = point.xy
#     return source
#
#
# def finddes(points):
#     des_points = [p for p in points if p.ptype == 'Runway']
#     point = random.choice(des_points)
#     print("Destination:", point.ptype, point.name, point.xy)
#     des = point.xy
#     return des

