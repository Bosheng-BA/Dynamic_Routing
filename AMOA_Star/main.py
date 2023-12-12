import sys
import airport
import Initial_network
import datetime
import Sour_and_Des
# import Find_Routing
import json
import os
import Cst
import tsst
import TEST
import Draw_path

# above imported library
""" Default airport and traffic files """
DATA_PATH = "/Users/小巴的工作台/BBS_WORK_SPACE/Python_Workspace/airport/Datas/DATA"
APT_FILE = os.path.join(DATA_PATH, "tianjin_new.txt")
# FPL_FILE = os.path.join(DATA_PATH, "ZBTJ_20210725_Manex_STD.B&B.sim")
FPL_FILE = os.path.join(DATA_PATH, "ZBTJ_20210725_Manex_16R.B&B.sim")


# 函数，将列表写入到json文件
def write_list_to_json(list_name, filename):
    with open(filename, 'w') as f:
        json.dump(list_name, f)


# 函数，将列表写入到文件
def write_list_to_file(list_name, filename):
    with open(filename, 'w') as f:
        for item in list_name:
            f.write("%s\n" % item)


def show_point_name(point, points):
    for p in points:
        if p.xy[0] == point[0] and p.xy[1] == point[1]:
            point_name = p.name
            return point_name


def show_point_coor(point, points):
    for p in points:
        if p.name == point:
            point_xy = p.xy
            return point_xy


def get_node_lock_periods(pathlist, activation_times_list, network_cepo, flight, node_lock_periods):
    # 此处需要修稿time-windows的内容根据 前序路径
    # node_lock_periods = {}

    # for path_index in range(len(pathlist)):
    path = pathlist[-1]
    activation_times = activation_times_list[-1]
    if flight.departure == 'ZBTJ':
        startt = flight.ttot - 600
    else:
        startt = flight.aldt
    flight_start_time = startt
    # flight_start_time = 0

    for i in range(1, len(path) - 1):  # Start from the second node in the path
        node = path[i]
        prev_node = path[i - 1]
        next_node = path[i + 1]

        # The node should be locked as soon as the previous node is reached
        start_time = activation_times[i - 1] + flight_start_time
        end_time = start_time + network_cepo[prev_node][node]

        # Determine the end of the lock period based on the distance to the next node
        distance_to_next_node = network_cepo[node][next_node]
        if distance_to_next_node > 20:
            end_time += 20
        else:
            end_time += distance_to_next_node

        # Add the lock period to the node's list of lock periods
        if node not in node_lock_periods:
            node_lock_periods[node] = []
        node_lock_periods[node].append((start_time, end_time))

    return node_lock_periods


