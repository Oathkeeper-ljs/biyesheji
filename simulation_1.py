import random
import switch
import DC
import delaunay2D
import numpy as np
import table_create
import Data
import math
import hashutils
import time

topo = 90

def run(topo):
    toposize = topo

    """
    初始化swt
    最好设置为可变长度
    """
    swt_num = toposize
    swt_list = {}
    for _ in range(swt_num):
        coor1 = 100*random.random()
        coor2 = 100*random.random()
        coor = [coor1,coor2]
        vars()['s%d'%_] = switch.switch(coor,_,_)
        swt_list[_] = vars()['s%d'%_]

    """
    初始化DC
    """
    dc_num = toposize
    dc_list = {}
    for _ in range(dc_num):
        vars()['d%d'%_] = DC.DataCenter(_,_)
        dc_list[_] = vars()['d%d'%_]

    radius = 100
    seeds = []
    for keys in swt_list:
        seeds.append(swt_list[keys].coor)

    """
    计算swt的Delaunay三角剖分
    """

    center = np.mean(seeds, axis=0)
    dt = delaunay2D.Delaunay2D(center, 50*radius)

    for s in seeds:
        dt.addPoint(s)

    # print (len(dt.exportTriangles()), "Delaunay triangles")
    # print(dt.exportTriangles())
    #
    import matplotlib.pyplot as plt
    import matplotlib.tri
    import matplotlib.collections

    # Create a plot with matplotlib.pyplot
    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.set_aspect('equal')
    plt.axis([-1, radius+1, -1, radius+1])

    # Plot our Delaunay triangulation (plot in blue)
    cx, cy = zip(*seeds)
    dt_tris = dt.exportTriangles()
    ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')

    plt.show()

    """
    在交换机上生成转发表
    """
    triangle_list = dt.exportTriangles()
    table_create.table_create(triangle_list,swt_list)

    data_list = {}

    """
    随机生成data_num个数据
    """
    data_in = []
    data_out = []
    data_in_num = 4000
    data_out_num = 4000
    # data_num = 7000
    for _ in range(data_in_num):
        locate = random.randint(0,toposize-1)*10 + random.randint(0,4)
        type = 'intra'
        tmp = Data.Data(_,locate,type,8,radius)
        data_in.append(tmp)
        data_list[_] = tmp
        #print(tmp.id, tmp.value,tmp.type, tmp.locate, tmp.coordinate)
    for _ in range(data_out_num):
        locate = random.randint(0,toposize-1)*10 + random.randint(0,4)
        type = 'inter'
        tmp = Data.Data(_,locate,type,8,radius)
        data_out.append(tmp)
        data_list[_+data_in_num] = tmp
        #print(tmp.id, tmp.value,tmp.type, tmp.locate, tmp.coordinate)
    # print("——————————————————————————————————————————————————————————————————————————————————")

    # print('data_in列表大小：'+str(len(data_in)))
    # print('data_out列表大小：'+str(len(data_out)))

    """
    将数据放入指定的表中
    """
    for keys in data_list:
        if data_list[keys].type == 'intra':
            # print(str(keys)+'数据'+str(data_list[keys].value))
            dc_list[math.floor(data_list[keys].locate / 10)].table_intra.insert([data_list[keys].value, data_list[keys].locate % 10])
        else:
            dc = table_create.data_publish(swt_list,data_list[keys])
            # print('dc:',dc)
            dc_list[dc].table_inter.insert(hashutils.fingerprint(data_list[keys].value, size =1), data_list[keys].locate)

    """
    打印每个DC的两张表
    """
    # print("DC域内的cuckoo表：")
    # for keys in dc_list:
    #     print(keys,dc_list[keys].table_intra.buckets)
    #
    # print("——————————————————————————————————————————————————————————————————————————————————")
    # print("DC域间的全局表：")
    # for keys in dc_list:
    #     print(keys,dc_list[keys].table_inter.table)

    """
    进行数据查找
    查找分为两类：
    1、在DC内进行域内查找，针对的是仅在域内共享的数据   data_in[]
    2、跨DC进行域间查找，由随机的一个DC进入，该DC负责将请求转发出去，
       经swt的多跳转发后，到达最终的DC，该DC查找全局表，给出结果
    """
    search_num = 1000
    # print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('域内查找')
    # print('————————————————————————————————————————————————————————————————————————————————————————————————')
    intra_right_list = []
    intra_wrong_list = []
    intra_search_num = search_num
    intra_time_s = time.time()
    for _ in range(intra_search_num):
        index_random = random.randint(0,len(data_in)-1)
        # print('index_random is '+ str(index_random))
        # print('data id:'+ str(data_in[index_random].id))
        # print('data value:'+ str(data_in[index_random].value))
        # print('data locate:'+ str(data_in[index_random].locate))
        # print('data fingerprint:'+ str(hashutils.fingerprint(data_in[index_random].value,1)))
        # print('data index'+str(dc_list[math.floor(data_in[index_random].locate / 10)].table_intra._get_index([data_in[index_random].value,0])))
        # print('data alnate index'+str(dc_list[math.floor(data_in[index_random].locate / 10)].table_intra._get_alternate_index(dc_list[math.floor(data_in[index_random].locate / 10)].table_intra._get_index(data_in[index_random].value),
        #                                                                                                                    hashutils.fingerprint(data_in[index_random].value,1))))

        if table_create.search_intra(data_in[index_random],math.floor(data_in[index_random].locate / 10),dc_list) is not False:
            intra_right_list.append(_)
        else:
            intra_wrong_list.append(_)
    intra_time_e = time.time()

    print('right_num:'+ str(len(intra_right_list)))
    print('wrong_num:'+ str(len(intra_wrong_list)))
    print('域内查找时间为：' + str(intra_time_e-intra_time_s))

    # print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('域间查找')
    # print('————————————————————————————————————————————————————————————————————————————————————————————————')
    inter_right_list = []
    inter_wrong_list = []
    inter_search_num = search_num
    inter_forward = 0
    inter_time_s = time.time()
    for _ in range(inter_search_num):
        index_random = random.randint(0,len(data_out)-1)

        # print('index_random is '+ str(index_random))
        # print('data id:'+ str(data_out[index_random].id))
        # print('data value:'+ str(data_out[index_random].value))
        # print('data locate:'+ str(data_out[index_random].locate))
        # print('data fingerprint:'+ str(hashutils.fingerprint(data_out[index_random].value,1)))

        dc_id_random = random.randint(0,len(dc_list)-1)
        # print('dc_id_random is '+ str(dc_id_random))
        res = table_create.search_inter(data_out[index_random],dc_id_random,dc_list,swt_list)
        if res[0]:
            inter_right_list.append(_)
            delay = res[1]
        else:
            inter_wrong_list.append(_)
    inter_time_e = time.time()

    print('right_num:'+ str(len(inter_right_list)))
    print('wrong_num:'+ str(len(inter_wrong_list)))
    print('域间查找时间为：'+str(inter_time_e-inter_time_s))
    print('转发次数为：'+str(delay))

    return [(inter_time_e-inter_time_s),delay]


count = 0
flag = 0
delay_time = 0
for loop in range(100):
    if flag == 1:
        break
    else:
        print('flag=%d'%flag)
        print(loop)
        try:
            [nice,tmp] = run(topo)
            print('time:%s'%nice)
            print('forward:%s'%delay_time)
            count += nice
            delay_time += tmp
            flag += 1
        except:
            pass
print('average forward time is:'+str(delay_time/10))
print('average time is:'+str(count/10))
print('final time is:'+str(count/10+0.01*delay_time/10))

print('dht time is:'+str(count/10+0.01*math.log2(topo)))