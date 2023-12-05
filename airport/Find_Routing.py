import sys
import os.path
import tkinter
import airport
import traffic
import hmi
import hmi2
import Initial_network
import RSA4CEPO2
import time
import datetime
import helpfunction
import Draw_path
import Sour_and_Des


def find_routing(the_airport, the_airport2, sour, des):

    # 单架飞机规划路径：
    # network_point, x, y, pointcoordlist, network = findpath.findRSApath(the_airport2)
    # s0 = findpath.findsource(points=the_airport2.points)
    # d0 = findpath.finddes(points=the_airport2.points)
    # s = pointcoordlist.index(s0)
    # # s = 12
    # d = pointcoordlist.index(d0)
    # orad = 500  # obstacle radius
    # ospeed = 2  # obstacle speed
    # (RSA4CEPO2.main(network, s, d, x, y, orad, ospeed, pointcoordlist, the_airport2, network_point))

    # 多飞机规划路径：
    # 初始化开始时间
    init_time = datetime.datetime(2023, 4, 17, 7, 0)
    pathlist = []  # 按照飞机的顺序储存飞机的节点序号路径
    path_coordlist = []  # 按照飞机的顺序储存飞机的节点坐标路径
    blockinfo = {}  # 与实际小时分钟计数
    blockinfo2 = {}  # 按照绝对时间计算

    # 为当前飞机规划路径
    network, pointcoordlist, network_cepo, in_angles, out_angles, in_angles_cepo, out_angles_cepo = \
        Initial_network.initial_network(the_airport2)

    # sour, des = Sour_and_Des.find_the_sour_des(points=the_airport2.points, pointcoordlist=pointcoordlist,
    #                                            stands=stand_dict, pists=runway_dict)

    # print(the_airport2.points[0].ptype)
    # print(network_cepo)
    Draw_path.create_matplotlib_figure0(network, pointcoordlist, path=[], stand=34, runway=2)

    for flightnum in range(1):  # 这里我们考虑多架飞机的情况
        start_time = init_time + datetime.timedelta(seconds=10 * flightnum)
        # 随机选择起点和终点
        s = pointcoordlist.index(sour)
        d = pointcoordlist.index(des)

        # source = Initial_network.findsource(the_airport2.points)
        # destination = Initial_network.finddes(the_airport2.points)

        # # 为当前飞机规划路径
        # network, x, y, pointcoordlist, network = findpath.findRSApath(the_airport2, blocked_points)
        # s = pointcoordlist.index(source)
        # d = pointcoordlist.index(destination)

        # source_flight = [155, 86]
        # des_flight = [170, 164]
        # s = source_flight[flightnum]
        # d = des_flight[flightnum]

        # s = 64
        # d = pointcoordlist.index((20155, 6926))
        # print("source:", s, ' destination:', d)
        # print(pointcoordlist[170], pointcoordlist[180])

        if flightnum != 0:
            path = pathlist[-1]
            block_timedict = helpfunction.blocknode(network_cepo, path, start_time)
            blockinfo[flightnum - 1] = block_timedict
            block_timedict2 = helpfunction.blocknode2(network_cepo, path, start_time)
            blockinfo2[flightnum - 1] = block_timedict2

        path_set, length_set, plist, t, v = RSA4CEPO2.main(network_cepo, in_angles_cepo, out_angles_cepo, s, d,
                                                           flightnum, pathlist, pointcoordlist, the_airport2, network,
                                                           start_time, blockinfo, points=the_airport2.points)
        print("Flightnum :", flightnum)
        print('shortest path:', path_set, 'length:', length_set)

        # 更新blocked_points，考虑当前飞机的位置和前一架飞机的位置
        # ... 省略更新blocked_points的代码

        pathlist.append(path_set)
        path_coordlist.append(plist)

        # 暂停20秒
        time.sleep(10)

        # 更新开始时间
        start_time += datetime.timedelta(seconds=10)
        # Draw.create_bokeh_animation(network, network_cepo, pointcoordlist, t, v, plist)
        Draw_path.create_matplotlib_figure(network_point=network, pointcoordlist=pointcoordlist, path=plist, stand=s, runway=d)
    # Draw_path.create_bokeh_animation_with_paths(network, network_cepo, pointcoordlist, v, t, pathlist, plist,
    #                                             blockinfo2, path_coordlist)


def loop_test(points, the_airport2, the_airport):
    stand_dict, runway_dict, stand_list, stand_dict2, runway_list, runway_dict2 \
        = Sour_and_Des.stand_and_runway_points(points)
    # print(runway_list)
    """遍历所有的停机坪与跑道起飞点的位置是否存在可行解"""
    # for i in range(0, len(stand_list)):
    #     sour = stand_list[i]
    #     if sour[1] >= 6926:
    #         B7 = runway_dict['B7']
    #         rp = [B7, (20155, 6926), (23610, 6926), (21057, 9026), (24108, 9026)]
    #         for j in range(len(rp)):
    #             des = rp[j]
    #             print("The process i=", i, " j=", j)
    #             find_routing(the_airport, the_airport2, sour, des)
    #     else:
    #         A10 = runway_dict['A10']
    #         A1 = runway_dict['A1']
    #         rp2 = [A10, A1, (20155, 6926), (21057, 9026), (24108, 9026)]
    #         for j in range(len(rp2)):
    #             des = rp2[j]
    #             print("The process i=", i, " j=", j)
    #             find_routing(the_airport, the_airport2, sour, des)

    # """遍历所有的跑道起飞点与停机坪的位置是否存在可行解"""
    # rl = ['B3','B4','A1','A5','W3','W7','W8','B6','B5','A10','A11']
    # rlabove = ['B3','B4','B6','B5']
    # rlbelow = ['A1','A5','A10','A11']
    # for i in range(6, len(runway_list)):
    #     sour = runway_list[i]
    #     sourname = runway_dict2[sour]
    #     if sourname in rl:
    #         for j in range(38, len(stand_list)):
    #             des = stand_list[j]
    #             if stand_list[j][1] >= 6926 and (sourname in rlabove):
    #                 print("The arrive process i=", i, " j=", j)
    #                 find_routing(the_airport, the_airport2, sour, des)
    #             elif stand_list[j][1] < 6926 and (sourname in rlbelow):
    #                 print("The arrive process i=", i, " j=", j)
    #                 find_routing(the_airport, the_airport2, sour, des)
    #             elif sourname not in rlbelow:
    #                 print("The arrive process i=", i, " j=", j)
    #                 find_routing(the_airport, the_airport2, sour, des)