if __name__ == "__main__":
    fpl_file = sys.argv[1] if 1 < len(sys.argv) else FPL_FILE
    # Load the airport and the traffic
    the_airport = airport.load(APT_FILE)
    the_airport2 = airport.load2(APT_FILE)

    flights = Sour_and_Des.flights
    node_lock_periods = {}
    activation_times_list = []
    pathlist = []  # 按照飞机的顺序储存飞机的节点序号路径
    path_coordlist = []  # 按照飞机的顺序储存飞机的节点坐标路径
    Stand = []
    # fail_find_number = []
    points = the_airport2.points

    for p in points:
        if p.ptype == 'Stand':
            Stand.append(p.xy)

    stand_dict, runway_dict, stand_list, stand_dict2, runway_list, runway_dict2 \
        = Sour_and_Des.stand_and_runway_points(points=the_airport2.points)
    # network, pointcoordlist, network_cepo, in_angles, out_angles, in_angles_cepo, out_angles_cepo \
    #     = Initial_network.initial_network(the_airport2)
    graph, weights, time_windows, in_angles, out_angles, costs, pushback_edges = \
        Initial_network.initial_network(the_airport2)
    # print(time_windows)
    # print(costs)

    for flightnum in range(0, len(flights)):
    # for flightnum in range(0, 3):
        # 多飞机规划路径：
        # 初始化开始时间
        init_time = datetime.datetime(2023, 4, 17, 7, 0)
        graph_copy = graph
        results = []
        paths = []
        COST_list = []
        flight = flights[flightnum]

        # 这里是选择确定飞机的推出的时间
        if flight.departure == 'ZBTJ':
            start_time = flight.ttot - 600
        else:
            start_time = flight.aldt

        # 这里是选择确定飞机的起飞与终点
        source, target = Sour_and_Des.find_the_sour_des(stands=stand_dict, pists=runway_dict, flight=flight)

        name1 = show_point_name(source, points=the_airport2.points)
        name2 = show_point_name(target, points=the_airport2.points)
        # using the general example to test
        # source_flight = [155, 86]
        # des_flight = [170, 164]
        # sour = source_flight[flightnum]
        # des = des_flight[flightnum]

        check = False
        if len(graph[source]) > 1:  # Only one pushback do not think about this
            for edge in graph[source]:
                if edge not in pushback_edges:  # Ensure the boolean value
                    check = False
                    break
                if edge in pushback_edges:
                    check = True

            if check:  # When the stand have two ways to pushback, we need choose the smallest COST
                for edge in graph[source]:
                    graph_copy[source].remove(edge)
                    # print(graph_copy)
                    path, COST = TEST.AMOA_star(source, target, costs, graph, time_windows, start_time, out_angles,
                                                in_angles, Stand)

                    graph_copy[source].append(edge)

                    COST_list.append(COST)
                    paths.append(path)

            if COST_list:
                # 将 COST_list 中的所有集合扁平化为一个包含所有成本向量的列表
                flattened_list = [item for sublist in COST_list if sublist is not None for item in sublist]

                # 在扁平化后的列表中找到第一个元素最小的成本向量
                if flattened_list:
                    min_cost_vector = min(flattened_list, key=lambda x: x[0])
                else:
                    min_cost_vector = None  # 或其他适当的默认值
                COST = {min_cost_vector}
                # COST = min(COST_list, key=lambda x: x[0])
                if min_cost_vector:
                    path = paths[COST_list.index(COST)]
                else:
                    path = None
        else:  # the normal condition
            path, COST = TEST.AMOA_star(source, target, costs, graph, time_windows, start_time, out_angles, in_angles,
                                        Stand)

        # path, COST = TEST.AMOA_star(source, target, costs, graph, time_windows, start_time, out_angles, in_angles,
        # Stand)
        print("fligt:", flightnum, "Path:", path)
        print("Cost:", COST)
        # if path:
        #     Draw_path.create_matplotlib_figure(graph, path, name1, name2, flightnum)

    # route, route_coord, route_activation_times = quickest_path_with_time_windows(graph, weights, time_windows,
    # source, target, start_time)
    #
    #     activation_times_list.append(route_activation_times)
    #     pathlist.append(route)
    #     path_coordlist.append(route_coord)
    #
    #     get_node_lock_periods(pathlist, activation_times_list, network_cepo, flight, node_lock_periods)
    #
    #     print('flightnum', flightnum)
    #     print('path', route)
    #
    # # 确保目录存在
    # file = Cst.file
    # os.makedirs(file, exist_ok=True)
    #
    # # 现在我们可以调用这些函数将列表写入到文本文件
    # write_list_to_file(pathlist, file + '/pathlist.txt')
    # write_list_to_file(path_coordlist, file + '/path_coordlist.txt')
    # write_list_to_file(activation_times_list, file + '/activation_times_list.txt')
    #
    # # 现在我们可以调用这些函数将列表写入到json文件
    # write_list_to_json(pathlist, file + '/pathlist.json')
    # write_list_to_json(path_coordlist, file + '/path_coordlist.json')
    # write_list_to_json(activation_times_list, file + '/activation_times_list.json')

    # Find_Routing_for_test.find_routing(the_airport, the_airport2)
