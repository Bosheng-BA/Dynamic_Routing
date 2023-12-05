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
        start_time = activation_times[i-1] + flight_start_time
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


    stand_dict, runway_dict, stand_list, stand_dict2, runway_list, runway_dict2 \
        = Sour_and_Des.stand_and_runway_points(points=the_airport2.points)
    # network, pointcoordlist, network_cepo, in_angles, out_angles, in_angles_cepo, out_angles_cepo \
    #     = Initial_network.initial_network(the_airport2)
    graph, weights, time_windows, in_angles, out_angles, costs = Initial_network.initial_network(the_airport2)
    # print(time_windows)
    # print(costs)

    for flightnum in range(0, len(flights)):
        flight = flights[flightnum]
        # 多飞机规划路径：
        # 初始化开始时间
        init_time = datetime.datetime(2023, 4, 17, 7, 0)

        # 这里是选择确定飞机的推出的时间
        if flight.departure == 'ZBTJ':
            start_time = flight.ttot - 600
        else:
            start_time = flight.aldt

        # 这里是选择确定飞机的起飞与终点
        source, target = Sour_and_Des.find_the_sour_des(stands=stand_dict, pists=runway_dict, flight=flight)

        # using the general example to test
        # source_flight = [155, 86]
        # des_flight = [170, 164]
        # sour = source_flight[flightnum]
        # des = des_flight[flightnum]

        # path, path_coord, path_activation_times = Find_Routing.find_routing\
        #     (the_airport, the_airport2, sour, des, flight, flightnum, network, pointcoordlist, network_cepo,
        #      in_angles, out_angles, in_angles_cepo, out_angles_cepo, node_lock_periods)
        # result = tsst.QPPTW_algorithm(graph, weights, time_windows, source, target, start_time)
        path, COST = TEST.AMOA_star(source, target, costs, graph, time_windows, start_time)
        print(path)
        # if result:
        #     print("Quickest Path:", [label[0] for label in result])
        # else:
        #     print("No path found.")
    #
    #     route, route_coord, route_activation_times = quickest_path_with_time_windows(graph, weights, time_windows, source, target, start_time)
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


