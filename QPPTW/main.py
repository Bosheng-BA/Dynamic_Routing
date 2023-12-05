import sys
import airport
import Initial_network
import datetime
import Sour_and_Des
import json
import os
import tsst
import Draw_path
import QPPTW

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
    fail_find_number = []
    points = the_airport2.points

    for p in points:
        if p.ptype == 'Stand':
            Stand.append(p.xy)
    # print(Stand)

    stand_dict, runway_dict, stand_list, stand_dict2, runway_list, runway_dict2 \
        = Sour_and_Des.stand_and_runway_points(points)

    graph, weights, time_windows, in_angles, out_angles, pushback_edges = Initial_network.initial_network(the_airport2)

    # for flightnum in range(0, len(flights)):
    # list = [2, 27, 30, 44, 48, 495]
    Standlist = ['911', '411', '108', '205', '417', '879']
    Runwaylist = ['A1', '16R-34L', 'W3', '16L-34R', 'B6', '16R-34L']
    path_list = []
    for flightnum in range(len(Standlist)):

        # 初始化开始时间
        init_time = datetime.datetime(2023, 4, 17, 7, 0)
        results = []
        paths = []
        new_time_windows_list = []
        graph_copy = graph
        flight = flights[flightnum]

        # 这里是选择确定飞机的推出的时间
        if flight.departure == 'ZBTJ':
            start_time = flight.ttot - 600
        else:
            start_time = flight.aldt

        # 这里是选择确定飞机的起飞与终点
        # source, target = Sour_and_Des.find_the_sour_des(stands=stand_dict, pists=runway_dict, flight=flight)
        source = show_point_coor(Standlist[flightnum], points=the_airport2.points)
        target = show_point_coor(Runwaylist[flightnum], points=the_airport2.points)
        check = False
        if len(graph[source]) > 1:  # Only one pushback do not think about this
            for edge in graph[source]:
                if edge not in pushback_edges:  # Ensure the boolean value
                    check = False
                    break
                if edge in pushback_edges:
                    check = True

        if check:  # When the stand have two ways to pushback, we need choose one
            for edge in graph[source]:
                graph_copy[source].remove(edge)
                # print(graph_copy)
                result, path_for_test, new_time_windows = QPPTW.QPPTW_algorithm(graph_copy, weights, time_windows, source, target,
                                                              start_time, in_angles, out_angles, Stand)
                graph_copy[source].append(edge)
                results.append(result)
                new_time_windows_list.append(new_time_windows)
                paths.append(path_for_test)
            new_results = results
            if new_results:
                result = min(new_results,
                             key=lambda x: x[-1][1][0] if x and x[-1] and len(x[-1]) >= 2 else float('inf'))
                new_time_windows = new_time_windows_list[results.index(result)]
        else:  # the normal condition
            result, path_for_test, new_time_windows = QPPTW.QPPTW_algorithm(graph, weights, time_windows, source, target, start_time,
                                                          in_angles, out_angles, Stand)

        time_windows = new_time_windows
        # result, path_for_test = tsst.QPPTW_algorithm(graph, weights, time_windows, source, target, start_time,
        #                                              in_angles, out_angles)
        name1 = show_point_name(source, points=the_airport2.points)
        name2 = show_point_name(target, points=the_airport2.points)

        # 检查输出以及绘制图像
        if result:
            print(flightnum, "Quickest Path:", [label[0] for label in result])
            path = [label[0] for label in result]
            path_list.append(path)
            # if flightnum in list:
                # Draw_path.create_matplotlib_figure(graph, path, name1, name2, flightnum)
        else:
            fail_find_number.append(flightnum)
            # 如果找不到的就在图中找出是那两个点
            # path = [source, target]
            for p in range(len(path_for_test)):
                # print("times:", p)
                path = path_for_test[p]
                # path = [label[0] for label in p]
                flightnum2 = str(flightnum) + "_No_" + str(p)
                # Draw_path.create_matplotlib_figure(graph, path, name1, name2, flightnum2)
            print("No path found.", flightnum, 'source', source, name1, 'targrt', target, name2)

    Draw_path.create_matplotlib_figure_for_mutiaircraft(graph, path_list, name1, name2, flightnum)

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
