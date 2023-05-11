import math
import pandas as pd
import geo
import datetime


# 转换路网的类型
def turn_network(network_point):
    neighbor_info = {key: list(value.keys()) for key, value in network_point.items()}
    return neighbor_info


# 将数字编号类型的路径序列转换为坐标类型
def list2node(list, pointcoordlist):
    plist = []
    for i in list:
        plist.append(pointcoordlist[i])
    return plist


# 打印出坐标类型的序列的point的信息
def print_plist(plist, points):
    for p in plist:
        for point in points:
            if point.xy == p:
                # print(f"Point: ptype={point.ptype}, name={point.name}, xy={point.xy}")
                # print(f"Point: {point.ptype} {point.name} {point.xy}", end="++")
                print(f" {point.ptype} {point.name} {point.xy}", end="--")


# 打印出一个路网的中每个point的neighbor point信息
def print_neighbor_info(neighbor_info, points):
    # 遍历新字典
    for key_xy, value_xys in neighbor_info.items():
        # 找到与键匹配的点并打印属性
        for point in points:
            if point.xy == key_xy:
                print(f"Key: ptype={point.ptype}, name={point.name}, xy={point.xy}")
                break

        # 找到与值匹配的点并打印属性
        for value_xy in value_xys:
            for point in points:
                if point.xy == value_xy:
                    print(f"Value: ptype={point.ptype}, name={point.name}, xy={point.xy}")
                    break


def create_neighbor_info_dataframe(neighbor_info, points):
    data = []

    # 遍历新字典
    for key_xy, value_xys in neighbor_info.items():
        key_info = None
        # 找到与键匹配的点并保存信息
        for point in points:
            if point.xy == key_xy:
                key_info = {"Point Type (Key)": point.ptype, "Point Name (Key)": point.name,
                            "Coordinates (Key)": point.xy}
                break

        # 找到与值匹配的点并保存信息
        for value_xy in value_xys:
            value_info = None
            for point in points:
                if point.xy == value_xy:
                    value_info = {"Point Type (Value)": point.ptype, "Point Name (Value)": point.name,
                                  "Coordinates (Value)": point.xy}
                    break

            if key_info is not None and value_info is not None:
                data.append({**key_info, **value_info})

    return pd.DataFrame(data)


def findpointtype(line1, line2, points):
    point_list_type = []
    point_list = [line1.xys[0], line1.xys[-1], line2.xys[0], line2.xys[-1]]
    for p in points:
        if p.xy in point_list:
            point_list_type.append(p.ptype)
    S = 'Stand'
    if S in point_list_type:
        return 1
    return 0


def initial_network(network_point, init_lines, init_points, points):
    # remove the path Stand to normal
    del_dict = {}
    for p, connections in network_point.items():
        for point in points:
            if point.xy == p and point.ptype == 'Stand':
                for connected_point in connections.keys():
                    for point2 in points:
                        if point2.xy == connected_point and point2.ptype == 'normal':
                            del_dict[p] = connected_point
    for p, connections in del_dict.items():
        network_point[p].pop(connections)
    return network_point


def blocknode(network, path, start_time):
    """

    """
    # start_time  # 此飞机的起始第一个点的时间
    # the current position of the obstacle
    block_timedict = {}
    path_cost = [0]

    for i in range(len(path) - 1):
        block_set = [start_time, start_time]

        path_cost.append(path_cost[-1] + network[path[i]][path[i + 1]])

        nextcost = network[path[i]][path[i + 1]]
        cost = 20 if nextcost > 20 else nextcost

        time1 = start_time + datetime.timedelta(seconds=path_cost[-2])  # block 开始时间
        time2 = time1 + datetime.timedelta(seconds=path_cost[-1]) + datetime.timedelta(seconds=cost)  # block 结束时间
        block_set[0] = time1
        block_set[1] = time2
        block_timedict[path[i]] = block_set

    return block_timedict


def blocknode2(network, path, start_time):
    """

    """
    # start_time  # 此飞机的起始第一个点的时间
    # the current position of the obstacle
    block_timedict2 = {}
    path_cost = [0]
    init_time = datetime.datetime(2023, 4, 17, 7, 0)
    s_t = (start_time - init_time).seconds
    # e_t = (start_time - init_time).seconds
    # block_set = [s_t, s_t]

    for i in range(len(path) - 1):
        block_set = [s_t, s_t]  # Initialize block_set as a new list with two elements

        path_cost.append(path_cost[-1] + network[path[i]][path[i + 1]])

        nextcost = network[path[i]][path[i + 1]]
        cost = 20 if nextcost > 20 else nextcost

        time1 = start_time + datetime.timedelta(seconds=path_cost[-2])  # block 开始时间
        time2 = time1 + datetime.timedelta(seconds=path_cost[-1]) + datetime.timedelta(seconds=cost)  # block 结束时间
        t1 = (time1 - init_time).seconds
        t2 = (time2 - init_time).seconds
        block_set[0] = t1
        block_set[1] = t2
        block_timedict2[i] = block_set

    return block_timedict2


def find_pushback_points(points, pointcoordlist):
    pushback_points = []
    for p in points:
        if p.ptype == 'pushback':
            # print(pointcoordlist.index(p.xy))
            pushback_points.append(pointcoordlist.index(p.xy))
    return pushback_points
